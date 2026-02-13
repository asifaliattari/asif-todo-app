# 🚀 Deploy TaskFlow to Local Kubernetes

## Prerequisites

✅ Docker Desktop installed and running
✅ Kubernetes enabled in Docker Desktop
✅ kubectl CLI installed (comes with Docker Desktop)
✅ Docker images built (already done!)

---

## Step 1: Enable Kubernetes in Docker Desktop

**If not already enabled:**

1. Open **Docker Desktop**
2. Click **Settings** (gear icon)
3. Go to **Kubernetes** tab
4. Check **"Enable Kubernetes"**
5. Click **"Apply & Restart"**
6. Wait 2-3 minutes for green status

**Verify:**
```bash
kubectl cluster-info
kubectl get nodes
```

You should see:
```
NAME             STATUS   ROLES           AGE   VERSION
docker-desktop   Ready    control-plane   ...   v1.xx.x
```

---

## Step 2: Load Docker Images into Kubernetes

Since we built images with Docker Compose, they're already available to Kubernetes (Docker Desktop shares the same Docker daemon).

**Verify images exist:**
```bash
docker images | grep taskflow
```

Should show:
- `asif_todo_app_phase2-backend:latest`
- `asif_todo_app_phase2-frontend:latest`

---

## Step 3: Deploy to Kubernetes

### Option A: Deploy Everything at Once (Recommended)

```bash
# Navigate to k8s directory
cd k8s

# Apply all manifests in order
kubectl apply -f namespace.yaml
kubectl apply -f secret.yaml
kubectl apply -f configmap.yaml
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml
```

### Option B: Use Kustomize (Single Command)

```bash
cd k8s
kubectl apply -k .
```

---

## Step 4: Verify Deployment

### Check Namespace
```bash
kubectl get namespaces
```

Should show `taskflow` namespace.

### Check Pods
```bash
kubectl get pods -n taskflow
```

Expected output:
```
NAME                                READY   STATUS    RESTARTS   AGE
taskflow-backend-xxxxxxxxx-xxxxx    1/1     Running   0          1m
taskflow-backend-xxxxxxxxx-xxxxx    1/1     Running   0          1m
taskflow-frontend-xxxxxxxxx-xxxxx   1/1     Running   0          1m
taskflow-frontend-xxxxxxxxx-xxxxx   1/1     Running   0          1m
```

### Check Services
```bash
kubectl get services -n taskflow
```

Expected output:
```
NAME                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
taskflow-backend    ClusterIP   10.x.x.x        <none>        8000/TCP         1m
taskflow-frontend   NodePort    10.x.x.x        <none>        3000:30000/TCP   1m
```

### Watch Deployment Progress
```bash
kubectl get pods -n taskflow -w
```

Press Ctrl+C to stop watching.

---

## Step 5: Access the Application

### Frontend (Web UI)
```
http://localhost:30000
```

The frontend is exposed on NodePort 30000.

### Backend API
The backend is only accessible within the cluster (ClusterIP). The frontend connects to it internally.

To access backend from your machine (for testing):
```bash
kubectl port-forward -n taskflow service/taskflow-backend 8000:8000
```

Then access:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/api/health

---

## Step 6: View Logs

### Backend Logs
```bash
# All backend pods
kubectl logs -n taskflow -l app=taskflow-backend -f

# Specific pod
kubectl logs -n taskflow <pod-name> -f
```

### Frontend Logs
```bash
# All frontend pods
kubectl logs -n taskflow -l app=taskflow-frontend -f

# Specific pod
kubectl logs -n taskflow <pod-name> -f
```

---

## Useful Commands

### Get All Resources
```bash
kubectl get all -n taskflow
```

### Describe Pod (for troubleshooting)
```bash
kubectl describe pod <pod-name> -n taskflow
```

### Execute Command in Pod
```bash
kubectl exec -it <pod-name> -n taskflow -- /bin/sh
```

### View ConfigMap
```bash
kubectl get configmap taskflow-config -n taskflow -o yaml
```

### View Secrets (base64 encoded)
```bash
kubectl get secret taskflow-secrets -n taskflow -o yaml
```

### Scale Deployment
```bash
# Scale backend to 3 replicas
kubectl scale deployment taskflow-backend -n taskflow --replicas=3

# Scale frontend to 3 replicas
kubectl scale deployment taskflow-frontend -n taskflow --replicas=3
```

### Restart Deployment
```bash
kubectl rollout restart deployment taskflow-backend -n taskflow
kubectl rollout restart deployment taskflow-frontend -n taskflow
```

---

## Cleanup / Uninstall

### Delete All Resources
```bash
kubectl delete namespace taskflow
```

This removes everything (pods, services, configmaps, secrets).

