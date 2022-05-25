#!/bin/bash
set -e # everything must succeed.
echo "[-] install.sh"

. mkvenv.sh

source venv/bin/activate
pip install pip wheel --upgrade
pip install -r requirements.txt --no-color

if [ ! -e app.cfg ]; then
    echo "* no app.cfg found! using the example settings (elife.cfg) by default."
    ln -s elife.cfg app.cfg
fi

python src/manage.py migrate --no-input

echo "[✓] install.sh"
