FROM python:3-alpine

ADD . /bot
RUN apk get py3-telegram-bot
WORKDIR "/bot"
VOLUME /bot/db
CMD [ "python", "app.py" ]
