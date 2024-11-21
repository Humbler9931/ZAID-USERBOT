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

# Temporary storage for login sessions
temp_login_sessions = {}


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
    chat_id = message.chat.id

    if chat_id in temp_login_sessions:
        await message.reply("⚠️ A login process is already in progress. Please complete it first.")
        return

    await message.reply("Please enter your phone number with the country code (e.g., `+914017898912`).")
    temp_login_sessions[chat_id] = {"stage": "phone"}


@app.on_message(filters.text & ~filters.command)
async def handle_login_steps(client: app, message: Message):
    chat_id = message.chat.id

    if chat_id not in temp_login_sessions:
        return  # Ignore unrelated messages

    login_session = temp_login_sessions[chat_id]
    stage = login_session.get("stage")

    # Step 1: Phone number
    if stage == "phone":
        phone_number = message.text.strip()
        login_session["phone_number"] = phone_number
        try:
            temp_client = Client("TempLogin", api_id=API_ID, api_hash=API_HASH)
            await temp_client.connect()
            sent_code = await temp_client.send_code(phone_number)
            login_session["temp_client"] = temp_client
            login_session["code_hash"] = sent_code.phone_code_hash
            login_session["stage"] = "otp"
            await message.reply(
                f"🔑 Code sent to `{phone_number}`.\n\nPlease enter the code in the format `1 3 5 7` (with spaces)."
            )
        except Exception as e:
            del temp_login_sessions[chat_id]
            await message.reply(f"**ERROR:** `{str(e)}`\nPlease check your phone number and try again.")

    # Step 2: OTP
    elif stage == "otp":
        otp_code = "".join(message.text.split())  # Remove spaces
        temp_client = login_session.get("temp_client")
        phone_number = login_session.get("phone_number")
        code_hash = login_session.get("code_hash")
        try:
            await temp_client.sign_in(phone_number, otp_code, phone_code_hash=code_hash)
            user = await temp_client.get_me()
            await message.reply(
                f"✅ Successfully logged in as **{user.first_name}**!\n\n"
                "If 2FA is enabled, please provide your password."
            )
            login_session["stage"] = "2fa"
        except Exception as e:
            if "2FA" in str(e):
                login_session["stage"] = "2fa"
                await message.reply("🔒 2-Step Verification is enabled. Please enter your password.")
            else:
                del temp_login_sessions[chat_id]
                await message.reply(f"**ERROR:** `{str(e)}`\nPlease check the code and try again.")

    # Step 3: 2FA Password
    elif stage == "2fa":
        password = message.text.strip()
        temp_client = login_session.get("temp_client")
        try:
            await temp_client.sign_in(password=password)
            user = await temp_client.get_me()
            await message.reply(
                f"✅ Successfully logged in as **{user.first_name}**!\n\nYour userbot is now ready!"
            )
            del temp_login_sessions[chat_id]
        except Exception as e:
            await message.reply(f"**ERROR:** `{str(e)}`\nPlease check your password and try again.")

    # Final cleanup
    if chat_id in temp_login_sessions and login_session.get("temp_client"):
        await login_session["temp_client"].disconnect()
        del temp_login_sessions[chat_id]


if __name__ == "__main__":
    print("Bot is running...")
    app.run()

