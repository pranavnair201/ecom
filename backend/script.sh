#!/bin/bash
pip3 install -r requirements.txt
# flask db init
# flask db migrate -m "initial migration"
flask db upgrade
python -u app.py