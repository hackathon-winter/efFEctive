FROM python:3
ENV PYTHONUNBUFFERD 1
RUN mkdir /code
RUN apt-get update && apt-get install -y nginx
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
ADD nginx.conf /etc/nginx/sites-available/default
RUN ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default