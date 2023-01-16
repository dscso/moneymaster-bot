#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import db as database
import json
import os

db = database.DB()
db.loadDB()

from telegram.ext import (Updater, CommandHandler)
from telegram.ext import ParseMode

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
def start(update, context):
    groupid = update.message.chat_id
    group = db.getGroup(groupid) # also creates the group if necessary
    group.addGroupMember(update.message.from_user.id)
    group.setName(update.message.from_user)
    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome! You are now added to the paying-union!")

def buy(update, context):
    buyer = update.message.from_user.id
    groupid = update.message.chat_id
    description = ""
    # arg processing
    if len(context.args) < 2:
        context.bot.send_message(chat_id=update.message.chat_id, text="`Not enought arguments!`", parse_mode='Markdown')
        return
    for i in range(0, len(context.args) - 1):
        description += (i > 0 and " " or "") + context.args[i]
    
    try:
        price = float(context.args[len(context.args) - 1])
    except ValueError:
        context.bot.send_message(chat_id=update.message.chat_id, text="`Price is not a number.`", parse_mode='Markdown')
        return
    # db stuff
    group = db.getGroup(groupid)
    group.setName(update.message.from_user)
    group.addTicket(buyer, database.Ticket(amount=price, description=description)) # add to db
    group.save()
    context.bot.send_message(chat_id=update.message.chat_id, text="Added \""+description+"\"!")

def list(update, context):
    group = db.getGroup(update.message.chat_id)
    group.setName(update.message.from_user)
    db.saveDB()
    tickets = group.getTickets()
    moneySpend:Dict[int, int] = {}
    for townerid, townerobj in tickets.items():
        moneySpend[townerid] = 0
        for ticket in townerobj:
            moneySpend[townerid] += ticket.getAmount()
    # some Math witchcraft
    totalAmount = 0
    for key,amount in moneySpend.items():
        totalAmount += amount
    if totalAmount == 0:
        context.bot.send_message(chat_id=update.message.chat_id, text="`nothing spend yet! Use /buy <name> <price> to make an entry.`", parse_mode='Markdown')
        return
    avg = totalAmount/len(moneySpend)
    response = "```Stats\nStats:\nTotal amount spend: {0:.2f}\nBalance:\n".format(totalAmount)
    # not really needed, just for name lenght determination
    maxLen = 0
    maxAvgLen = 0
    for user, amount in moneySpend.items(): # get the length of the longest number for table creation
        maxLen = maxLen < len(group.getName(user)) + len(str(round(amount))) and len(group.getName(user)) + len(str(round(amount))) or maxLen
        maxAvgLen = maxAvgLen < len("{0:.2f}".format(amount - avg)) and len("{0:.2f}".format(amount - avg)) or maxAvgLen
    for user, amount in moneySpend.items():
        space = ""
        avgspace = ""
        for x in range(maxLen - (len(group.getName(user)) + len("{0:.2f}".format(amount))) + 6): # convert numbers to spaces
            space += " "
        for x in range((maxAvgLen - len("{0:.2f}".format(amount - avg))) + 5):
            avgspace += " "
        response += "{0}{1}{2:.2f}{3}{4:.2f}\n".format(group.getName(user), space, amount, avgspace, amount - avg) # formulate response
    context.bot.send_message(chat_id=update.message.chat_id, text=response+"```", parse_mode='Markdown')


def show(update, context):
    group.setName(update.message.from_user.id, update.message.from_user)
    # ABSOLUT KEINE LUST!
    context.bot.send_message(chat_id=update.message.chat_id, text="give me the lol", parse_mode='Markdown')



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning(context.error)


def main(auth_tocken):
    updater = Updater(auth_tocken, use_context=True)
    
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('buy', buy))
    dp.add_handler(CommandHandler('b', buy))
    dp.add_handler(CommandHandler('list', list))
    dp.add_handler(CommandHandler('show', show))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    auth_tocken = os.getenv('AUTHTOCKEN', "")
    if auth_tocken == "":
        print("please define enviromental variable \"AUTHTOCKEN\"!")
        os._exit(1)
    main(auth_tocken)
