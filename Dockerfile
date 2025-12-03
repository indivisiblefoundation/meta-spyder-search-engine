# Stage 1: Builder
# Use a specific, slim version of Python for stability and reduced size.
FROM python:3.12-slim AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's cache.
# This layer only rebuilds if requirements.txt changes.
COPY requirements.txt ./

# Install Python dependencies, avoiding unnecessary caches and combining commands.
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
# Start a new, even more minimal stage for the final running application
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy only the installed packages from the builder stage (if needed, otherwise they are in the base image)
# and the application code.
COPY --from=builder /app /app

# Add metadata labels (optional, but good practice).
LABEL org.opencontainers.image.title="Meta-Spyder-Search-Engine" \
    org.opencontainers.image.version="1.0" \
    org.opencontainers.image.description="A containerized meta-search engine" \
    org.opencontainers.image.authors="TomasTorres"

# Create a non-root user and switch to it for enhanced security.
RUN groupadd -r appgroup && useradd --no-log-init -r -g appgroup appuser
USER appuser

# Expose the port your application will run on (e.g., if it has a web interface).
EXPOSE 8080

# Define the command to run your application when the container starts.
# Use the exec form for proper signal handling.
CMD ["python", "./your_main_script.py"]
