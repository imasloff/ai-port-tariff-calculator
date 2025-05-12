FROM python:3.11-slim as base

WORKDIR /work

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Command to run when container starts
# Default to running FastAPI
FROM base as backend

EXPOSE 8000

CMD ["python3", "-m", "app.server"]

FROM base as frontend

EXPOSE 8501

CMD ["streamlit", "run", "app/streamlit_app.py"]