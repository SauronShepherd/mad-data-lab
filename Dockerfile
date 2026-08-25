FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY server server
COPY backend backend
COPY data data
COPY dist dist
COPY app.yaml .
ENV UVICORN_HOST=0.0.0.0 DATABRICKS_APP_PORT=8000 ALLOW_FIXTURE_MODE=1
EXPOSE 8000
CMD ["python", "-m", "server.run"]
