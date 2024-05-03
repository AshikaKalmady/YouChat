# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster
 
# Set the working directory in the container to /app
WORKDIR /app
 
# Add the current directory contents into the container at /app
ADD . /app
 
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
 
# Make port 8080 available to the world outside this container
EXPOSE 8080
 
# # Run streamlit when the container launches
# CMD streamlit run --server.port 8080 frontend.py
CMD ["streamlit", "run", "frontend.py","--server.port", "8080"]