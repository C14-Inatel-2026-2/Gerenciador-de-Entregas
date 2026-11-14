FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install .

COPY . .

# Ajuste a porta e o comando de inicialização conforme a sua aplicação (ex: FastAPI/Flask/Uvicorn)
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-10000}"]