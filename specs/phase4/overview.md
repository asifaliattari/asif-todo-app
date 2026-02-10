# Phase IV - Kubernetes Deployment

**Author**: Asif Ali AstolixGen
**Phase**: IV - Container Orchestration with Kubernetes
**Goal**: Deploy TaskFlow to local Kubernetes cluster using Minikube

---

## Overview

Transform TaskFlow into a cloud-native application running on Kubernetes, demonstrating modern container orchestration and deployment practices.

## Objectives

1. **Containerize** frontend and backend applications
2. **Deploy** to local Kubernetes cluster (Minikube)
3. **Orchestrate** services with Kubernetes manifests
4. **Manage** configuration and secrets
5. **Expose** services via Ingress

---

## Architecture

```
┌─────────────────────────────────────────────┐
│           Minikube Cluster                  │
│                                             │
│  ┌────────────┐         ┌────────────┐    │
│  │  Ingress   │────────▶│  Frontend  │    │
│  │ Controller │         │   Service  │    │
│  └────────────┘         └─────┬──────┘    │
│         │                      │            │
│         │              ┌───────▼───────┐   │
│         │              │   Frontend    │   │
│         │              │  Deployment   │   │
│         │              │  (3 replicas) │   │
│         │              └───────────────┘   │
│         │                                   │
│         │              ┌────────────┐      │
│         └─────────────▶│  Backend   │      │
│                        │   Service  │      │
│                        └─────┬──────┘      │
│                              │              │
│                      ┌───────▼───────┐     │
│                      │    Backend    │     │
│                      │   Deployment  │     │
│                      │  (2 replicas) │     │
│                      └───────┬───────┘     │
│                              │              │
│                      ┌───────▼───────┐     │
│                      │   ConfigMap   │     │
│                      │   + Secrets   │     │
│                      └───────────────┘     │
│                                             │
│  External Database: Neon PostgreSQL        │
│  (Accessed via public endpoint)            │
└─────────────────────────────────────────────┘
```

---

## Components

### 1. Frontend Deployment
- **Image**: `taskflow-frontend:latest`
- **Replicas**: 3 (for high availability)
- **Port**: 3000
- **Environment**: ConfigMap for API URL
- **Resources**:
  - CPU: 100m (request), 200m (limit)
  - Memory: 128Mi (request), 256Mi (limit)

### 2. Backend Deployment
- **Image**: `taskflow-backend:latest`
- **Replicas**: 2
- **Port**: 8000
- **Environment**: Secrets for DATABASE_URL, API keys
- **Resources**:
  - CPU: 200m (request), 500m (limit)
  - Memory: 256Mi (request), 512Mi (limit)

### 3. Services
- **Frontend Service**: ClusterIP, exposes port 3000
- **Backend Service**: ClusterIP, exposes port 8000

### 4. Ingress
- **Host**: taskflow.local
- **Routes**:
  - `/` → Frontend Service
  - `/api/*` → Backend Service

### 5. Configuration
- **ConfigMap**: Non-sensitive configuration (API URLs, app settings)
- **Secrets**: Sensitive data (DATABASE_URL, JWT secrets, API keys)

---

## Prerequisites

- Docker Desktop installed
- Minikube installed
- kubectl installed
- Helm (optional, for easier deployment)

---

## Success Criteria

- [x] Frontend and backend Docker images built
- [x] All Kubernetes manifests created
- [x] Application deployed to Minikube
- [x] Services accessible via Ingress
- [x] Multiple replicas running (load balancing)
- [x] ConfigMaps and Secrets properly configured
- [x] Rolling updates work smoothly
- [x] Logs accessible via kubectl

---

## Files Structure

```
k8s/
├── namespace.yaml
├── configmap.yaml
├── secrets.yaml
├── frontend/
│   ├── deployment.yaml
│   └── service.yaml
├── backend/
│   ├── deployment.yaml
│   └── service.yaml
├── ingress.yaml
└── README.md
```

---

## Deployment Workflow

1. Build Docker images
2. Load images into Minikube
3. Create namespace
4. Apply ConfigMaps and Secrets
5. Deploy backend
6. Deploy frontend
7. Create Ingress
8. Access via browser

---

## References

- Kubernetes Docs: https://kubernetes.io/docs/
- Minikube: https://minikube.sigs.k8s.io/docs/
- Docker: https://docs.docker.com/

---

**Next**: See `kubernetes-deployment.md` for detailed implementation
