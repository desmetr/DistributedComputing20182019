# Use an official Python runtime as a parent image
FROM python:3.7.3

# Set the working directory to /app
WORKDIR /advertising

# Copy the current directory contents into the container at /app
COPY . /advertising

# Install any needed packages specified in requirements.txt
RUN make /advertising
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD export FLASK_APP=advertisingApp.py && flask run --host=0.0.0.0


