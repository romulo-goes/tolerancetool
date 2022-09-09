#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" & >/dev/null && pwd )"

echo $SCRIPT_DIR 

sudo dpkg -i requirements/*.deb

cd ../../..
python3 -m venv venv-tolerancetool
source venv-tolerancetool/bin/activate
pip3 install -r requirements/requirements.txt --no-index --find-links requirements
