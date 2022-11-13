FROM ubuntu:20.04
RUN apt-get update; apt-get install -y python3-pip; \
    python -m pip install --upgrade pip; \
    pip install virtualenv; mkdir myproject; virtualenv venv; . venv/bin/activate;\
    pip install django; pip install mysqlclient; 

CMD cd /; . /venv/bin/activate;\
    cd /; cd home;\
    python3 manage.py runserver