#!/bin/bash
pip3 install -r requirements.txt
flask db upgrade
python app.py