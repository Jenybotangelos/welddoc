#!/bin/bash

# Install ODBC Driver 18 for SQL Server on Azure Linux
if ! command -v sqlcmd &> /dev/null; then
    apt-get update
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 || true
fi

# Ensure we're in the right directory
cd weldoc-backend 2>/dev/null || true

# Install any missing packages
pip install -r requirements.txt --quiet 2>/dev/null || true

# Start gunicorn
gunicorn --bind=0.0.0.0 --timeout 600 run:app
