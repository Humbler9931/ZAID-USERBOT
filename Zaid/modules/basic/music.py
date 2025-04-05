import asyncio
import aiohttp
import os
from pyrogram import filters, Client
from pyrogram.types import Message
from Zaid.modules.help import add_command_help

# Define the JioSaavn API URL for searching songs
API_URL = "https://jiosaavn-api.lagendplayersyt.workers.dev/api/search/songs?query="

@Client.on_message(filters.command(["m", "music"], ".") & filters.me)
async def send_music(bot: Client, message: Message):
    try:
        cmd = message.command

        # Determine the song name from the command or replied message
        song_name = ""
        if len(cmd) > 1:
            song_name = " ".join(cmd[1:])
        elif message.reply_to_message and len(cmd) == 1:
            song_name = message.reply_to_message.text or message.reply_to_message.caption
        elif not message.reply_to_message and len(cmd) == 1:
            await message.edit("Please provide a song name.")
            await asyncio.sleep(2)
            await message.delete()
            return

        await message.edit(f"Searching for the song: `{song_name}`")

        # Fetch the song info using the JioSaavn API
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}{song_name}") as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get("data", {}).get("results", [])
                    # Filter out songs where the language is "instrumental"
                    valid_results = [song for song in results if song.get("language", "").lower() != "instrumental"]
                    if not valid_results:
                        await message.edit("No non-instrumental results found for the given song.")
                        return
                    # Select the first valid (non-instrumental) result
                    chosen_song = valid_results[0]
                    song_url = chosen_song.get("url")
                    song_title = chosen_song.get("name")
                    song_duration = chosen_song.get("duration")
                else:
                    await message.edit("Failed to fetch song information.")
                    return

        if not song_url:
            await message.edit("No results found for the given song.")
            return

        await message.edit(f"Found the song: `{song_title}` ({song_duration}).\nForwarding for download...")

        # Forward the song URL to the downloader bot
        forwarded_message = await bot.send_message("@songdownloderfrozenbot", song_url)

        # Wait for the downloader bot to respond with the audio file
        bot_response = None
        for _ in range(10):  # Retry for up to 10 iterations
            async for response in bot.get_chat_history("@songdownloderfrozenbot", limit=10):
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

        await message.edit("Forwarding the song...")

        # Forward the received audio message directly to the current chat
        reply_to = message.reply_to_message.id if message.reply_to_message else None
        await bot.forward_messages(
            chat_id=message.chat.id,
            from_chat_id="@songdownloderfrozenbot",
            message_ids=bot_response.message_id,
            reply_to_message_id=reply_to,
        )

        # Optionally clean up the temporary messages
        await asyncio.gather(
            forwarded_message.delete(),
            bot_response.delete(),
        )

        await message.delete()

    except Exception as e:
        print(e)
        await message.edit("Failed to forward the song.")
        await asyncio.sleep(2)
        await message.delete()

# Adding help command for the music module
add_command_help("music", [[".m `or` .music", "Search and forward songs using JioSaavn."]])



