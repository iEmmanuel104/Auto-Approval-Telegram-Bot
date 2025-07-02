@echo off
REM Auto Approval Bot Starter Script for Windows

echo 🤖 Starting Auto Approval Bot...

REM Check if .env file exists
if not exist .env (
    echo ❌ Error: .env file not found!
    echo Please copy .env.example to .env and fill in your credentials
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo ❌ Error: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

REM Activate virtual environment
echo 📦 Activating virtual environment...
call venv\Scripts\activate

REM Load environment variables from .env file
echo 🔧 Loading environment variables...
for /f "delims=" %%x in (.env) do (
    set "line=%%x"
    if not "!line:~0,1!"=="#" (
        set "%%x"
    )
)

REM Start the bot
echo 🚀 Starting bot...
python bot.py

pause