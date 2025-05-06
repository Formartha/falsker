FROM python:3.10-slim

WORKDIR /app

# Install Python dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app/ .

# Expose the Flask app on port 5002
CMD ["python", "flasker.py"]
