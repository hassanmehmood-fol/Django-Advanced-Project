FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=60

WORKDIR /app

COPY requirements.txt requirements.dev.txt ./

# Base + dev dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements.dev.txt

COPY . .

EXPOSE 8000

# Django runserver (dev mode)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
