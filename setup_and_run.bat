@echo off
echo Setting up SQL Visualizer...
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo Virtual environment activated!
echo.

REM Check if requirements are installed
echo Installing/updating requirements...
pip install -r requirements.txt
echo Requirements installed!
echo.

REM Generate encryption key if not exists
python -c "
from cryptography.fernet import Fernet
import os

if not os.path.exists('.env'):
    print('Creating .env file...')
    key = Fernet.generate_key().decode()
    with open('.env', 'w') as f:
        f.write(f'SECRET_KEY=your-super-secret-key-change-this-in-production-environment\n')
        f.write(f'DATABASE_URL=sqlite:///sql_visualizer.db\n')
        f.write(f'ENCRYPTION_KEY={key}\n')
        f.write(f'FLASK_ENV=development\n')
    print('Environment file created with encryption key!')
else:
    print('Environment file already exists.')
"

echo.
echo Setup complete! Starting the application...
echo.
echo Open your browser and go to: http://localhost:5000
echo.

REM Run the application
python run.py

pause
