# Hugging Face Deployment Script for TaskFlow Backend
# Run this from PowerShell in the backend directory

Write-Host "🚀 TaskFlow Backend - Hugging Face Deployment" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
$gitInstalled = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitInstalled) {
    Write-Host "❌ Git is not installed. Please install Git first." -ForegroundColor Red
    exit 1
}

# Get Hugging Face username
Write-Host "📝 Enter your Hugging Face username:" -ForegroundColor Yellow
$hfUsername = Read-Host

if ([string]::IsNullOrWhiteSpace($hfUsername)) {
    Write-Host "❌ Username cannot be empty" -ForegroundColor Red
    exit 1
}

# Get Space name
Write-Host ""
Write-Host "📝 Enter your Space name (default: taskflow-api):" -ForegroundColor Yellow
$spaceName = Read-Host
if ([string]::IsNullOrWhiteSpace($spaceName)) {
    $spaceName = "taskflow-api"
}

$spaceUrl = "https://huggingface.co/spaces/$hfUsername/$spaceName"

Write-Host ""
Write-Host "📋 Deployment Summary:" -ForegroundColor Cyan
Write-Host "   Username: $hfUsername" -ForegroundColor White
Write-Host "   Space: $spaceName" -ForegroundColor White
Write-Host "   URL: $spaceUrl" -ForegroundColor White
Write-Host ""

# Ask for confirmation
Write-Host "⚠️  Make sure you have already created the Space at:" -ForegroundColor Yellow
Write-Host "   https://huggingface.co/spaces (SDK: Docker)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Continue with deployment? (Y/N):" -ForegroundColor Yellow
$confirm = Read-Host

if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "❌ Deployment cancelled" -ForegroundColor Red
    exit 0
}

# Create temporary deployment directory
$tempDir = Join-Path $env:TEMP "taskflow-backend-deploy"
Write-Host ""
Write-Host "📁 Creating deployment directory..." -ForegroundColor Cyan

if (Test-Path $tempDir) {
    Remove-Item $tempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $tempDir | Out-Null

# Copy necessary files
Write-Host "📦 Copying backend files..." -ForegroundColor Cyan
$backendDir = $PSScriptRoot

Copy-Item "$backendDir\app" -Destination "$tempDir\app" -Recurse
Copy-Item "$backendDir\Dockerfile" -Destination "$tempDir\Dockerfile"
Copy-Item "$backendDir\requirements.txt" -Destination "$tempDir\requirements.txt"
Copy-Item "$backendDir\.dockerignore" -Destination "$tempDir\.dockerignore" -ErrorAction SilentlyContinue

# Create README.md from README_HF.md
if (Test-Path "$backendDir\README_HF.md") {
    Copy-Item "$backendDir\README_HF.md" -Destination "$tempDir\README.md"
} else {
    Write-Host "⚠️  README_HF.md not found, creating basic README.md" -ForegroundColor Yellow
    $readmeContent = @"
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
"@
    $readmeContent | Out-File -FilePath "$tempDir\README.md" -Encoding UTF8
}

# Initialize git and push
Write-Host "🔧 Initializing git repository..." -ForegroundColor Cyan
Set-Location $tempDir
git init
git checkout -b main

Write-Host "📝 Adding files..." -ForegroundColor Cyan
git add .
git commit -m "Initial deployment of TaskFlow Backend"

Write-Host "🔗 Adding Hugging Face remote..." -ForegroundColor Cyan
git remote add space "https://huggingface.co/spaces/$hfUsername/$spaceName"

Write-Host ""
Write-Host "🚀 Pushing to Hugging Face Space..." -ForegroundColor Cyan
Write-Host "   You may need to enter your Hugging Face credentials" -ForegroundColor Yellow
Write-Host ""

git push space main --force

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Deployment successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Next Steps:" -ForegroundColor Cyan
    Write-Host "   1. Go to: $spaceUrl/settings" -ForegroundColor White
    Write-Host "   2. Add these environment variables in 'Variables and secrets':" -ForegroundColor White
    Write-Host "      - DATABASE_URL: Your Neon PostgreSQL URL" -ForegroundColor White
    Write-Host "      - SECRET_KEY: Generate with 'openssl rand -base64 32'" -ForegroundColor White
    Write-Host ""
    Write-Host "   3. Wait for Space to build (check logs)" -ForegroundColor White
    Write-Host ""
    Write-Host "   4. Test your API at:" -ForegroundColor White
    Write-Host "      https://$hfUsername-$spaceName.hf.space/docs" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Deployment failed" -ForegroundColor Red
    Write-Host "   Check the error messages above" -ForegroundColor Yellow
    Write-Host "   Make sure:" -ForegroundColor Yellow
    Write-Host "   - You created the Space on Hugging Face" -ForegroundColor White
    Write-Host "   - Your credentials are correct" -ForegroundColor White
    Write-Host "   - Space name matches exactly" -ForegroundColor White
}

# Cleanup
Write-Host ""
Write-Host "🧹 Cleaning up temporary files..." -ForegroundColor Cyan
Set-Location $backendDir
Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "✨ Done!" -ForegroundColor Cyan
