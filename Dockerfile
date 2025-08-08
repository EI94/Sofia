FROM python:3.12-slim AS runtime

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements-bulk.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements-bulk.txt

# Copy bulk API package
COPY sofia_bulk_api/ /app/sofia_bulk_api

# Create data directory for TinyDB
RUN mkdir -p /app/data

# Set environment variables
ENV BULK_API_KEY="changeme"
ENV CORE_SOFIA_URL="https://sofia-lite-xxxxx.run.app/api/prompt"
ENV PYTHONPATH="/app"

# Expose port
EXPOSE 8080

# Run the application
CMD ["uvicorn", "sofia_bulk_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
