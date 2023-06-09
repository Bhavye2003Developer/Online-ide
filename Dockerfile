FROM python:3.9-slim-buster

WORKDIR /usr/share/ide 
# if not there, created

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

COPY ide .

CMD [ "python3", "/usr/share/ide/manage.py", "runserver", "0.0.0.0:8000" ]
