# pull base image
FROM python:3.14

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory to be /app inside docker container
WORKDIR /app


# Install dependencies
RUN mkdir requirements
COPY requirements /app/requirements/
RUN pip install -r requirements/prod.txt

# Copy project files from local folder to docker's /app/ dir
COPY . /app/