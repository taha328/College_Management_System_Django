# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        pkg-config \
        libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*
#Copying 
COPY . /app/

# Set working directory in the container
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip && pip install gunicorn && pip install -r requirements.txt



# Command to run the Gunicorn server with the specified configuration and WSGI application
CMD ["gunicorn", "-c", "gunicorn_config.py", "apogee.wsgi:application"]
