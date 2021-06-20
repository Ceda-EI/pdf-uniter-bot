#!/usr/bin/env python

import os
import os.path as pt

from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import config

def on_start(upd, ctx):
    message = ("Welcome to PDF Uniter.\n"
               "To get started, simply send images that will be compiled into "
               "a pdf in the order they are sent. Once completed, send /finish "
               "to receive a pdf. In case of errors, send /cancel to restart.")
    ctx.bot.send_message(upd.effective_chat.id, message)


def on_img_received(upd, ctx):
    biggest_img = list(sorted(
        upd.message.photo,
        key=lambda photo: (photo.width, photo.height),
        reverse=True
    ))[0].get_file()
    user_id = upd.effective_chat.id
    os.makedirs(f"data/{user_id}", exist_ok=True)
    existing_files = [int(i) for i in os.listdir(f"data/{user_id}")]
    if existing_files:
        new_name = max(existing_files) + 1
    else:
        new_name = 1
    biggest_img.download(f"data/{user_id}/{new_name:04}")
    ctx.bot.send_message(upd.effective_chat.id, f"Added image {new_name}")


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
