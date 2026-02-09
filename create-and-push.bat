@echo off
echo ========================================
echo  GitHub Repository Setup
echo ========================================
echo.
echo Step 1: Opening GitHub to create repository...
echo.
start https://github.com/new?name=asif-todo-app^&description=TaskFlow+-+AI-Powered+Project+Management+System+by+Asif+Ali+AstolixGen+for+GIAIC+Hackathon+2026^&visibility=public
echo.
echo INSTRUCTIONS:
echo 1. A browser window will open to create the repository
echo 2. Make sure "asif-todo-app" is the repository name
echo 3. Set it to PUBLIC
echo 4. DO NOT initialize with README, .gitignore, or license
echo 5. Click "Create repository"
echo 6. Come back to this window and press any key when done...
echo.
pause
echo.
echo Step 2: Pushing code to GitHub...
echo.
git push -u origin main
echo.
if %errorlevel% equ 0 (
    echo ========================================
    echo  SUCCESS! Code pushed to GitHub!
    echo ========================================
    echo.
    echo Your repository: https://github.com/asifaliattari/asif-todo-app
    echo.
    echo Next step: Deploy to Vercel
    echo Go to: https://vercel.com/new
    echo.
) else (
    echo ========================================
    echo  Push failed. You may need to:
    echo  1. Configure git credentials
    echo  2. Or push manually: git push -u origin main
    echo ========================================
)
echo.
pause
