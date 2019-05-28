
#FROM tiangolo/uwsgi-nginx-flask:python2.7
FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

#RUN pip install --upgrade pip
COPY src/requirements.txt  /app
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src /app
