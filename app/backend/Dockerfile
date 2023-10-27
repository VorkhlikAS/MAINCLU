FROM python:3.9.18-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD . .

# RUN python3 ./db/main.py

CMD [ "python", "server.py" ]
