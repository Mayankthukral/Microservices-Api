# /caps-api/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY model/caps_model.py model/
COPY route/caps_route.py route/
COPY app.py .

CMD ["python", "app.py"]