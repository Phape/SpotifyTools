FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements-prod.txt requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy application code
COPY . /app

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# Use gunicorn instead of uwsgi for better Python 3.11+ compatibility
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--worker-class", "gevent", "app:app"]