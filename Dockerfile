FROM python:3.8-alpine

LABEL maintainer="Paul (Kyunghan) Lee <contact@paullee.dev>"

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "app:app"]
