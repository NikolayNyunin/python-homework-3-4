FROM python:3.12.7-slim-bullseye

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN chmod +x /app/docker/start.sh

CMD ["/app/docker/start.sh"]
