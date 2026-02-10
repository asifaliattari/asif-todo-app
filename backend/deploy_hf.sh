#!/bin/bash

# Hugging Face Deployment Script for TaskFlow Backend
# Run this from bash/terminal in the backend directory

echo "🚀 TaskFlow Backend - Hugging Face Deployment"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Get Hugging Face username
echo "📝 Enter your Hugging Face username:"
read -r hf_username

if [ -z "$hf_username" ]; then
    echo "❌ Username cannot be empty"
    exit 1
fi

# Get Space name
echo ""
echo "📝 Enter your Space name (default: taskflow-api):"
read -r space_name
if [ -z "$space_name" ]; then
    space_name="taskflow-api"
fi

space_url="https://huggingface.co/spaces/$hf_username/$space_name"

echo ""
echo "📋 Deployment Summary:"
echo "   Username: $hf_username"
echo "   Space: $space_name"
echo "   URL: $space_url"
echo ""

# Ask for confirmation
echo "⚠️  Make sure you have already created the Space at:"
echo "   https://huggingface.co/spaces (SDK: Docker)"
echo ""
echo "Continue with deployment? (Y/N):"
read -r confirm

if [ "$confirm" != "Y" ] && [ "$confirm" != "y" ]; then
    echo "❌ Deployment cancelled"
    exit 0
fi

# Create temporary deployment directory
temp_dir="/tmp/taskflow-backend-deploy"
echo ""
echo "📁 Creating deployment directory..."

rm -rf "$temp_dir"
mkdir -p "$temp_dir"

# Copy necessary files
echo "📦 Copying backend files..."
backend_dir="$(pwd)"

cp -r "$backend_dir/app" "$temp_dir/"
cp "$backend_dir/Dockerfile" "$temp_dir/"
cp "$backend_dir/requirements.txt" "$temp_dir/"
[ -f "$backend_dir/.dockerignore" ] && cp "$backend_dir/.dockerignore" "$temp_dir/"

# Create README.md from README_HF.md
if [ -f "$backend_dir/README_HF.md" ]; then
    cp "$backend_dir/README_HF.md" "$temp_dir/README.md"
else
    echo "⚠️  README_HF.md not found, creating basic README.md"
    cat > "$temp_dir/README.md" << 'EOF'
---
title: TaskFlow API
emoji: ✅
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
app_port: 7860
---

# TaskFlow Backend API
FastAPI backend for TaskFlow todo application.
EOF
fi

# Initialize git and push
echo "🔧 Initializing git repository..."
cd "$temp_dir" || exit 1
git init
git checkout -b main

echo "📝 Adding files..."
git add .
git commit -m "Initial deployment of TaskFlow Backend"

echo "🔗 Adding Hugging Face remote..."
git remote add space "https://huggingface.co/spaces/$hf_username/$space_name"

echo ""
echo "🚀 Pushing to Hugging Face Space..."
echo "   You may need to enter your Hugging Face credentials"
echo ""

git push space main --force

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Deployment successful!"
    echo ""
    echo "📋 Next Steps:"
    echo "   1. Go to: $space_url/settings"
    echo "   2. Add these environment variables in 'Variables and secrets':"
    echo "      - DATABASE_URL: Your Neon PostgreSQL URL"
    echo "      - SECRET_KEY: Generate with 'openssl rand -base64 32'"
    echo ""
    echo "   3. Wait for Space to build (check logs)"
    echo ""
    echo "   4. Test your API at:"
    echo "      https://$hf_username-$space_name.hf.space/docs"
    echo ""
else
    echo ""
    echo "❌ Deployment failed"
    echo "   Check the error messages above"
    echo "   Make sure:"
    echo "   - You created the Space on Hugging Face"
    echo "   - Your credentials are correct"
    echo "   - Space name matches exactly"
fi

# Cleanup
echo ""
echo "🧹 Cleaning up temporary files..."
cd "$backend_dir" || exit 1
rm -rf "$temp_dir"

echo "✨ Done!"
