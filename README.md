# fastapi-aks-secure
Python-based FastAPI app that authenticates via Azure Entra ID, runs in a Docker container on AKS, and uses Azure Key Vault for secrets. The CI/CD pipeline in GitHub Actions performs static analysis, container vulnerability scanning, and deploys automatically to AKS using OIDC authentication — no stored secrets.
