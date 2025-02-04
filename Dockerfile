FROM python:3.10-slim-buster

ADD . /edu-platform
WORKDIR /edu-platform

RUN mkdir /.cache && chmod 777 /.cache

RUN apt-get update
RUN apt-get update
RUN chmod -R 775 /edu-platform
RUN chown -R :root /edu-platform

RUN pip install -r requirements.txt

CMD [ "python", "./app.py" ]