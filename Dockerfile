# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8882 to the outside world
EXPOSE 8882

# Create a virtual environment
RUN python -m venv venv

# Install dependencies in the virtual environment
RUN /bin/bash -c "source venv/bin/activate && pip install -r requirements.txt"

# Copy the entrypoint script into the container
COPY entrypoint.sh /app/entrypoint.sh

# Ensure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Command to run the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
