FROM python:3-alpine

ADD . /bot
RUN apk add py3-telegram-bot
WORKDIR "/bot"
VOLUME /bot/db
CMD [ "python", "app.py" ]
