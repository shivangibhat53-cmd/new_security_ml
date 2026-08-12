FROM python:3.10-slim-bookworm

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y awscli && \
    apt-get clean

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python3","app.py"]