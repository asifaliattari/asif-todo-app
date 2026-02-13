@echo off
REM TaskFlow - Deploy to Local Kubernetes
REM Created by Asif Ali AstolixGen

echo ========================================
echo  TaskFlow - Kubernetes Deployment
echo ========================================
echo.

REM Check if kubectl is available
kubectl version --client >nul 2>&1
if errorlevel 1 (
    echo [ERROR] kubectl not found!
    echo Please install kubectl or enable Kubernetes in Docker Desktop.
    pause
    exit /b 1
)

REM Check if cluster is running
echo [1/8] Checking Kubernetes cluster...
kubectl cluster-info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Cannot connect to Kubernetes cluster!
    echo.
    echo Please enable Kubernetes in Docker Desktop:
    echo 1. Open Docker Desktop
    echo 2. Go to Settings ^> Kubernetes
    echo 3. Check "Enable Kubernetes"
    echo 4. Click "Apply & Restart"
    echo 5. Wait 2-3 minutes
    pause
    exit /b 1
)
echo [OK] Cluster is running

REM Create namespace
echo.
echo [2/8] Creating namespace...
kubectl apply -f namespace.yaml
if errorlevel 1 (
    echo [ERROR] Failed to create namespace
    pause
    exit /b 1
)

REM Create secrets
echo.
echo [3/8] Creating secrets...
kubectl apply -f secret.yaml
if errorlevel 1 (
    echo [ERROR] Failed to create secrets
    pause
    exit /b 1
)

REM Create configmap
echo.
echo [4/8] Creating configmap...
kubectl apply -f configmap.yaml
if errorlevel 1 (
    echo [ERROR] Failed to create configmap
    pause
    exit /b 1
)

REM Deploy backend
echo.
echo [5/8] Deploying backend...
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml
if errorlevel 1 (
    echo [ERROR] Failed to deploy backend
    pause
    exit /b 1
)

REM Deploy frontend
echo.
echo [6/8] Deploying frontend...
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml
if errorlevel 1 (
    echo [ERROR] Failed to deploy frontend
    pause
    exit /b 1
)

REM Wait for pods
echo.
echo [7/8] Waiting for pods to start (this may take 30-60 seconds)...
timeout /t 10 /nobreak >nul
kubectl wait --for=condition=ready pod -l app=taskflow-backend -n taskflow --timeout=120s
kubectl wait --for=condition=ready pod -l app=taskflow-frontend -n taskflow --timeout=120s

REM Show status
echo.
echo [8/8] Deployment complete!
echo.
echo ========================================
echo  Deployment Status
echo ========================================
kubectl get all -n taskflow

echo.
echo ========================================
echo  Access Your Application
echo ========================================
echo.
echo  Frontend:  http://localhost:30000
echo  Backend:   kubectl port-forward -n taskflow service/taskflow-backend 8000:8000
echo.
echo ========================================
echo  Useful Commands
echo ========================================
echo.
echo  View pods:     kubectl get pods -n taskflow
echo  View logs:     kubectl logs -n taskflow -l app=taskflow-backend
echo  Scale up:      kubectl scale deployment taskflow-backend -n taskflow --replicas=3
echo  Delete all:    kubectl delete namespace taskflow
echo.
echo Deployment successful! Open http://localhost:30000 in your browser.
echo.
pause
