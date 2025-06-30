FROM python:3.11-slim

# Installa dipendenze di sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia e installa requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'applicazione
COPY app/ ./app

# Crea utente non-root per sicurezza
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Esponi la porta (Cloud Run usa PORT env var)
EXPOSE 8000

# Comando per avviare l'applicazione
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"] 