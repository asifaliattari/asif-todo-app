# How to Use Secrets for Deployment

## ⚠️ IMPORTANT: Never commit secret.yaml to Git!

## For Local/Minikube Deployment:

### Step 1: Create secret.yaml from template
```bash
cd k8s
cp secret.yaml.example secret.yaml
```

### Step 2: Edit secret.yaml with your real values

Replace placeholder values with your actual credentials:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: taskflow-secrets
  namespace: taskflow
type: Opaque
stringData:
  # Get these from your HuggingFace Spaces environment variables
  DATABASE_URL: "your-neon-postgresql-url"
  SECRET_KEY: "your-jwt-secret"
  OPENAI_API_KEY: "your-openai-key"
  SENDGRID_API_KEY: "your-sendgrid-key"
  SENDER_EMAIL: "your-sender-email"
  ADMIN_EMAIL: "your-admin-email"
```

### Step 3: Deploy to Kubernetes
```bash
kubectl apply -f secret.yaml
kubectl apply -k .
```

### Step 4: Verify secrets are created
```bash
kubectl get secrets -n taskflow
kubectl describe secret taskflow-secrets -n taskflow
```

## For Production Deployment:

### Option 1: Use kubectl create secret
```bash
kubectl create secret generic taskflow-secrets \
  --from-literal=DATABASE_URL="your-url" \
  --from-literal=SECRET_KEY="your-key" \
  --from-literal=OPENAI_API_KEY="your-key" \
  --from-literal=SENDGRID_API_KEY="your-key" \
  --from-literal=SENDER_EMAIL="your-email" \
  --from-literal=ADMIN_EMAIL="your-email" \
  --namespace=taskflow
```

### Option 2: Use environment file
```bash
kubectl create secret generic taskflow-secrets \
  --from-env-file=../backend/.env \
  --namespace=taskflow
```

### Option 3: Use sealed-secrets (GitOps)
For production, use encrypted secrets that CAN be committed:
- https://github.com/bitnami-labs/sealed-secrets

## Security Best Practices:

✅ DO:
- Use secret.yaml.example as template
- Create secret.yaml locally (git-ignored)
- Use environment variables in production
- Rotate secrets regularly
- Use RBAC to limit secret access

❌ DON'T:
- Commit secret.yaml to Git
- Share secrets in Slack/email
- Hardcode secrets in code
- Use same secrets for dev/prod
- Log secret values

## Where Your Secrets Come From:

Your current secrets are in **HuggingFace Spaces**:
1. Go to: https://huggingface.co/spaces/YOUR_USERNAME/taskflow-api
2. Settings → Variables and secrets
3. Copy the values to your local secret.yaml

## Verification:

After deployment, check secrets are loaded:
```bash
# Check if secret exists
kubectl get secret taskflow-secrets -n taskflow

# Check environment variables in pod
kubectl exec -n taskflow <pod-name> -- env | grep -E "DATABASE_URL|OPENAI"
```
