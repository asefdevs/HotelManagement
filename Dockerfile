FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN pip install celery[redis]

EXPOSE 8000

RUN chmod +x /app/django.sh

WORKDIR /app

ENTRYPOINT ["/app/django.sh"]
