FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt requirements.txt
COPY main.py main.py
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]
