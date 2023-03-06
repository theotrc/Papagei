FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY . /app 

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

CMD ["python", "app.py","0.0.0.0:8000"]