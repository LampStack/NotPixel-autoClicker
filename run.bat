@echo off
title NotPixel

:run_bot
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

if not exist venv\Lib\site-packages\installed (
    if exist requirements.txt (
        echo Installing wheel for faster installation...
        pip install wheel
        echo Installing dependencies...
        pip install -r requirements.txt
        echo. > venv\Lib\site-packages\installed
    ) else (
        echo requirements.txt not found, skipping dependency installation.
    )
) else (
    echo Dependencies already installed, skipping installation.
)

if not exist .env (
    echo Copying configuration file...
    copy .env-example .env
) else (
    echo .env file already exists, skipping copy.
)

:menu
echo -----------------------------------------
echo 1. Run Bot
echo 2. Exit
echo -----------------------------------------
set /p choice="Please select an option (1, 2): "

if "%choice%"=="1" (
    echo Starting the bot...
    python main.py
    pause
    goto menu
) else if "%choice%"=="2" (
    exit
) else (
    echo Invalid option. Please try again.
    goto menu
)
