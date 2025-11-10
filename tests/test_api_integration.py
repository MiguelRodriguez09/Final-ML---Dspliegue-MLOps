import os
import requests

# Prefer in-process Flask test client (to collect coverage) when possible.
API_BASE = os.getenv('API_BASE_URL', 'http://localhost:5000')
USE_TEST_CLIENT = False
TEST_CLIENT = None
try:
    # Attempt to import the app and load artifacts so tests run in-process
    from mlops_pipeline.src import model_deploy as md
    if hasattr(md, 'load_artifacts'):
        # Load artifacts if not already loaded
        try:
            md.load_artifacts()
        except Exception:
            # if loading fails, we'll fall back to external requests
            pass
    if hasattr(md, 'app'):
        TEST_CLIENT = md.app.test_client()
        USE_TEST_CLIENT = True
except Exception:
    USE_TEST_CLIENT = False


def _get(endpoint, **kwargs):
    if USE_TEST_CLIENT and TEST_CLIENT is not None:
        resp = TEST_CLIENT.get(endpoint)
        # emulate requests.Response interface minimally
        class R:
            status_code = resp.status_code
            def json(self):
                return resp.get_json()
        return R()
    else:
        return requests.get(f"{API_BASE}{endpoint}", **kwargs)


def _post(endpoint, json=None, **kwargs):
    if USE_TEST_CLIENT and TEST_CLIENT is not None:
        resp = TEST_CLIENT.post(endpoint, json=json)
        class R:
            status_code = resp.status_code
            def json(self):
                return resp.get_json()
        return R()
    else:
        return requests.post(f"{API_BASE}{endpoint}", json=json, **kwargs)


def test_health_check():
    """Health endpoint should return 200 and contain expected keys"""
    r = _get('/', timeout=5)
    assert r.status_code == 200, f"Health endpoint returned {r.status_code}"
    data = r.json()
    # basic shape checks
    assert 'status' in data
    assert 'model_loaded' in data
    assert 'preprocessor_loaded' in data


def test_model_info():
    """Model info should return model metadata and metrics"""
    r = _get('/model-info', timeout=5)
    assert r.status_code == 200, f"Model-info returned {r.status_code}"
    data = r.json()
    assert 'model_name' in data
    assert 'metrics' in data
    metrics = data.get('metrics', {})
    # expect numeric metric keys (if present)
    assert any(k in metrics for k in ('test_accuracy', 'test_roc_auc', 'test_f1'))


def test_predict_single():
    """POST /predict should return prediction and churn_probability"""
    payload = {
        "CreditScore": 619,
        "Geography": "France",
        "Gender": "Female",
        "Age": 42,
        "Tenure": 2,
        "Balance": 0,
        "NumOfProducts": 1,
        "HasCrCard": 1,
        "IsActiveMember": 1,
        "EstimatedSalary": 101348.88
    }
    r = _post('/predict', json=payload, timeout=10)
    assert r.status_code == 200, f"Predict returned {r.status_code}"
    data = r.json()
    # Support two possible response shapes that might be returned by the API
    if 'prediction' in data and 'churn_probability' in data:
        prob = data.get('churn_probability')
        assert isinstance(prob, float) or isinstance(prob, int)
        assert 0.0 <= float(prob) <= 1.0
    else:
        # legacy/alternative shape: predictions + probabilities
        assert 'predictions' in data and 'probabilities' in data
        probs = data.get('probabilities')
        # ensure probabilities shape matches
        assert isinstance(probs, list) and len(probs) >= 1
        p0 = probs[0]
        assert isinstance(p0, list) and len(p0) >= 2
        # probability for churn assumed to be second class
        churn_prob = float(p0[-1])
        assert 0.0 <= churn_prob <= 1.0


def test_predict_batch():
    """POST /predict-batch should accept an array of records and return predictions list"""
    batch = [
        {
            "CreditScore": 850,
            "Geography": "France",
            "Gender": "Male",
            "Age": 45,
            "Tenure": 10,
            "Balance": 150000,
            "NumOfProducts": 3,
            "HasCrCard": 1,
            "IsActiveMember": 1,
            "EstimatedSalary": 200000
        },
        {
            "CreditScore": 400,
            "Geography": "Germany",
            "Gender": "Male",
            "Age": 55,
            "Tenure": 1,
            "Balance": 0,
            "NumOfProducts": 1,
            "HasCrCard": 0,
            "IsActiveMember": 0,
            "EstimatedSalary": 30000
        }
    ]
    # The API expects a raw JSON array for batch endpoint
    # The API expects a raw JSON array for batch endpoint
    r = _post('/predict-batch', json=batch, timeout=20)
    assert r.status_code == 200, f"Predict-batch returned {r.status_code}"
    data = r.json()
    assert 'predictions' in data
    preds = data.get('predictions')
    assert isinstance(preds, list)
    assert len(preds) == len(batch)
    for p in preds:
        assert 'prediction' in p
        # support both 'churn_probability' and 'probability' field names
        if 'churn_probability' in p:
            prob = p['churn_probability']
            assert 0.0 <= float(prob) <= 1.0
        else:
            # API may return a 'probability' array [prob_no, prob_yes] or a single value
            assert 'probability' in p
            prob_field = p['probability']
            if isinstance(prob_field, list):
                prob_val = float(prob_field[-1])
            else:
                prob_val = float(prob_field) if prob_field is not None else None
            assert prob_val is None or (0.0 <= prob_val <= 1.0)
