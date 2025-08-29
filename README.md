Application Deployment Steps:

1) Django services
-- # Create a virtual environment
-- python -m venv .venv
-- # But I had to specify the full path: "C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe -m venv .venv"
-- # Activate virtual environment:
-- .\.venv\Scripts\Activate.ps1
-- # Installing the required libraries
-- pip install -r requirements.txt

2) React front service
-- # Install project dependencies
-- npm install
-- # Build project
-- npm run build

3) Enter databases data and server addresses into file .env
