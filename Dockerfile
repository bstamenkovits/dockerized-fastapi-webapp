FROM node:22-alpine AS build

# Install dependencies first to leverage Docker cache
# (dependency installation in separate layer means it won't run again unless
# package.json changes)
COPY ./frontend/package.json ./
COPY ./frontend/package-lock.json ./

RUN npm install

# Copy the rest of the Angular application code
COPY ./frontend .

# Build the Angular application for production
# Adjust 'dist/frontend' if your angular.json specifies a different outputPath
RUN npm run build -- --configuration production


# Use a slim Python base image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./backend/requirements.txt .

COPY --from=build /app/dist/frontend /app/frontend

# Install necessary Python packages
# We use a requirements.txt for better dependency management in real apps,
# but for this simple example, we'll install directly.
RUN pip install -r requirements.txt

# Copy the Flask application code into the container
COPY ./backend/src/ .

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the Flask application
# This is overridden by the 'command' in docker-compose.yml for this setup
CMD ["python", "app.py"]
