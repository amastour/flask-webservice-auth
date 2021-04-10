FROM ubuntu:18.04

RUN apt update 

RUN apt install -y python3 python3-pip

ADD requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN mkdir /app

ADD src src

EXPOSE 5000

ENV CONFIG_TYPE=dev

RUN python3 src/manage.py db_init

CMD ["python3", "/src/manage.py" ,"run"]
