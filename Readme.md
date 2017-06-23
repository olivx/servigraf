
# Servigraf *WebGraf* Sistemas
[![Build Status](https://travis-ci.org/olivx/servigraf.svg?branch=master)](https://travis-ci.org/olivx/servigraf)

[![Code Health](https://landscape.io/github/olivx/servigraf/master/landscape.svg?style=flat)](https://landscape.io/github/olivx/servigraf/master)

[![Code Climate](https://codeclimate.com/github/olivx/servigraf/badges/gpa.svg)](https://codeclimate.com/github/olivx/servigraf)

## introdução
WebGraf é um novo sistema feito em django que vai substituir o antigo sistema,
*sysgraf* feito em java, o objetivo é arrumar os BUG que haviam no sistema antigo,
 desenvolver e novas funcinalidades, explorando todo o potencional do django e criando
 mais controle para que possa focar em seus serviços e não no controle da sua empresa.

### rodando o sistema em ambiente de desenvolvimento
```bash
git clone git@github.com:olivx/servigraf.git servigraf
cd servigraf
python -m venv .servigraf
source .servigraf/bin/activate
pip install -r requirements.txt
python contrib/generate_.env.py
python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py runserver

```



##### oliveiravicente.net@gmail.com