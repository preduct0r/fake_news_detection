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
import html
import json
import logging
import traceback

import configargparse
import html2text
import requests
from bs4 import BeautifulSoup
from telegram import ParseMode, Update
from telegram.ext import CommandHandler, Filters, JobQueue, MessageHandler, Updater

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

parser = configargparse.ArgParser()

parser.add_argument(
    "--telegram_token",
    type=str,
    default="5629691617:AAHPrWQv7y8ZkYMnr6lc8JTh7GyXiprBXk4",
)
parser.add_argument(
    "--error_token",
    type=str,
    default="1727154835:AAFpb9ZFwD0SAaUyyZ-wmDEVkKSoF4rqXVI",
)
# почему то error_chat_id совпадает с chat_id?
parser.add_argument(
    "--chat_id",
    type=str,
    default="406153563",
)

args = parser.parse_args()


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi!")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning(context.error)

    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an request\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML
    )
    # parsed_html = BeautifulSoup(message)
    # parsed_html = html2text.html2text(message)
    # send_text = 'https://api.telegram.org/bot' + args.error_token + '/sendMessage?chat_id=' + args.error_chat_id + '&parse_mode=Markdown&text=' + parsed_html
    # response = requests.get(send_text)


if __name__ == "__main__":
    updater = Updater(args.telegram_token, use_context=True)
    dp = updater.dispatcher
    job_queue = dp.job_queue

    def repeating_job(context):
        context.bot.send_message(chat_id=args.chat_id, text="job executed")

    job_queue.run_repeating(
        callback=repeating_job,
        interval=5,
        first=0,
    )

    dp.add_handler(CommandHandler("n", repeating_job, pass_job_queue=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
