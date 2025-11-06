## Purpose

Give AI coding agents immediate, actionable context for working in this repository: key files, data flow, environment setup, and project-specific conventions.

## Big picture (what to know first)

- This is an MLOps demo pipeline built around Jupyter notebooks. The canonical workflow lives in `mlops_pipeline/src/` and proceeds roughly:
  1. `cargar_datos.ipynb` — data ingestion
  2. `compresion_eda.ipynb` — EDA (spelled "compresion_eda.ipynb")
  3. `model_trainig.ipynb` — training (note the filename typo: "trainig")
  4. `model_evaluation.ipynb` — evaluation
  5. `model_deploy.ipynb` — deployment steps
  6. `model_monitoring.ipynb` — monitoring

- Stable, runnable code (as opposed to analysis notebooks) should be in `mlops_pipeline/src/*.py` — currently `ft_engineering.py` and `heuristic_model.py` are the intended script locations.

## Key files and data

- `base_de_datos.csv` — the primary dataset at the repo root. Notebooks expect data here by relative path.
- `set_up.bat` — Windows setup script. Important: the script expects `etl_scripts\src` and `config.json` with a `project_code` field; in this repo the directory layout differs. Use this script only after verifying/updating paths or prefer manual venv creation (examples below).
- `config.json` and `requirements.txt` are present but currently empty — treat them as places to add project configuration and pinned dependencies.

## Project-specific patterns & conventions

- Filenames and notebook titles use Spanish (e.g., `cargar_datos.ipynb`, `compresion_eda.ipynb`). Keep Spanish naming when adding new notebooks or scripts for consistency.
- Notebooks are the primary source of exploratory and step-by-step logic; when extracting production code, port key functions into `ft_engineering.py` or new `.py` modules under `mlops_pipeline/src/`.
- There is one obvious filename typo: `model_trainig.ipynb` (should be `model_training.ipynb`). Don't rename without confirming references in other files or updating the setup script.

## How to run locally (concise, tested steps for Windows PowerShell)

1. Create and activate a venv (preferred manual flow):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
if (Test-Path requirements.txt) { pip install -r requirements.txt }
python -m ipykernel install --user --name=proj-venv --display-name="proj-venv Python"
```

2. Open the notebooks in `mlops_pipeline/src/` and select the `proj-venv` kernel.

3. If you must use `set_up.bat`, inspect and fix the hardcoded paths before running (it attempts to cd into `etl_scripts\src` and read `project_code` from `config.json`).

## Integration points & external dependencies

- Notebooks read/write `base_de_datos.csv` and may write intermediate artifacts locally. Expect no external cloud services configured in the repo.
- Add any external package requirements to `requirements.txt` so `set_up.bat` and CI can install them.

## Editing guidelines for AI agents (concrete do/don't)

- DO: Make small, verifiable changes. Prefer adding new `.py` modules and unit tests instead of editing large notebooks.
- DO: Reference paths exactly as they appear in the repo (`mlops_pipeline/src/model_trainig.ipynb`), and call out the filename typo in PR descriptions if you rename files.
- DO NOT: Run `set_up.bat` blindly — it contains directory assumptions that don't match the repo root. Update it only with an explicit task and tests verifying venv creation.

## Examples to copy/paste

- To run the training notebook interactively: open `mlops_pipeline/src/model_trainig.ipynb` and run cells after selecting the venv kernel.
- To extract reusable code from a notebook: copy the function-level code into `mlops_pipeline/src/ft_engineering.py` and add an `if __name__ == "__main__":` entry that accepts a CSV path and outputs features.

## Quick mental model for reviewers

- Notebooks = experimentation and narrative. `.py` in `mlops_pipeline/src/` = code that should be production-ready.
- Any change that moves code from a notebook into `.py` should include a small test or a short example script demonstrating the same input/output on `base_de_datos.csv`.

---

If any of the paths, filenames, or expectations above are wrong or missing details you need, tell me which area to expand and I will update this doc and adapt the setup steps.
