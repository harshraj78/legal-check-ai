FROM python:3.13-slim

# Prevents Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.0.0

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only dependency files
COPY pyproject.toml poetry.lock* ./

# Install dependencies without creating a virtualenv inside Docker
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Create a non-root user and switch to it
RUN useradd -m appuser
USER appuser

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]