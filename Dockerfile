FROM --platform=linux/amd64 python:3.10.3-slim

WORKDIR /reporter

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "main.py"]