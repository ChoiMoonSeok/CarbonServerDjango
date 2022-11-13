FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends; apt-get install -y mysql-server; \
    apt-get install -y python3; apt-get install -y python3-pip; \
    python -m pip install --upgrade pip; \
    pip install virtualenv; mkdir myproject; virtualenv venv; . venv/bin/activate;\
    pip install django; sudo apt-get install python-dev libmysqlclient-dev; sudo apt-get install python3-dev; \
    pip install mysqlclient; 

CMD cd /; . /venv/bin/activate;\
    cd /; cd home;\
    python3 manage.py runserver