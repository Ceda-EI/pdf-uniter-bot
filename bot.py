#!/usr/bin/env python

import os
import os.path as pt
import shutil
import subprocess

from telegram.parsemode import ParseMode as Parse
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import config

def on_start(upd, ctx):
    message = (
        "<b>Welcome to PDF Uniter</b>\n\n"
        "To get started, simply send images that will be compiled into a pdf "
        "in the order they are sent.\n\n"
        "- Once completed, send /finish to receive a pdf.\n"
        "- To set a different filename, use <code>/finish filename.</code>\n"
        "- In case of errors, send /cancel to restart.\n"
    )
    ctx.bot.send_message(upd.effective_chat.id, message, parse_mode=Parse.HTML)


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
    user_id = upd.effective_chat.id
    path = f"data/{user_id}"
    if not pt.isdir(path):
        ctx.bot.send_message(upd.effective_chat.id, "No Images Available")
        return

    ctx.bot.send_message(upd.effective_chat.id, "Started Merging")
    files = list(sorted(
        os.listdir(path),
        key=lambda file: int(file)
    ))
    pdf_path = f"{path}/final.pdf"
    subprocess.run(["convert", *[path + "/" + file for file in files], pdf_path])

    _, *filename = upd.message.text.split(" ")
    if filename:
        filename = " ".join(filename).rstrip(".pdf") + ".pdf"
    else:
        filename = "final.pdf"
    with open(pdf_path, "rb") as f:
        ctx.bot.send_document(upd.effective_chat.id, f, filename=filename)
    shutil.rmtree(path)



def on_cancel(upd, ctx):
    user_id = upd.effective_chat.id
    path = f"data/{user_id}"
    if pt.isdir(path):
        shutil.rmtree(f"data/{user_id}")
    ctx.bot.send_message(upd.effective_chat.id, "Cleared images")


updater = Updater(token=config.API_KEY, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", on_start))
dispatcher.add_handler(CommandHandler("help", on_start))
dispatcher.add_handler(MessageHandler(filters.Filters.photo, on_img_received))
dispatcher.add_handler(CommandHandler("finish", on_finish))
dispatcher.add_handler(CommandHandler("cancel", on_cancel))

def main():
    "Main Function"
    updater.start_polling()


if __name__ == "__main__":
    main()
