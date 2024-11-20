from Zaid import app, API_ID, API_HASH
from config import OWNER_ID, ALIVE_PIC
from pyrogram import filters
import os
import re
import asyncio
import time
from pyrogram import *
from pyrogram.types import * 

PHONE_NUMBER_TEXT = (
    "hello user 💖 I am frozen ub!\n\n I can help you host your own userbot \n\n‣ powered by FROZENBOTS 💞 \n\n‣ for any help owner id -: @FroZzeN_xD \n\n‣ This specially for Buzzy People's(lazy)\n\n‣ Now /clone {send your PyroGram String Session}"
)

@app.on_message(filters.command("start"))

async def hello(client: app, message):
    buttons = [
           [
                InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url="t.me/vibeshiftbots"),

            ],
            [
                InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url="t.me/Frozensuppo"),
            ],
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_photo(message.chat.id, ALIVE_PIC, caption=PHONE_NUMBER_TEXT, reply_markup=reply_markup)

# © By Itz-Zaid Your motherfucker if uh Don't gives credits.
@app.on_message(filters.command("clone"))

async def clone(bot: app, msg: Message):
    chat = msg.chat
    text = await msg.reply("Usage:\n\n /clone session")
    cmd = msg.command
    phone = msg.command[1]
    try:
        await text.edit("wait booting your own userbot.... ")
                   # change this Directry according to ur repo
        client = Client(name="Melody", api_id=API_ID, api_hash=API_HASH, session_string=phone, plugins=dict(root="Zaid/modules"))
        await client.start()
        user = await client.get_me()
        await msg.reply(f" sucessfully ✅ booted your own userbot!!{user.first_name}  ab @Frozensupport1 join karr la nahi to id ban karr du ga  ")
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to Start again.")
