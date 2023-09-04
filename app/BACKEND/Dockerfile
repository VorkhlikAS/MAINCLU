FROM python:latest

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

# CMD [ "python3", "main.py" ]

CMD [ "uvicorn", "server:app", "--reload", "--host", "0.0.0.0" ]

