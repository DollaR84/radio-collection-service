FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a user and group
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents and requirements.txt into the container at /app
COPY src/ /app/
COPY entrypoint.sh requirements.txt /app/

# Ensure the entrypoint script is executable
RUN chmod a+x /app/entrypoint.sh

RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  libpq-dev \
  curl \
  postgresql-client \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r /app/requirements.txt

# Establish the rights to the directory
RUN mkdir -p /app/data && chown -R appuser:appgroup /app/data
# Switching to an unheard of user
USER appuser

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "-m", "main"]
