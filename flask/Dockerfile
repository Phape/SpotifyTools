FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements-prod.txt requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy application code
COPY . /app

# Workaround: Symlink for sass_embedded architecture issue
# The library looks for /usr/local/lib/python3.12/site-packages/sass_embedded/dart_sass/_ext/1.89.2-linux-aarch64/dart-sass/src/dart
# But only 1.89.2-linux-arm64 is present
RUN find /usr/local/lib/python*/site-packages/sass_embedded/dart_sass/_ext/ -type d -name "1.*-linux-arm64" -exec bash -c 'for d; do ln -s "$d" "${d/arm64/aarch64}"; done' _ {} +

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# Use gunicorn instead of uwsgi for better Python 3.11+ compatibility
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--worker-class", "gevent", "app:app"]