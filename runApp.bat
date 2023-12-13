@echo off

if not exist venv\Scripts\activate (
	echo Creating virtual environment...
	python -m venv venv
	call venv\Scripts\activate
) else (
	call venv\Scripts\activate
)

echo Installing/updating requirements...
pip install -r requirements.txt

echo Running the app...
python flaskapp\app.py