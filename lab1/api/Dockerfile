FROM python:3.11.1-slim

WORKDIR /app

RUN pip install fastapi uvicorn sqlalchemy psycopg2-binary

COPY *.py ./

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]
