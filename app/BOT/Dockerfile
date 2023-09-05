FROM python:latest

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENV BOT_TOKEN=""

# ENTRYPOINT [ "/bin/bash" ]

CMD [ "python3", "main.py" ]
