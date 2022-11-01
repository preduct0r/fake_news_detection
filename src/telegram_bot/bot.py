#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""


import datetime
import logging

import configargparse
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, JobQueue

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

parser = configargparse.ArgParser()

parser.add_argument(
    "--telegram_token",
    type=str,
    default="5629691617:AAHPrWQv7y8ZkYMnr6lc8JTh7GyXiprBXk4",
)

args = parser.parse_args()


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    
    
def repeating_job(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Setting a daily notifications!')
    
    # job_queue.run_repeating(callback = notify_assignees, 
    #                         interval = 5,
    #                         first=0,
    #                         context=update)

def notify_assignees(bot, job):
    bot.send_message(chat_id="5629691617", text="Some text!")
    
    
    
if __name__ == '__main__':
    updater = Updater(args.telegram_token, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('notify', repeating_job, pass_job_queue=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


