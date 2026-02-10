#!/bin/bash

# TaskFlow Kubernetes Deployment Script
# Author: Asif Ali AstolixGen

set -e

echo "🚀 TaskFlow Kubernetes Deployment"
echo "=================================="

# Colors
GREEN='\033[0.32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Step 1: Build Docker images
echo -e "\n${YELLOW}Step 1: Building Docker images...${NC}"
echo "Building backend image..."
docker build -t taskflow-backend:latest ./backend

echo "Building frontend image..."
docker build -t taskflow-frontend:latest ./frontend

# Step 2: Load images into Minikube
echo -e "\n${YELLOW}Step 2: Loading images into Minikube...${NC}"
minikube image load taskflow-backend:latest
minikube image load taskflow-frontend:latest

# Step 3: Create namespace
echo -e "\n${YELLOW}Step 3: Creating namespace...${NC}"
kubectl apply -f k8s/namespace.yaml

# Step 4: Create secrets (you need to edit secrets.yaml first)
echo -e "\n${YELLOW}Step 4: Creating secrets...${NC}"
if [ -f k8s/secrets.yaml ]; then
    kubectl apply -f k8s/secrets.yaml
else
    echo "⚠️  Please create k8s/secrets.yaml from secrets.yaml.template"
    echo "   and add your actual secrets!"
    exit 1
fi

# Step 5: Create ConfigMap
echo -e "\n${YELLOW}Step 5: Creating ConfigMap...${NC}"
kubectl apply -f k8s/configmap.yaml

# Step 6: Deploy backend
echo -e "\n${YELLOW}Step 6: Deploying backend...${NC}"
kubectl apply -f k8s/backend/

# Step 7: Deploy frontend
echo -e "\n${YELLOW}Step 7: Deploying frontend...${NC}"
kubectl apply -f k8s/frontend/

# Step 8: Create Ingress
echo -e "\n${YELLOW}Step 8: Creating Ingress...${NC}"
kubectl apply -f k8s/ingress.yaml

# Step 9: Wait for deployments
echo -e "\n${YELLOW}Step 9: Waiting for deployments...${NC}"
kubectl wait --for=condition=available --timeout=300s deployment/taskflow-backend -n taskflow
kubectl wait --for=condition=available --timeout=300s deployment/taskflow-frontend -n taskflow

# Step 10: Display status
echo -e "\n${GREEN}✅ Deployment complete!${NC}\n"
echo "View pods:"
echo "  kubectl get pods -n taskflow"
echo ""
echo "View services:"
echo "  kubectl get svc -n taskflow"
echo ""
echo "Access application:"
echo "  Add to /etc/hosts: $(minikube ip) taskflow.local"
echo "  Open: http://taskflow.local"
echo ""
echo "View logs:"
echo "  kubectl logs -f deployment/taskflow-backend -n taskflow"
echo "  kubectl logs -f deployment/taskflow-frontend -n taskflow"
