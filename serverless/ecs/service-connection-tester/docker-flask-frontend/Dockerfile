# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["./gunicorn.sh"]