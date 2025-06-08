FROM python:3.11-slim

WORKDIR /app

# Copia TODO lo necesario, incluyendo test/
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
