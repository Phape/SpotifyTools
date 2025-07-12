#!/bin/bash
set -e

echo "🎨 Compiling SCSS files with Dart Sass..."

# Create output directory if it doesn't exist
mkdir -p /app/app/static/css

# Compile SCSS files
if [ -f "/app/app/static/css/main.scss" ]; then
    echo "📦 Compiling main.scss..."
    sass --style=compressed --no-source-map \
         /app/app/static/css/main.scss \
         /app/app/static/css/main.css
    echo "✅ SCSS compilation completed"
else
    echo "⚠️  main.scss not found, skipping compilation"
fi

echo "🚀 Starting Flask application..."
exec "$@"
