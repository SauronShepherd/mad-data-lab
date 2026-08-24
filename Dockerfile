FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY server server
COPY dist dist
COPY app.yaml .
ENV UVICORN_HOST=0.0.0.0 UVICORN_PORT=8000
EXPOSE 8000
CMD ["python", "-m", "server.run"]
