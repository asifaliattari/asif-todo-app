# Kubernetes Setup Guide - TaskFlow Phase 4

**Created by**: Asif Ali AstolixGen  
**Hackathon**: GIAIC Hackathon 2026 - Phase 4

## Prerequisites

- Docker Desktop installed and running
- Minikube installed
- kubectl installed

## Step-by-Step Deployment

### 1. Install Minikube

**Windows (using Chocolatey):**
```bash
choco install minikube
```

**Or download installer:**
https://minikube.sigs.k8s.io/docs/start/

**Verify installation:**
```bash
minikube version
```

### 2. Start Minikube

```bash
minikube start --driver=docker
```

**Check status:**
```bash
minikube status
kubectl cluster-info
```

### 3. Build Docker Images for Minikube

**Important**: Point your Docker CLI to Minikube's Docker daemon:
```bash
# Windows PowerShell
minikube docker-env | Invoke-Expression

# Or use this command to see the variables
minikube docker-env
```

**Build images:**
```bash
# Backend
cd backend
docker build -t taskflow-backend:latest .

# Frontend
cd ../frontend
docker build -t taskflow-frontend:latest .
```

**Verify images:**
```bash
docker images | grep taskflow
```

### 4. Create Kubernetes Secret

**Copy the example and fill in your values:**
```bash
cd k8s
cp secret.yaml.example secret.yaml
```

**Edit secret.yaml with your actual credentials:**
- DATABASE_URL (Neon PostgreSQL)
- SECRET_KEY
- OPENAI_API_KEY
- SENDGRID_API_KEY
- SENDER_EMAIL
- ADMIN_EMAIL

### 5. Deploy to Kubernetes

**Apply all manifests:**
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
```

**Or use Kustomize:**
```bash
kubectl apply -k k8s/
```

### 6. Verify Deployment

**Check pods:**
```bash
kubectl get pods -n taskflow
```

**Check services:**
```bash
kubectl get services -n taskflow
```

**Check deployments:**
```bash
kubectl get deployments -n taskflow
```

**View logs:**
```bash
# Backend logs
kubectl logs -n taskflow -l app=backend -f

# Frontend logs
kubectl logs -n taskflow -l app=frontend -f
```

### 7. Access the Application

**Get Minikube IP:**
```bash
minikube ip
```

**Access frontend:**
```bash
minikube service frontend-service -n taskflow
```

Or manually: `http://<minikube-ip>:30000`

**Port forwarding (alternative):**
```bash
# Frontend
kubectl port-forward -n taskflow service/frontend-service 3000:3000

# Backend
kubectl port-forward -n taskflow service/backend-service 8000:8000
```

Then access:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## Kubernetes Commands Reference

### Pod Management

```bash
# List all pods
kubectl get pods -n taskflow

# Describe a pod
kubectl describe pod <pod-name> -n taskflow

# Get pod logs
kubectl logs <pod-name> -n taskflow

# Execute command in pod
kubectl exec -it <pod-name> -n taskflow -- /bin/bash
```

### Scaling

```bash
# Scale backend
kubectl scale deployment backend-deployment --replicas=3 -n taskflow

# Scale frontend
kubectl scale deployment frontend-deployment --replicas=3 -n taskflow
```

### Updates

```bash
# Update image
kubectl set image deployment/backend-deployment backend=taskflow-backend:v2 -n taskflow

# Rollout status
kubectl rollout status deployment/backend-deployment -n taskflow

# Rollback
kubectl rollout undo deployment/backend-deployment -n taskflow
```

### Resource Monitoring

```bash
# Resource usage
kubectl top nodes
kubectl top pods -n taskflow

# Describe resources
kubectl describe deployment backend-deployment -n taskflow
kubectl describe service backend-service -n taskflow
```

### Cleanup

```bash
# Delete all resources
kubectl delete namespace taskflow

# Or delete individually
kubectl delete -k k8s/
```

## Troubleshooting

### Pods Not Starting

**Check pod status:**
```bash
kubectl get pods -n taskflow
kubectl describe pod <pod-name> -n taskflow
```

**Common issues:**
- Image not found: Rebuild images in Minikube's Docker
- Secret not found: Apply secret.yaml first
- ConfigMap not found: Apply configmap.yaml first

### Image Pull Errors

**Solution:** Make sure you built images in Minikube's Docker daemon:
```bash
minikube docker-env | Invoke-Expression
docker images | grep taskflow
```

### Service Not Accessible

**Check service:**
```bash
kubectl get svc -n taskflow
minikube service list
```

**Access via Minikube:**
```bash
minikube service frontend-service -n taskflow --url
```

### Database Connection Issues

**Check secret:**
```bash
kubectl get secret taskflow-secrets -n taskflow -o yaml
```

**View logs:**
```bash
kubectl logs -n taskflow -l app=backend
```

## Architecture Diagram

```
┌─────────────────────────────────────────┐
│          Minikube Cluster               │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │      Namespace: taskflow          │ │
│  │                                   │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │  Frontend (2 replicas)      │ │ │
│  │  │  Port: 3000                 │ │ │
│  │  │  NodePort: 30000            │ │ │
│  │  └─────────────────────────────┘ │ │
│  │              ↓                    │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │  Backend (2 replicas)       │ │ │
│  │  │  Port: 8000                 │ │ │
│  │  │  ClusterIP                  │ │ │
│  │  └─────────────────────────────┘ │ │
│  │              ↓                    │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │  ConfigMap & Secrets        │ │ │
│  │  └─────────────────────────────┘ │ │
│  └───────────────────────────────────┘ │
│                 ↓                       │
└─────────────────────────────────────────┘
                  ↓
    External: Neon PostgreSQL
```

## Resource Specifications

### Backend Deployment
- **Replicas**: 2
- **Resources**: 
  - Requests: 256Mi RAM, 0.25 CPU
  - Limits: 512Mi RAM, 0.5 CPU
- **Health Checks**: Liveness & Readiness probes on /health

### Frontend Deployment
- **Replicas**: 2
- **Resources**:
  - Requests: 256Mi RAM, 0.25 CPU
  - Limits: 512Mi RAM, 0.5 CPU
- **Health Checks**: Liveness & Readiness probes on /

## Next Steps

1. ✅ Deploy to Minikube successfully
2. ⏳ Test all features work in Kubernetes
3. ⏳ Document deployment process
4. ⏳ Create demo video
5. ⏳ Move to Phase 5 (Cloud deployment with Kafka/Dapr)

---

**Need Help?**
- Minikube Docs: https://minikube.sigs.k8s.io/docs/
- Kubectl Docs: https://kubernetes.io/docs/reference/kubectl/
- Kubernetes Tutorials: https://kubernetes.io/docs/tutorials/
