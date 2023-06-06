FROM ubuntu

WORKDIR /usr/share/ide 
# if not there, created

RUN apt-get -y update && apt-get -y upgrade

RUN apt-get install -y python3 && apt-get install -y g++ && apt-get install -y python3-pip && pip install django

RUN apt update

RUN apt-get install default-jdk -y

COPY ide .

CMD [ "python3", "/usr/share/ide/manage.py", "runserver", "0.0.0.0:8000" ]
