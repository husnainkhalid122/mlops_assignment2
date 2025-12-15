# MLOps Project

Comprehensive MLOps assignment including Git, DVC, CI/CD, Docker, Airflow, FastAPI, and AWS deployment.

## Project Structure

```
mlops_assignment2/
├── src/                    # Training scripts
├── api/                    # FastAPI application
├── data/                   # Dataset storage (tracked with DVC)
├── models/                 # Trained models
├── tests/                  # Unit tests
├── .github/workflows/      # GitHub Actions CI/CD
├── dvc_storage/            # DVC remote storage
├── requirements.txt        # Dependencies
└── dvc.yaml               # DVC pipeline
```

## Quick Start

1. Clone repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Initialize DVC: `dvc init`
6. Run training: `dvc repro`

## Tasks

- Task 1: Project Setup + Git + DVC
- Task 2: CI/CD Pipeline (GitHub Actions)
- Task 3: Docker
- Task 4: Airflow Pipeline
- Task 5: FastAPI
- Task 6: AWS EC2 + S3
- Task 7: Final Deliverables
