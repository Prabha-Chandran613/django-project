# Use the official Python image as the base image
FROM python:3.8

# Set environment variables for Keycloak
ENV KEYCLOAK_USER=prabha
ENV KEYCLOAK_PASSWORD=Scpp@2001

# Set work directory in the container
WORKDIR /app

# Copy the entire Django project directory to the container
COPY . /app/

# Install Django and any other required dependencies (if not using requirements.txt)
RUN pip install django keycloak

# Expose the port for Django
EXPOSE 8000

# Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
