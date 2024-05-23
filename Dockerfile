FROM python:3.10

RUN mkdir -p /app

# Set the working directory
WORKDIR /app

RUN apt-get update && apt-get install git -y && apt-get install curl -y

RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy the requirements file to the working directory
COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app
