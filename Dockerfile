FROM python:3.12.7-alpine

RUN apk update && apk add python3-dev gcc libc-dev

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install gunicorn
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt
RUN pip list

ADD ./backend /app/backend
ADD ./docker /app/docker

RUN chmod +x /app/docker/backend/server-entrypoint.sh
RUN chmod +x /app/docker/backend/worker-entrypoint.sh
