FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd

RUN apt-get update && apt-get install -y postgresql-client

COPY . .

COPY models /app/models


# CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 && echo 'FastAPI application started successfully!'"]

# CMD bash -c "while ! nc -z db 5432; do sleep 1; done; echo 'PostgreSQL started'; alembic upgrade head; uvicorn main:app --host 0.0.0.0 --port 8000"

# Set the entrypoint to the script
ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
