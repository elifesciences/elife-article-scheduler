#!/bin/bash
set -e # everything must succeed.

python=/usr/bin/python3.5
py=${python##*/} # ll: python3.5

# check for exact version of python3
if [ ! -e "venv/bin/$py" ]; then
    echo "could not find venv/bin/$py, recreating venv"
    rm -rf venv
    $python -m venv venv
fi

source venv/bin/activate

if [ ! -e src/core/settings.py ]; then
    echo "no settings.py found! using the DEV settings (dev_settings.py) by default."
    cd src/core/
    ln -s dev_settings.py settings.py
    cd ../../
fi

pip install -r requirements.txt

python src/manage.py migrate --no-input
