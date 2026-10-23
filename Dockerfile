# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirement files and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port 5000
EXPOSE 5000

# Run Flask app via Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]