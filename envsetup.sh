#!/bin/bash

if [ -d "env" ]; then
    echo "Python virtual environment exists."
else
    python -m venv env
fi

# Activate the virtual environment
source env/bin/activate

# Install requirements
pip3 install -r requirements.txt

if [ -d "logs" ]; then
    echo "Log folder exists."
else
    mkdir logs
    touch logs/error.log logs/access.log
fi

sudo chmod -R 777 logs
