from Zaid import app, API_ID, API_HASH
from config import OWNER_ID, ALIVE_PIC
from pyrogram import filters
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

PHONE_NUMBER_TEXT = (
    "Hello user 💖 I am Frozen UB!\n\n"
    "I can help you host your own userbot.\n\n"
    "‣ Powered by FROZENBOTS 💞\n\n"
    "‣ For assistance, contact: [@FroZzeN_xD](https://t.me/FroZzeN_xD)\n\n"
    "‣ Especially designed for busy (or lazy) people 😎.\n\n"
    "‣ Use /clone followed by your Pyrogram String Session to start.\n"
    "‣ Use /login to log in without a string session."
)

@app.on_message(filters.command("start"))
async def hello(client: app, message):
    buttons = [
        [InlineKeyboardButton("📢 Channel", url="https://t.me/vibeshiftbots")],
        [InlineKeyboardButton("💬 Support Group", url="https://t.me/Frozensupport1")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_photo(
        message.chat.id,
        ALIVE_PIC,
        caption=PHONE_NUMBER_TEXT,
        reply_markup=reply_markup,
    )

@app.on_message(filters.command("clone"))
async def clone(client: app, message: Message):
    if len(message.command) < 2:
        await message.reply("Usage:\n\n`/clone <string_session>`")
        return

    session_string = message.command[1]
    text = await message.reply("Wait, booting your userbot...")

    try:
        # Initialize and start the userbot with the provided session string
        userbot_client = Client(
            name="Userbot",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_string,
            plugins=dict(root="Zaid/modules"),
        )
        await userbot_client.start()
        user = await userbot_client.get_me()
        await text.edit(
            f"Successfully ✅ booted your userbot as **{user.first_name}**!\n\n"
            "Make sure to join [Frozen Support Group](https://t.me/Frozensupport1) to avoid account suspension!"
        )
    except Exception as e:
        await text.edit(f"**ERROR:** `{str(e)}`\nPlease use /start to try again.")

@app.on_message(filters.command("login"))
async def login(client: app, message: Message):
    if len(message.command) < 2:
        await message.reply("Usage:\n\n`/login <phone_number>`")
        return

    phone_number = message.command[1]
    text = await message.reply(f"Attempting to log in with the phone number: `{phone_number}`...")

    try:
        # Start a new client instance for login
        temp_client = Client(
            "TempLogin",
            api_id=API_ID,
            api_hash=API_HASH,
            phone_number=phone_number,
            plugins=dict(root="Zaid/modules"),
        )
        await temp_client.start()
        user = await temp_client.get_me()
        await text.edit(
            f"Successfully ✅ logged in as **{user.first_name}**!\n\n"
            "Ensure to join [Frozen Support Group](https://t.me/Frozensupport1) for updates and support."
        )
    except Exception as e:
        await text.edit(f"**ERROR:** `{str(e)}`\nPlease check your phone number and try again.")

# Entry point for the application
if __name__ == "__main__":
    print("Bot is running...")
    app.run()

