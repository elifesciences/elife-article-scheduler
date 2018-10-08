#!/bin/bash
set -e # everything must succeed.
echo "[-] install.sh"

. mkvenv.sh

source venv/bin/activate

if [ ! -e src/core/settings.py ]; then
    echo "no settings.py found! using the DEV settings (dev_settings.py) by default."
    cd src/core/
    ln -s dev_settings.py settings.py
    cd ../../
fi

pip install -r requirements.txt

python src/manage.py migrate --no-input

echo "[✓] install.sh"
