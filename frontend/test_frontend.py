#!/usr/bin/env python3
"""
MLOps Frontend - Test Suite
Pruebas automatizadas para verificar la integración con la API
"""

import json
import time
import requests
from typing import Dict, Any

# Configuración
API_BASE_URL = 'http://localhost:5000'
FRONTEND_URL = 'http://localhost:8080'

class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.YELLOW}ℹ {text}{Colors.RESET}")

def test_api_connection() -> bool:
    """Test API connectivity"""
    print_header("Test 1: API Connection")
    
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        data = response.json()
        
        if response.status_code == 200:
            print_success(f"API Status: {data.get('status')}")
            print_success(f"Model Loaded: {data.get('model_loaded')}")
            print_success(f"Preprocessor Loaded: {data.get('preprocessor_loaded')}")
            return True
        else:
            print_error(f"API returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to API. Is it running?")
        print_info(f"Expected URL: {API_BASE_URL}")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_model_info() -> bool:
    """Test model info endpoint"""
    print_header("Test 2: Model Information")
    
    try:
        response = requests.get(f"{API_BASE_URL}/model-info", timeout=5)
        data = response.json()
        
        if response.status_code == 200:
            print_success(f"Model Name: {data.get('model_name')}")
            print_success(f"Model Type: {data.get('model_type')}")
            print_success(f"Features: {data.get('n_features')}")
            
            metrics = data.get('metrics', {})
            print_success(f"Test Accuracy: {metrics.get('test_accuracy', 0):.4f}")
            print_success(f"Test ROC-AUC: {metrics.get('test_roc_auc', 0):.4f}")
            return True
        else:
            print_error(f"Failed with status code: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_prediction() -> bool:
    """Test prediction endpoint"""
    print_header("Test 3: Single Prediction")
    
    # Test data
    test_input = {
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
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=test_input,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        data = response.json()
        
        if response.status_code == 200:
            prediction = "CHURN" if data.get('prediction') == 1 else "NO CHURN"
            probability = data.get('churn_probability', 0)
            
            print_success(f"Prediction: {prediction}")
            print_success(f"Churn Probability: {probability:.2%}")
            
            print("\n" + Colors.BOLD + "Input Data:" + Colors.RESET)
            for key, value in test_input.items():
                print(f"  {key}: {value}")
            
            return True
        else:
            print_error(f"Failed with status code: {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_batch_prediction() -> bool:
    """Test batch prediction endpoint"""
    print_header("Test 4: Batch Prediction")
    
    # Test data
    batch_data = [
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
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict-batch",
            json={"data": batch_data},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        data = response.json()
        
        if response.status_code == 200:
            predictions = data.get('predictions', [])
            print_success(f"Processed {len(predictions)} records")
            
            for i, pred in enumerate(predictions, 1):
                prediction = "CHURN" if pred.get('prediction') == 1 else "NO CHURN"
                probability = pred.get('churn_probability', 0)
                print(f"  Record {i}: {prediction} ({probability:.2%})")
            
            return True
        else:
            print_error(f"Failed with status code: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_frontend_server() -> bool:
    """Test if frontend server is accessible"""
    print_header("Test 5: Frontend Server")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        
        if response.status_code == 200:
            print_success(f"Frontend accessible at: {FRONTEND_URL}")
            print_success(f"Status Code: {response.status_code}")
            
            # Check for key elements in HTML
            content = response.text.lower()
            if 'mlops' in content:
                print_success("HTML contains MLOps references")
            if 'prediction' in content or 'predicción' in content:
                print_success("HTML contains prediction functionality")
                
            return True
        else:
            print_error(f"Frontend returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to frontend server. Is it running?")
        print_info(f"Expected URL: {FRONTEND_URL}")
        print_info("Start with: python server.py")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_cors() -> bool:
    """Test CORS configuration"""
    print_header("Test 6: CORS Configuration")
    
    try:
        response = requests.options(
            f"{API_BASE_URL}/predict",
            headers={
                'Origin': FRONTEND_URL,
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            },
            timeout=5
        )
        
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        
        if cors_header:
            print_success(f"CORS enabled: {cors_header}")
            
            methods = response.headers.get('Access-Control-Allow-Methods', '')
            if 'POST' in methods:
                print_success("POST method allowed")
            
            headers_allowed = response.headers.get('Access-Control-Allow-Headers', '')
            if 'Content-Type' in headers_allowed.lower():
                print_success("Content-Type header allowed")
            
            return True
        else:
            print_error("CORS not configured properly")
            print_info("Add CORS(app) to model_deploy.py")
            return False
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print(f"\n{Colors.BOLD}MLOps Frontend - Test Suite{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}\n")
    
    tests = [
        ("API Connection", test_api_connection),
        ("Model Information", test_model_info),
        ("Single Prediction", test_prediction),
        ("Batch Prediction", test_batch_prediction),
        ("Frontend Server", test_frontend_server),
        ("CORS Configuration", test_cors),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
            time.sleep(0.5)  # Small delay between tests
        except Exception as e:
            print_error(f"Test '{name}' crashed: {str(e)}")
            results.append((name, False))
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Colors.GREEN}PASSED{Colors.RESET}" if result else f"{Colors.RED}FAILED{Colors.RESET}"
        print(f"{name:.<40} {status}")
    
    print(f"\n{Colors.BOLD}Total: {passed}/{total} tests passed{Colors.RESET}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All tests passed!{Colors.RESET}")
        print(f"\n{Colors.GREEN}✓ Frontend is ready to use!{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Open {FRONTEND_URL} in your browser{Colors.RESET}\n")
        return True
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}⚠ Some tests failed{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Please check the errors above and fix them{Colors.RESET}\n")
        return False

if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}\n")
        exit(1)
