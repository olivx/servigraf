#!/bin/bash
git clone git@github.com:olivx/servigraf.git servigraf
cd servigraf
python -m venv .servigraf
source .servigraf/bin/activate
pip install -r requirements.txt
python contrib/generate_.env.py
python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py  createsuperuser
python manage.py  init_fake_data
python manage.py runserver
