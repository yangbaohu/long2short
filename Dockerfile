FROM python
RUN mkdir /long2short
WORKDIR /long2short
ADD . /long2short

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT gunicorn -D --log-file file.log --access-logfile access.log -k gevent -w 4 -b 0.0.0.0:5000 main:app
