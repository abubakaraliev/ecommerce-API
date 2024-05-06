FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y gcc python3-dev libmariadb-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

WORKDIR /app

RUN pip install --default-timeout=100 -r requirements.txt  && \
pip install mysqlclient \
&& pip install itsdangerous

WORKDIR /app/src

EXPOSE 9090

CMD ["python3", "app.py"]