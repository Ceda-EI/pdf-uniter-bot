#!/usr/bin/env python

from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import config

def on_start(upd, ctx):
    pass


def on_img_received(upd, ctx):
    pass


def on_finish(upd, ctx):
    pass


def on_cancel(upd, ctx):
    pass


updater = Updater(token=config.API_KEY, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", on_start))
dispatcher.add_handler(MessageHandler(filters.Filters.photo, on_img_received))
dispatcher.add_handler(CommandHandler("finish", on_finish))
dispatcher.add_handler(CommandHandler("cancel", on_cancel))

def main():
    "Main Function"
    updater.start_polling()


if __name__ == "__main__":
    main()
