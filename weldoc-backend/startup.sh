#!/bin/bash
cd /home/site/wwwroot

# Install ODBC Driver 18 for SQL Server on Azure Linux
if ! command -v sqlcmd &> /dev/null; then
    apt-get update
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 || true
fi

# Ensure all packages are installed (covers msal and others)
pip install -r requirements.txt --quiet || true

# Start gunicorn
gunicorn --bind=0.0.0.0 --timeout 600 run:app
