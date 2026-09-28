# This uses a minimal base image with Python 3.11 installed
FROM python:3.11-slim

# This sets the working directory inside the container to /app
WORKDIR /app

# This sets the backend URL for the Streamlit app
ENV BACKEND_URL="http://host.docker.internal:7860"

# This copies all files from the current directory on the host to the container's /app directory
COPY . .

# This installs Python dependencies listed in requirements.txt
RUN pip3 install -r requirements.txt

# This defines the command to run the Streamlit app on port 8501 and make it accessible externally
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]
