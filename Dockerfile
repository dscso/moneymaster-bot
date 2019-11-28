FROM python:3

ADD . /bot
RUN pip3 install python-telegram-bot
WORKDIR "/bot"
CMD [ "python", "app.py" ]
