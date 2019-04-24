FROM python:3.7-alpine

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# install  pillow dependencies

RUN apk --no-cache add python \
                       build-base \
                       python-dev \
                       # wget dependency
                       openssl \
                       # dev dependencies
                       git \
                       bash \
                       sudo \
                       py2-pip \
                       # Pillow dependencies
                       jpeg-dev \
                       zlib-dev \
                       freetype-dev \
                       lcms2-dev \
                       openjpeg-dev \
                       tiff-dev \
                       tk-dev \
                       tcl-dev \
                       harfbuzz-dev \
                       fribidi-dev

RUN pip install --upgrade pip
RUN pip install pipenv

RUN apk update \
    && apk add --no-cache --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && apk del build-deps


COPY Pipfile* ./
RUN pipenv install --system --deploy

COPY . /app

# RUN pip install -r requirements.txt

# run entrypoint
# ENTRYPOINT ["/app/entrypoint.sh"]
ENTRYPOINT ["gunicorn", "servigraf.wsgi:application", "--bind 0.0.0.0:8000"]
