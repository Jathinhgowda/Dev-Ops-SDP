FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install Flask

EXPOSE 5007

CMD ["python","app.py"]
