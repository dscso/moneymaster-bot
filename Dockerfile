FROM python:3.7-slim-buster

ADD . /bot
RUN pip install python-telegram-bot
WORKDIR "/bot"
VOLUME /bot/db
CMD [ "python", "app.py" ]
