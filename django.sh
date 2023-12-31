#!/bin/bash
echo "Create migrations"
python manage.py makemigrations 
echo "=================================="

echo "Migrate"
python manage.py migrate
echo "=================================="

echo Start celery worker 

celery -A hotelmanagementsystem worker --loglevel=info &
celery -A hotelmanagementsystem beat --loglevel=info &
echo "=================================="


echo "Start server"
python manage.py runserver 0.0.0.0:8000 