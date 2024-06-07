import asyncio
from pyrogram import filters, Client 
from pyrogram.types import Message
from pyrogram.errors import TimeoutError

# Assuming SUDO_USER and ReplyCheck are correctly imported from your modules
from Zaid import SUDO_USER
from Zaid.helper.PyroHelpers import ReplyCheck
from Zaid.modules.help import add_command_help

@Client.on_message(
    filters.command(["m", "music"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def send_music(bot: Client, message: Message):
    try:
        cmd = message.command

        # Determine the song name from the command or replied message
        song_name = ""
        if len(cmd) > 1:
            song_name = " ".join(cmd[1:])
        elif message.reply_to_message and len(cmd) == 1:
            song_name = (
                message.reply_to_message.text or message.reply_to_message.caption
            )
        elif not message.reply_to_message and len(cmd) == 1:
            await message.edit("Please provide a song name.")
            await asyncio.sleep(2)
            await message.delete()
            return

        # Fetch the song using the inline bot
        song_results = await bot.get_inline_bot_results("vkmusic_bot", song_name)

        try:
            # Send the result to Saved Messages as hide_via doesn't work sometimes
            saved = await bot.send_inline_bot_result(
                chat_id="me",
                query_id=song_results.query_id,
                result_id=song_results.results[0].id,
            )

            # Forward the saved message to the target chat
            saved_message = await bot.get_messages("me", int(saved.updates[1].message.id))
            reply_to = (
                message.reply_to_message.id
                if message.reply_to_message
                else None
            )
            await bot.send_audio(
                chat_id=message.chat.id,
                audio=str(saved_message.audio.file_id),
                reply_to_message_id=ReplyCheck(message),
            )

            # Delete the message from Saved Messages
            await bot.delete_messages("me", saved_message.id)
        except TimeoutError:
            await message.edit("The request timed out.")
            await asyncio.sleep(2)
        await message.delete()
    except Exception as e:
        print(e)
        await message.edit("Failed to find the song.")
        await asyncio.sleep(2)
        await message.delete()

# Adding help command for the music module
add_command_help("music", [[".m `or` .music", "Search and send songs."]])

