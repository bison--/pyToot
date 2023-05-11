# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements-full.txt .

# Install the application's dependencies
RUN pip install --no-cache-dir -r requirements-full.txt

# Copy the rest of the application code to the container
COPY . .

# Set the environment variable to run the application
ENV PYTHONUNBUFFERED=1

# Define the command to run the application
CMD [ "python", "./main.py" ]
