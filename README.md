para devolverlo a la vida>>>

# 1. Crear el resource group y el registro de nuevo
az group create --name rg-acr-demo --location eastus

az acr create --resource-group rg-acr-demo --name miregistroarc2025xk7 --sku Basic --admin-enabled true

# 2. Disparar el pipeline
git commit --allow-empty -m "ci: retomar proyecto"
git push origin main
