FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ templates/
COPY static/ static/

EXPOSE 5443

CMD ["gunicorn", "--bind", "0.0.0.0:5443", "--workers", "2", "--timeout", "30", \
     "--certfile", "/certs/cert.pem", "--keyfile", "/certs/privkey.pem", "app:app"]
