FROM ubuntu:20.04
RUN apt-get update && apt-get install -y --no-install-recommends; \
    apt-get install -y python3; apt-get install -y python3-pip; \
    pip install --upgrade pip; pip install virtualenv; mkdir myproject; virtualenv venv; . venv/bin/activate;\
    pip install django; pip install djangorestframework; pip install dj_rest_auth;
CMD cd /; . /venv/bin/activate;\
    cd /; cd home;\
    python3 manage.py makemigrations; python3 manage.py migrate \
    python3 manage.py runserver