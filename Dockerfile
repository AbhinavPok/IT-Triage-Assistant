FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy application files
COPY src/ ./src/
COPY datamgmt.py .
COPY requirements.txt .

# Install dependencies (stdlib only for now)
RUN pip install --no-cache-dir -r requirements.txt

# Create runtime directories
RUN mkdir -p output archive logs \
    && chown -R appuser:appuser /app

# Drop privileges
USER appuser

# Default command (triage app)
CMD ["python", "src/main.py"]
