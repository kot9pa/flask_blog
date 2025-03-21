# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy the application files
COPY requirements.txt .env /app/
COPY /src /app/src
COPY /migrations /app/migrations

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Command to run your application
ENTRYPOINT [ "" ]