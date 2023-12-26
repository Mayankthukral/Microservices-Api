# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for MongoDB URI
ENV MONGODB_URI="mongodb+srv://mayankthukral1810:hello123@cluster0.zyjeuqn.mongodb.net/?retryWrites=true&w=majority"

COPY .env .env

# Print the environment variable for debugging
RUN echo $MONGODB_URI

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Run app.py when the container launches
CMD ["python", "app.py"]
