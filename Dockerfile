FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nginx \
        supervisor \
        && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

RUN mkdir -p /var/log/supervisor \
             /etc/supervisor/conf.d

COPY config.nginx /etc/nginx/sites-enabled/flaskapp
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY . .

EXPOSE 80

CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf", "-n", "-u", "root"]
