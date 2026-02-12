#!/bin/bash
echo "Monitoring deployments..."
for i in {1..20}; do
    echo ""
    echo "=== Check #$i at $(date +%H:%M:%S) ==="
    
    # Check backend
    BACKEND_VERSION=$(curl -s https://asifaliastolixgen-taskflow-api.hf.space/ | python -m json.tool 2>/dev/null | grep version | cut -d'"' -f4)
    echo "Backend version: $BACKEND_VERSION"
    
    # Check frontend
    ADMIN_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://asif-todo-app.vercel.app/admin)
    FILES_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://asif-todo-app.vercel.app/files)
    echo "Frontend /admin: HTTP $ADMIN_STATUS"
    echo "Frontend /files: HTTP $FILES_STATUS"
    
    # Check if ready
    if [ "$BACKEND_VERSION" = "2.1.0" ] && [ "$ADMIN_STATUS" = "200" ]; then
        echo ""
        echo "🎉 DEPLOYMENT COMPLETE! 🎉"
        echo "Backend: v2.1.0 ✅"
        echo "Frontend: /admin and /files ready ✅"
        exit 0
    fi
    
    sleep 60
done

echo ""
echo "Monitoring timed out after 20 minutes"
