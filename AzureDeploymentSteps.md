````markdown
# Despliegue de la PoC de Anonimización en Azure

A continuación se recogen todos los pasos necesarios para desplegar tu proyecto Flask en Azure App Service, integrando los servicios de Azure Document Intelligence y Azure Text Analytics.

---

## 1. Instalar y configurar Azure CLI

1. Descarga e instala la Azure CLI si no la tienes:
   ```bash
   https://learn.microsoft.com/cli/azure/install-azure-cli
````

2. Abre la terminal y autentícate:

   ```bash
   az login
   ```
3. (Opcional) Selecciona tu suscripción si tienes varias:

   ```bash
   az account set --subscription "Nombre o ID de tu suscripción"
   ```

---

## 2. Crear un grupo de recursos

```bash
az group create \
  --name anonimiza-rg \
  --location westeurope
```

---

## 3. Provisionar los servicios AI de Azure

### 3.1. Crear Form Recognizer (Document Intelligence)

```bash
az cognitiveservices account create \
  --name anonimiza-form-recognizer \
  --resource-group anonimiza-rg \
  --kind FormRecognizer \
  --sku S0 \
  --location westeurope \
  --yes
```

### 3.2. Crear Text Analytics (PII Detection)

```bash
az cognitiveservices account create \
  --name anonimiza-text-analytics \
  --resource-group anonimiza-rg \
  --kind TextAnalytics \
  --sku S0 \
  --location westeurope \
  --yes
```

---

## 4. Preparar la aplicación para Azure App Service

### 4.1. Requisitos en `requirements.txt`

```txt
flask
azure-ai-formrecognizer
azure-ai-textanalytics
python-dotenv
PyPDF2
```

### 4.2. Crear `startup.sh`

```bash
#!/usr/bin/env bash
gunicorn --bind=0.0.0.0 --timeout 600 app:app
```

Dale permisos de ejecución:

```bash
chmod +x startup.sh
```

### 4.3. (Opcional) Dockerfile

```dockerfile
FROM mcr.microsoft.com/azure-cli-python:3.9
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN chmod +x startup.sh
CMD ["./startup.sh"]
```

---

## 5. Crear Plan y Web App en Azure App Service

### 5.1. Crear App Service Plan

```bash
az appservice plan create \
  --name anonimiza-plan \
  --resource-group anonimiza-rg \
  --sku B1 \
  --is-linux
```

### 5.2. Crear Web App para Python

```bash
az webapp create \
  --resource-group anonimiza-rg \
  --plan anonimiza-plan \
  --name anonimiza-webapp \
  --runtime "PYTHON|3.9" \
  --deployment-local-git
```

Guarda la URL de Git remoto que se muestra.

---

## 6. Configurar variables de entorno (App Settings)

```bash
az webapp config appsettings set \
  --resource-group anonimiza-rg \
  --name anonimiza-webapp \
  --settings \
    AZURE_FORM_RECOGNIZER_ENDPOINT="https://anonimiza-form-recognizer.cognitiveservices.azure.com/" \
    AZURE_FORM_RECOGNIZER_KEY="<tu-form-recognizer-key>" \
    AZURE_TEXT_ANALYTICS_ENDPOINT="https://anonimiza-text-analytics.cognitiveservices.azure.com/" \
    AZURE_TEXT_ANALYTICS_KEY="<tu-text-analytics-key>"
```

---

## 7. Desplegar el código

1. Inicializa Git (si no está):

   ```bash
   git init
   git add .
   git commit -m "Primer commit PoC anonimización"
   ```
2. Añade el remoto de Azure:

   ```bash
   git remote add azure <URL-REMOTO-AZURE>
   ```
3. Empuja a Azure:

   ```bash
   git push azure main
   ```

---

## 8. Probar la aplicación

Visita:

```
https://anonimiza-webapp.azurewebsites.net
```

Sube un PDF y verifica extracción de texto y resaltado de PII.

---

## 9. Monitorización y logs

* Logs en tiempo real:

  ```bash
  az webapp log tail \
    --name anonimiza-webapp \
    --resource-group anonimiza-rg
  ```
* En el Portal: Web App → **Log Stream**, **Diagnóstico de errores**.

---

## 10. Mantenimiento y escalado

* Escala el plan si es necesario:

  ```bash
  az appservice plan update --resource-group anonimiza-rg --name anonimiza-plan --sku S2
  ```
* Gestiona secretos con **Azure Key Vault** y **Managed Identity**.
* Configura alertas de uso y coste en el Resource Group.
* Integración continua con GitHub Actions o Azure DevOps.

```
```
