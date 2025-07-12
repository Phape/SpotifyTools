FROM python:3.12-slim

WORKDIR /app

# Install Dart Sass CLI
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://github.com/sass/dart-sass/releases/download/1.89.2/dart-sass-1.89.2-linux-x64.tar.gz \
    | tar -xz -C /opt \
    && ln -s /opt/dart-sass/sass /usr/local/bin/sass \
    && apt-get remove -y curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements-prod.txt requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy application code
COPY . /app

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# Start gunicorn directly - SCSS compilation handled by Flask-Assets DartSassFilter
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--worker-class", "gevent", "app:app"]