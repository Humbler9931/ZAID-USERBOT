import asyncio
import aiohttp
import os
from pyrogram import filters, Client
from pyrogram.types import Message
from Zaid.modules.help import add_command_help

# Define the API URL for searching songs
API_URL = "https://small-bush-de65.tenopno.workers.dev/search?title="

# Define the path where songs will be temporarily downloaded
download_path = "downloads/"
os.makedirs(download_path, exist_ok=True)

@Client.on_message(filters.command(["m", "music"], ".") & filters.me)
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

        await message.edit(f"Searching for the song: `{song_name}`")

        # Fetch the YouTube link using the API
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}{song_name}") as response:
                if response.status == 200:
                    data = await response.json()
                    song_url = data.get("link")
                    song_title = data.get("title")
                    song_duration = data.get("duration")
                else:
                    await message.edit("Failed to fetch song information.")
                    return

        if not song_url:
            await message.edit("No results found for the given song.")
            return

        await message.edit(f"Found the song: `{song_title}` ({song_duration}).\nDownloading...")

        # Forward URL to the bot for downloading
        forwarded_message = await bot.send_message("@YoutubeAudioDownloadBot", song_url)

        # Wait for the bot to respond with the audio file
        bot_response = None
        for _ in range(10):  # Retry for up to 10 iterations
            async for response in bot.get_chat_history("@YoutubeAudioDownloadBot", limit=10):
                if response.audio:  # Check if the message contains an audio file
                    bot_response = response
                    break
            if bot_response:
                break
            await asyncio.sleep(2)

        if not bot_response:
            await message.edit("❌ Failed to retrieve the audio file.")
            await forwarded_message.delete()
            return

        # Download the audio file locally
        audio_file_path = await bot_response.download(file_name=download_path)

        # Clean up forwarded messages
        await asyncio.gather(
            forwarded_message.delete(),
            bot_response.delete(),
        )

        await message.edit("Uploading the song...")

        # Send the downloaded audio file
        reply_to = (
            message.reply_to_message.id
            if message.reply_to_message
            else None
        )
        await bot.send_audio(
            chat_id=message.chat.id,
            audio=audio_file_path,
            caption=f"Here is your song: `{song_title}` ({song_duration})",
            reply_to_message_id=reply_to,
        )

        # Clean up the downloaded file
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)

        await message.delete()

    except Exception as e:
        print(e)
        await message.edit("Failed to download the song.")
        await asyncio.sleep(2)
        await message.delete()

# Adding help command for the music module
add_command_help("music", [[".m `or` .music", "Search and send songs using YouTube."]])


