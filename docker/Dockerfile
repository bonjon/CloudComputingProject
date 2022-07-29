# syntax=docker/dockerfile:1

FROM python:3.9-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "streamlit", "run", "main.py" ]