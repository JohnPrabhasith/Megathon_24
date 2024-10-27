# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the app code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Define environment variable for MongoDB URI
ENV MONGODB_URI = "mongodb+srv://vigneshpatel0707:12345@cluster0.fjgp0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#Replace or set as runtime variable

# Command to run the app
CMD ["python", "app.py"]
