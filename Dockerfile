FROM ubuntu:20.04

RUN apt-get update && apt-get install -y --no-install-recommends; \
    apt-get install -y python3;\
    apt-get install -y python3-pip; \
    pip install --upgrade pip;\
    pip install virtualenv;\
    mkdir myproject;\
    virtualenv venv;\
    . venv/bin/activate;\
    pip install django==4.1.4;\
    pip install djangorestframework==3.14.0;\
    pip install dj_rest_auth==2.2.5;\
    pip install django-allauth==0.51.0; \
    apt-get install python-dev libmysqlclient-dev -y;\
    pip install setuptools;\
    apt-get install python3-dev;\
    pip install mysqlclient;\
    pip install gunicorn;\
    pip install drf_yasg;\
    pip install tzdata;\
    pip install djangorestframework-simplejwt

CMD cd /; . /venv/bin/activate;\
    cd /; cd /home;\
    sleep 10; \
    python3 manage.py makemigrations; \
    python3 manage.py migrate; \
    python3 manage.py runserver 0.0.0.0:8000\ 