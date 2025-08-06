         ___        ______     ____ _                 _  ___  
        / \ \      / / ___|   / ___| | ___  _   _  __| |/ _ \ 
       / _ \ \ /\ / /\___ \  | |   | |/ _ \| | | |/ _` | (_) |
      / ___ \ V  V /  ___) | | |___| | (_) | |_| | (_| |\__, |
     /_/   \_\_/\_/  |____/   \____|_|\___/ \__,_|\__,_|  /_/ 
 ----------------------------------------------------------------- 


# Group 18 – CLO835 Final Project  
**Slogan:** _"Together, we got this!!!"_

## 📌 Project Overview

This project demonstrates a **2-tier web application** deployed to a **managed Kubernetes cluster (Amazon EKS)** using **CI/CD automation** via GitHub Actions. The application consists of:

- **Frontend:** Flask app pulling a background image from **private S3**.
- **Backend:** MySQL database accessed via internal ClusterIP.
- **CI/CD:** Docker image built and pushed to **Amazon ECR** on GitHub push.
- **Secrets & Config:** Managed via Kubernetes Secrets and ConfigMaps.
- **Storage:** PVCs ensure persistent storage for MySQL.

---

## 📁 Project Structure

├── .github/workflows/
│   └── docker-build.yml       # GitHub Actions workflow
├
│── configmap-background.yaml
│── configmap-team.yaml
│── aws-secret.yaml
│── mysql-secret.yaml
│── ecr-pull-secret.sh
│── pvc.yaml
│── serviceaccount.yaml
│── role.yaml
│── rolebinding.yaml
│── mysql-deployment.yaml
│── flask-deployment.yaml
│── mysql-service.yaml
│── flask-service.yaml
├── Dockerfile
├── app/
│   ├── static/
│   │   └── background.jpg (populated at runtime from S3)
│   ├── templates/
│   └── app.py
└── README.md

 Deployment Steps
1. Configure AWS Credentials
Disable managed credentials in Cloud9:
/usr/local/bin/aws cloud9 update-environment --environment-id $C9_PID --managed-credentials-action DISABLE
Then manually create your AWS credentials file:
vi ~/.aws/credentials
# Add access key, secret key, and session token
Confirm:
cat ~/.aws/credentials

2.  Install Dependencies
sudo yum -y install jq gettext

3.  Create the EKS Cluster
eksctl create cluster -f eks_config.yaml

4.  Create Secrets and ConfigMaps
kubectl apply -f k8s/aws-secret.yaml
kubectl apply -f k8s/mysql-secret.yaml
kubectl apply -f k8s/configmap-background.yaml
kubectl apply -f k8s/configmap-team.yaml

5.  Create ECR Pull Secret
aws ecr get-login-password --region us-east-1 | \
kubectl create secret docker-registry ecr-pull-secret \
  --namespace fp \
  --docker-server=537380924761.dkr.ecr.us-east-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password)
   
6. 📦 Create RBAC, PVC, and Service Account
kubectl apply -f serviceaccount.yaml
kubectl apply -f role.yaml
kubectl apply -f rolebinding.yaml
kubectl apply -f pvc.yaml

7. 🧱 Deploy MySQL and Flask App
kubectl apply -f k8s/mysql-deployment.yaml
kubectl apply -f k8s/mysql-service.yaml

kubectl apply -f k8s/flask-deployment.yaml
kubectl apply -f k8s/flask-service.yaml

8. 🌐 Access the Web App
Find the NodePort or LoadBalancer service exposed and test via browser or curl:

kubectl get svc -n fp

