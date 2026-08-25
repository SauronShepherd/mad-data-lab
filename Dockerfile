FROM node:22-slim AS frontend-build
WORKDIR /frontend
COPY package.json package-lock.json ./
RUN npm ci
COPY index.html vite.config.* tsconfig.json ./
COPY src src
RUN npm run build

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY server server
COPY backend backend
COPY data data
COPY cases cases
COPY --from=frontend-build /frontend/dist dist
COPY app.yaml .
ENV UVICORN_HOST=0.0.0.0 DATABRICKS_APP_PORT=8000 ALLOW_FIXTURE_MODE=1
EXPOSE 8000
CMD ["python", "-m", "server.run"]
