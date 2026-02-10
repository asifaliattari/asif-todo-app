# TaskFlow - Kubernetes Deployment

**Author**: Asif Ali AstolixGen
**Phase**: IV - Container Orchestration

---

## Overview

This directory contains all Kubernetes manifests to deploy TaskFlow to a local Minikube cluster.

## Architecture

- **Frontend**: Next.js app (3 replicas)
- **Backend**: FastAPI app (2 replicas)
- **Database**: External Neon PostgreSQL
- **Load Balancer**: Kubernetes Services + Ingress

---

## Prerequisites

### 1. Install Required Tools

**Docker Desktop**:
- Download: https://www.docker.com/products/docker-desktop
- Verify: `docker --version`

**Minikube**:
```bash
# Windows (with Chocolatey)
choco install minikube

# macOS
brew install minikube

# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

**kubectl**:
```bash
# Windows
choco install kubernetes-cli

# macOS
brew install kubectl

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

### 2. Start Minikube

```bash
# Start Minikube with adequate resources
minikube start --cpus=4 --memory=4096mb --driver=docker

# Enable Ingress addon
minikube addons enable ingress

# Verify
kubectl get nodes
```

---

## Quick Deploy

### 1. Create Secrets File

```bash
cp k8s/secrets.yaml.template k8s/secrets.yaml
```

Edit `k8s/secrets.yaml` and add your actual secrets:
- DATABASE_URL (from Neon console)
- BETTER_AUTH_SECRET (generate with `openssl rand -base64 32`)
- OPENAI_API_KEY (from OpenAI platform)

⚠️ **NEVER commit secrets.yaml to git!**

### 2. Run Deployment Script

```bash
chmod +x k8s/deploy.sh
./k8s/deploy.sh
```

The script will:
1. Build Docker images
2. Load images into Minikube
3. Create namespace
4. Apply ConfigMaps and Secrets
5. Deploy backend and frontend
6. Create Ingress
7. Wait for deployments to be ready

### 3. Access the Application

Add to your `/etc/hosts` (or `C:\Windows\System32\drivers\etc\hosts` on Windows):

```
<minikube-ip> taskflow.local
```

Get Minikube IP:
```bash
minikube ip
```

Then open: **http://taskflow.local**

---

## Manual Deployment

If you prefer step-by-step deployment:

### 1. Build Docker Images

```bash
# Backend
docker build -t taskflow-backend:latest ./backend

# Frontend  
docker build -t taskflow-frontend:latest ./frontend
```

### 2. Load Images into Minikube

```bash
minikube image load taskflow-backend:latest
minikube image load taskflow-frontend:latest
```

### 3. Apply Manifests

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secrets (edit first!)
kubectl apply -f k8s/secrets.yaml

# Create ConfigMap
kubectl apply -f k8s/configmap.yaml

# Deploy backend
kubectl apply -f k8s/backend/

# Deploy frontend
kubectl apply -f k8s/frontend/

# Create Ingress
kubectl apply -f k8s/ingress.yaml
```

### 4. Verify Deployment

```bash
# Check pods
kubectl get pods -n taskflow

# Check services
kubectl get svc -n taskflow

# Check ingress
kubectl get ingress -n taskflow
```

---

## Useful Commands

### View Logs

```bash
# Backend logs
kubectl logs -f deployment/taskflow-backend -n taskflow

# Frontend logs
kubectl logs -f deployment/taskflow-frontend -n taskflow

# Specific pod
kubectl logs -f <pod-name> -n taskflow
```

### Scale Deployments

```bash
# Scale backend to 3 replicas
kubectl scale deployment taskflow-backend --replicas=3 -n taskflow

# Scale frontend to 5 replicas
kubectl scale deployment taskflow-frontend --replicas=5 -n taskflow
```

### Update Deployment

```bash
# After rebuilding images
minikube image load taskflow-backend:latest
kubectl rollout restart deployment/taskflow-backend -n taskflow

# Check rollout status
kubectl rollout status deployment/taskflow-backend -n taskflow
```

### Debug

```bash
# Describe pod
kubectl describe pod <pod-name> -n taskflow

# Shell into container
kubectl exec -it <pod-name> -n taskflow -- /bin/sh

# Port forward (for direct access)
kubectl port-forward svc/taskflow-backend 8000:8000 -n taskflow
kubectl port-forward svc/taskflow-frontend 3000:3000 -n taskflow
```

### Clean Up

```bash
# Delete all resources
kubectl delete namespace taskflow

# Or delete specific resources
kubectl delete -f k8s/
```

---

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n taskflow

# Describe pod for events
kubectl describe pod <pod-name> -n taskflow

# Check logs
kubectl logs <pod-name> -n taskflow
```

**Common Issues**:
- Image pull errors: Make sure images are loaded into Minikube
- ConfigMap/Secret missing: Apply them before deployments
- Resource limits: Adjust in deployment.yaml

### Ingress Not Working

```bash
# Check Ingress status
kubectl get ingress -n taskflow

# Verify Ingress controller is running
kubectl get pods -n ingress-nginx
```

**Fix**:
```bash
# Enable Ingress addon
minikube addons enable ingress

# Check Minikube IP
minikube ip

# Update /etc/hosts with correct IP
```

### Database Connection Errors

- Verify DATABASE_URL in secrets.yaml
- Check Neon database is accessible
- Ensure SSL mode is included in URL: `?sslmode=require`

### Pod Crashes (CrashLoopBackOff)

```bash
# Check logs
kubectl logs <pod-name> -n taskflow --previous

# Common causes:
# - Missing environment variables
# - Database connection failed
# - Application error on startup
```

---

## Production Considerations

For production deployment (not Minikube):

1. **Image Registry**: Push images to Docker Hub or private registry
2. **Persistent Storage**: Use PersistentVolumeClaims for stateful data
3. **Database**: Consider managed PostgreSQL or deploy PostgreSQL in cluster
4. **Secrets Management**: Use external secrets manager (HashiCorp Vault, AWS Secrets Manager)
5. **Monitoring**: Add Prometheus + Grafana
6. **Logging**: Use EFK stack (Elasticsearch, Fluentd, Kibana)
7. **Auto-scaling**: Configure HorizontalPodAutoscaler
8. **Resource Limits**: Fine-tune based on actual usage
9. **Network Policies**: Restrict pod-to-pod communication
10. **TLS**: Use cert-manager for HTTPS

---

## Files Reference

```
k8s/
├── namespace.yaml          # Creates taskflow namespace
├── configmap.yaml          # Non-sensitive configuration
├── secrets.yaml.template   # Template for secrets (copy to secrets.yaml)
├── secrets.yaml           # Actual secrets (git-ignored)
├── backend/
│   ├── deployment.yaml    # Backend deployment (2 replicas)
│   └── service.yaml       # Backend service (ClusterIP)
├── frontend/
│   ├── deployment.yaml    # Frontend deployment (3 replicas)
│   └── service.yaml       # Frontend service (ClusterIP)
├── ingress.yaml           # Ingress routing rules
├── deploy.sh              # Automated deployment script
└── README.md              # This file
```

---

## Next Steps

- Add HorizontalPodAutoscaler for auto-scaling
- Implement health check endpoints
- Add Prometheus metrics
- Set up CI/CD pipeline for automated deployments
- Configure network policies for security

---

**Deployed and ready!** 🚀

*Created by Asif Ali AstolixGen for GIAIC Hackathon 2026*
