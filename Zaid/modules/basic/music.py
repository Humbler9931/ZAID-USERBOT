import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message
import yt_dlp
import os
from Zaid.modules.help import add_command_help

# Define the path where songs will be temporarily downloaded
download_path = "downloads/"
os.makedirs(download_path, exist_ok=True)

# Define the path to cookies file
cookies_path = "cookies.txt"  # Make sure to place your cookies file here

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

        # yt-dlp options for extracting song link
        ydl_opts = {
            "quiet": True,
            "format": "bestaudio/best",
            "cookiefile": cookies_path,
        }

        # Search for the song and get the URL
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch:{song_name}", download=False)
            song_info = search_results["entries"][0]  # First result
            song_url = song_info["webpage_url"]

        await message.edit(f"Found the song: [{song_info['title']}]({song_url}).\nDownloading...")

        # yt-dlp options for downloading the song
        ydl_opts_download = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": f"{download_path}%(title)s.%(ext)s",
            "quiet": True,
            "cookiefile": cookies_path,
        }

        # Download the song
        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
            info = ydl.extract_info(song_url, download=True)
            file_path = ydl.prepare_filename(info)
            audio_file = f"{os.path.splitext(file_path)[0]}.mp3"

        await message.edit("Uploading the song...")

        # Send the audio file
        reply_to = (
            message.reply_to_message.id
            if message.reply_to_message
            else None
        )
        await bot.send_audio(
            chat_id=message.chat.id,
            audio=audio_file,
            caption=f"Here is your song: [{song_info['title']}]({song_url})",
            reply_to_message_id=reply_to,
        )

        # Clean up the downloaded file
        if os.path.exists(audio_file):
            os.remove(audio_file)

        await message.delete()

    except Exception as e:
        print(e)
        await message.edit("Failed to download the song.")
        await asyncio.sleep(2)
        await message.delete()

# Adding help command for the music module
add_command_help("music", [[".m `or` .music", "Search and send songs using YouTube."]])


