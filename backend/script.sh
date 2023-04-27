#!/bin/bash
pip3 install -r requirements.txt
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python app.py