FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install .

COPY . .

# Ajuste a porta e o comando de inicialização conforme a sua aplicação (ex: FastAPI/Flask/Uvicorn)
CMD ["uvicorn", "src.gestao_frotas.main:app", "--host", "0.0.0.0", "--port", "10000"]