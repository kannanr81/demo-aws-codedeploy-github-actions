# Use the official Python Alpine image as the base image
FROM public.ecr.aws/docker/library/python:alpine3.18

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY app.py /app
COPY requirements.txt /app

# Install system dependencies and Python packages
RUN apk add --no-cache gcc musl-dev libffi-dev py3-pip && \
    pip install --no-cache-dir boto3 flask && \
    pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python3", "app.py"]
