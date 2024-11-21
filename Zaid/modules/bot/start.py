from pyrogram import filters, Client
from pyrogram.types import *
from config import OWNER_ID, ALIVE_PIC, API_ID, API_HASH

PHONE_NUMBER_TEXT = (
    "Hello Master 👋!\n\n"
    "I am your assistant userbot 🤖.\n\n"
    "‣ I can help you host and manage your userbot sessions.\n\n"
    "‣ Repo: [GitHub Repository](https://github.com/Itz-Zaid/Zaid-Userbot)\n\n"
    "‣ This is designed for busy (or lazy) people 😌.\n\n"
    "‣ Use /clone {send your Pyrogram String Session} to get started!"
)

# Initialize the bot client
app = Client(
    "FrozenUB",
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="Zaid/modules"),  # Update plugin directory if needed
)

@app.on_message(filters.user(OWNER_ID) & filters.command("start"))
async def hello(client, message):
    buttons = [
        [InlineKeyboardButton("✘ Updates Channel", url="t.me/vibeshiftbots")],
        [InlineKeyboardButton("✘ Support Group", url="t.me/frozensupport1")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_photo(
        message.chat.id,
        ALIVE_PIC,
        caption=PHONE_NUMBER_TEXT,
        reply_markup=reply_markup
    )

@app.on_message(filters.user(OWNER_ID) & filters.command("clone"))
async def clone(client, message):
    if len(message.command) < 2:
        await message.reply("Usage:\n\n/clone <session_string>")
        return

    phone = message.command[1]
    text = await message.reply("Wait, booting your userbot client...")
    
    try:
        # Start the userbot client with the provided session string
        cloned_client = Client(
            name="ClonedBot",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=phone,
            plugins=dict(root="Zaid/modules")
        )
        await cloned_client.start()
        user = await cloned_client.get_me()
        await text.edit(f"Your client has been successfully booted as **{user.first_name}** ✅.")
    except Exception as e:
        await text.edit(f"**ERROR:** `{str(e)}`\nPlease use /start to try again.")

# Entry point for the application
if __name__ == "__main__":
    print("Bot is running...")
    app.run()

