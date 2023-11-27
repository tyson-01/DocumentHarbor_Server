@echo off

if not exist venv\Scripts\activate (
	echo Creating virtual environment...
	python -m venv venv
	call venv\Scripts\activate
	pip install -r requirements.txt
) else (
	call venv\Scripts\activate
)

echo Running the app...
python flaskapp\app.py