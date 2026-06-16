FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Fixed application settings
ENV DJANGO_SETTINGS_MODULE=config.settings.prod
ENV DEBUG=False

WORKDIR /app

# Install nginx
RUN apt-get update && apt-get install -y nginx \
    && rm -f /etc/nginx/sites-enabled/default \
    && rm -f /etc/nginx/conf.d/default.conf \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements /app/requirements/
RUN pip install --no-cache-dir -r requirements/prod.txt

# Copy application code
COPY . /app/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/app/entrypoint.sh"]