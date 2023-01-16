FROM python:3.7-slim-buster

ADD . /bot
RUN pip install "python_telegram_bot==12.4.2"
WORKDIR "/bot"
VOLUME /bot/db
CMD [ "python", "app.py" ]
