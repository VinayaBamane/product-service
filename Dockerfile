
# Use lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY database.py .

# Expose application port
EXPOSE 5001

# Start Flask application
CMD ["python", "app.py"]
