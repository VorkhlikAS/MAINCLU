FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD . .

# RUN python3 ./db/main.py

CMD [ "python", "server.py" ]