### Or Delete Individually
```bash
kubectl delete -f frontend-service.yaml
kubectl delete -f frontend-deployment.yaml
kubectl delete -f backend-service.yaml
kubectl delete -f backend-deployment.yaml
kubectl delete -f configmap.yaml
kubectl delete -f secret.yaml
kubectl delete -f namespace.yaml
```

---

## Troubleshooting

### Pods Not Starting

**Check pod status:**
```bash
kubectl get pods -n taskflow
```

**Check pod events:**
```bash
kubectl describe pod <pod-name> -n taskflow
```

**Check logs:**
```bash
kubectl logs <pod-name> -n taskflow
```

### Common Issues

**1. ImagePullBackOff**
- Image doesn't exist locally
- Solution: Rebuild images with `docker-compose build`

**2. CrashLoopBackOff**
- Container is crashing after starting
- Check logs: `kubectl logs <pod-name> -n taskflow`
- Usually database connection or missing env vars

**3. Pending Status**
- Not enough resources
- Check events: `kubectl describe pod <pod-name> -n taskflow`

**4. Backend Health Check Failing**
- Database not accessible
- Check secret.yaml has correct DATABASE_URL
- Restart deployment: `kubectl rollout restart deployment taskflow-backend -n taskflow`

---

## Architecture Differences: Docker Compose vs Kubernetes

### Docker Compose:
- Single machine
- 1 replica per service
- Port mapping: localhost:3000, localhost:8000
- docker-compose.yml manages everything

### Kubernetes:
- Can scale across multiple nodes (but we're using 1 node locally)
- 2 replicas per service (high availability)
- NodePort: localhost:30000 (frontend)
- ClusterIP: internal only (backend)
- Multiple YAML files for different resource types
- Auto-restarts, health checks, load balancing

---

## Monitoring

### Resource Usage
```bash
kubectl top pods -n taskflow
kubectl top nodes
```

### Events
```bash
kubectl get events -n taskflow --sort-by='.lastTimestamp'
```

### Dashboard (Optional)
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
kubectl proxy
```

Then access: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/

---

## Next Steps After Deployment

1. **Test the Application**
   - Open http://localhost:30000
   - Create account, add tasks
   - Test AI chatbot

2. **Verify High Availability**
   ```bash
   # Delete one backend pod
   kubectl delete pod <backend-pod-name> -n taskflow

   # Kubernetes will automatically create a new one
   kubectl get pods -n taskflow -w
   ```

3. **Scale Up/Down**
   ```bash
   # Scale to 3 replicas
   kubectl scale deployment taskflow-backend -n taskflow --replicas=3

   # Watch the new pods come up
   kubectl get pods -n taskflow -w
   ```

4. **Update Application**
   ```bash
   # Rebuild Docker image
   docker-compose build backend

   # Restart deployment to use new image
   kubectl rollout restart deployment taskflow-backend -n taskflow
   ```

---

## Video Demonstration Script

### Show Kubernetes Deployment (3 minutes)

1. **Show cluster info:**
   ```bash
   kubectl cluster-info
   kubectl get nodes
   ```

2. **Show all resources:**
   ```bash
   kubectl get all -n taskflow
   ```

3. **Show 2 replicas running:**
   ```bash
   kubectl get pods -n taskflow
   ```

4. **Access frontend:**
   - Open http://localhost:30000
   - Show it's the same app, now on Kubernetes!

5. **Show pod logs:**
   ```bash
   kubectl logs -n taskflow -l app=taskflow-backend --tail=20
   ```

6. **Demonstrate high availability:**
   ```bash
   # Delete a pod
   kubectl delete pod <pod-name> -n taskflow

   # Show Kubernetes auto-recreates it
   kubectl get pods -n taskflow -w
   ```

7. **Show scaling:**
   ```bash
   kubectl scale deployment taskflow-backend -n taskflow --replicas=4
   kubectl get pods -n taskflow
   ```

---

## ✅ Deployment Checklist

- [ ] Kubernetes enabled in Docker Desktop
- [ ] `kubectl cluster-info` working
- [ ] Docker images built and available
- [ ] secret.yaml created with real credentials
- [ ] All manifests applied successfully
- [ ] All pods showing "Running" status
- [ ] Frontend accessible at http://localhost:30000
- [ ] Backend health check passing
- [ ] Application fully functional

---

**Your TaskFlow app is now running on Kubernetes! 🎉**

This gives you:
- ✅ Container orchestration
- ✅ Auto-healing (crashed pods restart automatically)
- ✅ Load balancing across replicas
- ✅ Resource management
- ✅ Production-like environment locally

**Ready for Phase 5: Cloud Deployment!** ☁️
