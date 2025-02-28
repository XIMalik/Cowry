FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV DEBIAN_FRONTEND=noninteractive
 RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    gcc \
    zlib1g-dev \
    libaio1 \
    libaio-dev \
    libpq-dev \
    nano && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /frontend

COPY . .

RUN pip install -r r.txt

EXPOSE 1010