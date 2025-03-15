# Azure CLI Cheat Sheet

A handy reference for checking resources, troubleshooting deployments, and manually creating Azure resources.

---

## **General Azure Subscription & Tenant Info**

### **Check active subscription and tenant ID**
```sh
az account show --query "{SubscriptionId:id, TenantId:tenantId}" --output json
```

### **List all available subscriptions**
```sh
az account list --output table
```

### **Set the correct subscription**
```sh
az account set --subscription <SUBSCRIPTION_ID>
```

---

## **Resource Group Management**

### **List all resource groups**
```sh
az group list --output table
```

### **Delete a specific resource group**
```sh
az group delete --name <RESOURCE_GROUP> --yes --no-wait
```

### **Delete ALL resource groups** **(Irreversible)**
```sh
az group list --query "[].name" --output tsv | xargs -I {} az group delete --name {} --yes --no-wait
```

---

## **Checking Deployments & Errors**

### **List all deployments in a resource group**
```sh
az deployment group list --resource-group <RESOURCE_GROUP> --query "[].{Name:name, Status:properties.provisioningState}" --output table
```

### **Show details of a failed deployment**
```sh
az deployment group show --resource-group <RESOURCE_GROUP> --name <DEPLOYMENT_NAME> --query "properties.error"
```

### **Check which resources failed in a deployment**
```sh
az deployment operation group list --resource-group <RESOURCE_GROUP> --name <DEPLOYMENT_NAME> --query "[].{Resource:properties.targetResource.id, Status:properties.statusMessage}" --output table
```

---

## **Checking & Managing Resources**

### **List all resources in a resource group**
```sh
az resource list --resource-group <RESOURCE_GROUP> --output table
```

### **Delete a specific resource**
```sh
az resource delete --name <RESOURCE_NAME> --resource-group <RESOURCE_GROUP>
```

---

## **Key Vault Management**

### **Check if a Key Vault exists**
```sh
az keyvault show --name <KEYVAULT_NAME>
```

### **List deleted (soft-deleted) Key Vaults**
```sh
az keyvault list-deleted --output table
```

### **Permanently delete (purge) a Key Vault** **(Irreversible)**
```sh
az keyvault purge --name <KEYVAULT_NAME> --location <LOCATION>
```

### **Manually create a Key Vault**
```sh
az keyvault create \
  --name <KEYVAULT_NAME> \
  --resource-group <RESOURCE_GROUP> \
  --location <LOCATION> \
  --enabled-for-deployment true \
  --enabled-for-template-deployment true
```

---

## **Managed Identity Management**

### **Check if a Managed Identity exists**
```sh
az identity show --name <IDENTITY_NAME> --resource-group <RESOURCE_GROUP>
```

### **Manually create a Managed Identity**
```sh
az identity create --name <IDENTITY_NAME> --resource-group <RESOURCE_GROUP>
```

---

## **Checking App Services**

### **List all Web Apps in a resource group**
```sh
az webapp list --resource-group <RESOURCE_GROUP> --output table
```

### **Delete a Web App**
```sh
az webapp delete --name <WEBAPP_NAME> --resource-group <RESOURCE_GROUP>
```

---

## **Checking Role Assignments**

### **Check role assignments for a Service Principal**
```sh
az role assignment list --assignee <CLIENT_ID> --output table
```

### **Manually assign a Contributor role**
```sh
az role assignment create --assignee <CLIENT_ID> --role Contributor --scope /subscriptions/<SUBSCRIPTION_ID>
```

---

## **Service Principal Management**

### **Check if a Service Principal exists**
```sh
az ad sp list --display-name "<SERVICE_PRINCIPAL_NAME>" --output table
```

### **Manually create a Service Principal**
```sh
az ad sp create-for-rbac --name "<SERVICE_PRINCIPAL_NAME>" --role contributor --scopes /subscriptions/<SUBSCRIPTION_ID>
```

### **Delete a Service Principal**
```sh
az ad sp delete --id <CLIENT_ID>
```

---

## **Deployment Commands**

### **Run an ARM template deployment**
```sh
az deployment group create \
  --resource-group <RESOURCE_GROUP> \
  --template-file <TEMPLATE_PATH> \
  --parameters @<PARAMETERS_FILE>
```

### **Run the deployment with debugging**
```sh
az deployment group create \
  --resource-group <RESOURCE_GROUP> \
  --template-file <TEMPLATE_PATH> \
  --parameters @<PARAMETERS_FILE> \
  --debug
```

---

## **Logs**

### **Download diagnostic logs**
```sh
az webapp log download --resource-group <RESOURCE_GROUP> --name <APP_NAME>
```

### **View logs in real-time**
```sh
az webapp log tail --resource-group <RESOURCE_GROUP> --name <APP_NAME>
```

---

## **Final Tip: Check Logs in Azure Portal**
If CLI debugging doesn’t show enough info:
1. Go to **Azure Portal** → **Resource Groups** → Select your **resource group**.
2. Click **Deployments**.
3. Find the **failed deployment**, click on it, and read the error details.

---

