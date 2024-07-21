FROM python:3.9

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r /app/requirements.txt

COPY . .

#WORKDIR src

#CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000