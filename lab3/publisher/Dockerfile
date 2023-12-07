FROM python:3.11.1-slim

WORKDIR /app

RUN pip install paho-mqtt requests

COPY main.py ./

CMD ["python", "main.py"]
