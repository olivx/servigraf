
# Servigraf *WebGraf* Sistemas
[![Build Status](https://travis-ci.org/olivx/servigraf.svg?branch=master)](https://travis-ci.org/olivx/servigraf)

[![Code Health](https://landscape.io/github/olivx/servigraf/master/landscape.svg?style=flat)](https://landscape.io/github/olivx/servigraf/master)

[![Code Climate](https://codeclimate.com/github/olivx/servigraf/badges/gpa.svg)](https://codeclimate.com/github/olivx/servigraf)

## introdução
WebGraf é um projeto de CRUD basico para demotração.
### rodando o sistema em ambiente de desenvolvimento
```bash
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
```



##### oliveiravicente.net@gmail.com
