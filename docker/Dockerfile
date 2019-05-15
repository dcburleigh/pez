
#FROM tiangolo/uwsgi-nginx-flask:python2.7
FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

COPY src /app

#RUN pip install --upgrade pip
RUN pip install --upgrade pip && pip install -r requirements.txt
