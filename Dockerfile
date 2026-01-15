FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /ai_agent

COPY pyproject.toml ./

# Install dependencies only
RUN pip install --no-cache-dir .

# Copy project files
COPY . .

# Run the application
CMD ["python", "main.py"]