FROM python:3.8-alpine

LABEL maintainer="Paul (Kyunghan) Lee <contact@paullee.dev>"

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /app

EXPOSE 8000

ENTRYPOINT ["gunicorn", "-t", "600", "-w", "1", "-b", "0.0.0.0:8000", "app:app"]
