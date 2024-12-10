@echo off
echo Setting up your Python environment...

:: Create virtual environment
python -m venv venv

:: Activate virtual environment
call venv\Scripts\activate

:: Install required dependencies
pip install -r requirements.txt

echo Setup complete! You can now run your project.
pause
