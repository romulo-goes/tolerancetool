#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" & >/dev/null && pwd )"

echo $SCRIPT_DIR 

python3 -m venv venv-tolerancetool
source venv-tolerancetool/bin/activate
pip install -r requirements/requirements.txt
