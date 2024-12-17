from pyrogram import Client
from config import (
    API_ID, API_HASH, SUDO_USERS, OWNER_ID, BOT_TOKEN,
    STRING_SESSION1, STRING_SESSION2, STRING_SESSION3, STRING_SESSION4,
    STRING_SESSION5, STRING_SESSION6, STRING_SESSION7, STRING_SESSION8,
    STRING_SESSION9, STRING_SESSION10
)
from datetime import datetime
import asyncio
import time
from aiohttp import ClientSession

# Initialization
StartTime = time.time()
START_TIME = datetime.now()
CMD_HELP = {}
SUDO_USER = SUDO_USERS
clients = []
ids = []

# Ensure OWNER_ID is in SUDO_USERS
if OWNER_ID not in SUDO_USERS:
    SUDO_USERS.append(OWNER_ID)

# Default API_ID and API_HASH
if not API_ID:
    print("WARNING: API ID NOT FOUND. USING DEFAULT Frozen API ⚡")
    API_ID = "6435225"

if not API_HASH:
    print("WARNING: API HASH NOT FOUND. USING DEFAULT Frozen API ⚡")
    API_HASH = "4e984ea35f854762dcde906dce426c2d"

if not BOT_TOKEN:
    print("ERROR: BOT TOKEN NOT FOUND. PLEASE ADD IT! ⚡")
    exit(1)

# Create an aiohttp session
aiosession = None

async def initialize_session():
    global aiosession
    if not aiosession:
        aiosession = ClientSession()

# Bot Client
app = Client(
    name="app",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Zaid/modules/bot"),
    in_memory=True,
)

# Add user clients using STRING_SESSION variables
async def start_user_clients():
    session_strings = [
        STRING_SESSION1, STRING_SESSION2, STRING_SESSION3, STRING_SESSION4,
        STRING_SESSION5, STRING_SESSION6, STRING_SESSION7, STRING_SESSION8,
        STRING_SESSION9, STRING_SESSION10
    ]
    
    for i, session_string in enumerate(session_strings, start=1):
        if session_string:
            print(f"Client{i}: Found.. Starting.. 📳")
            client = Client(
                name=f"client{i}",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=session_string,
                plugins=dict(root="Zaid/modules")
            )
            clients.append(client)

# Main function to start all clients
async def main():
    await initialize_session()
    await start_user_clients()
    print("All clients initialized successfully.")

    # Start all clients
    for client in clients:
        await client.start()
    await app.start()
    print("Bot and all user clients are running!")

    # Keep the bot running
    await asyncio.Event().wait()

# Run the main loop
if __name__ == "__main__":
    asyncio.run(main())

