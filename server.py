import time
import requests
from flask import Flask, jsonify, Response
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, CallbackContext
import threading

app = Flask(__name__)

# URLs to ping
URLS_TO_PING = [
    "https://vcmusicuser-xv2p.onrender.com/",
    "https://fallenrobot-04y5.onrender.com",  # New URL added previously
    "https://frozen-youtube-api-search-link-ksog.onrender.com/"  # New URL added now
]

# Dictionary to store the last ping time and status
ping_status = {url: {"last_ping": None, "status": None} for url in URLS_TO_PING}

# HTML Template
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Uptime Monitor</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f0f8f5;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .container {
            animation: fadeIn 2s;
            flex: 1;
        }
        h1 {
            color: #2d572c;
        }
        .status-success {
            color: #28a745;
            animation: greenGlow 2s infinite;
        }
        .status-failed {
            color: red;
            animation: shake 0.5s;
            animation-iteration-count: infinite;
        }
        .status-error {
            color: orange;
        }
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        @keyframes greenGlow {
            0% {
                text-shadow: 0 0 5px #28a745;
            }
            50% {
                text-shadow: 0 0 20px #28a745;
            }
            100% {
                text-shadow: 0 0 5px #28a745;
            }
        }
        @keyframes shake {
            0% { transform: translate(1px, 1px) rotate(0deg); }
            10% { transform: translate(-1px, -2px) rotate(-1deg); }
            20% { transform: translate(-3px, 0px) rotate(1deg); }
            30% { transform: translate(3px, 2px) rotate(0deg); }
            40% { transform: translate(1px, -1px) rotate(1deg); }
            50% { transform: translate(-1px, 2px) rotate(-1deg); }
            60% { transform: translate(-3px, 1px) rotate(0deg); }
            70% { transform: translate(3px, 1px) rotate(-1deg); }
            80% { transform: translate(-1px, -1px) rotate(1deg); }
            90% { transform: translate(1px, 2px) rotate(0deg); }
            100% { transform: translate(1px, -2px) rotate(-1deg); }
        }
        footer {
            text-align: center;
            padding: 10px;
            background-color: #2d572c;
            color: white;
            animation: footerGlow 3s infinite;
        }
        @keyframes footerGlow {
            0% {
                text-shadow: 0 0 5px #ffffff;
            }
            50% {
                text-shadow: 0 0 20px #ffffff;
            }
            100% {
                text-shadow: 0 0 5px #ffffff;
            }
        }
    </style>
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center">API Uptime Monitor</h1>
        <table class="table table-bordered mt-4">
            <thead>
                <tr>
                    <th>URL</th>
                    <th>Last Ping Time</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody id="status-table">
                <!-- Status rows will be inserted here by JavaScript -->
            </tbody>
        </table>
    </div>
    <footer>
        Powered by Frozen Bots
    </footer>
    <script>
        async function fetchPingStatus() {
            try {
                const response = await fetch('/ping_status');
                const data = await response.json();
                const tableBody = document.getElementById('status-table');
                tableBody.innerHTML = ''; // Clear existing rows

                for (const [url, status] of Object.entries(data)) {
                    const row = document.createElement('tr');
                    const urlCell = document.createElement('td');
                    const lastPingCell = document.createElement('td');
                    const statusCell = document.createElement('td');

                    urlCell.textContent = url;
                    lastPingCell.textContent = status.last_ping;
                    statusCell.textContent = status.status;

                    if (status.status === 'Success') {
                        statusCell.classList.add('status-success');
                    } else if (status.status.startsWith('Failed')) {
                        statusCell.classList.add('status-failed');
                    } else if (status.status.startsWith('Error')) {
                        statusCell.classList.add('status-error');
                    }

                    row.appendChild(urlCell);
                    row.appendChild(lastPingCell);
                    row.appendChild(statusCell);
                    tableBody.appendChild(row);
                }
            } catch (error) {
                console.error('Error fetching ping status:', error);
            }
        }

        // Fetch status every minute
        setInterval(fetchPingStatus, 60000);
        // Initial fetch
        fetchPingStatus();
    </script>
</body>
</html>
"""

# Ping the Render apps every 1 minute (60 seconds)
def keep_alive():
    while True:
        for url in URLS_TO_PING:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    ping_status[url] = {"last_ping": time.strftime('%Y-%m-%d %H:%M:%S'), "status": "Success"}
                    print(f"Successfully pinged {url}!")
                else:
                    ping_status[url] = {"last_ping": time.strftime('%Y-%m-%d %H:%M:%S'), "status": f"Failed - {response.status_code}"}
                    print(f"Failed to ping {url}. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                ping_status[url] = {"last_ping": time.strftime('%Y-%m-%d %H:%M:%S'), "status": f"Error - {e}"}
                print(f"Error pinging {url}: {e}")
        time.sleep(60)  # Sleep for 1 minute

@app.route('/')
def home():
    return Response(index_html, mimetype='text/html')

@app.route('/ping_status')
def get_ping_status():
    return jsonify(ping_status)

# Telegram bot setup
TELEGRAM_TOKEN = '7550365382:AAFOULp0zwiL6cPK3Ikqewot0lrhICHz4ro'
bot = Bot(token=TELEGRAM_TOKEN)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome to the monitoring bot! Use /add <URL> to add a new URL for monitoring.")

async def add(update: Update, context: CallbackContext):
    if len(context.args) == 1:
        new_url = context.args[0]
        if new_url not in URLS_TO_PING:
            URLS_TO_PING.append(new_url)
            ping_status[new_url] = {"last_ping": None, "status": None}
            await update.message.reply_text(f"Added {new_url} to monitoring list.")
        else:
            await update.message.reply_text(f"{new_url} is already being monitored.")
    else:
        await update.message.reply_text("Usage: /add <URL>")

application = Application.builder().token(TELEGRAM_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("add", add))

if __name__ == '__main__':
    # Start the keep_alive function in a separate thread to keep the app alive
    threading.Thread(target=keep_alive, daemon=True).start()
    
    # Start the Flask app
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8000)).start()
    
    # Start the Telegram bot
    application.run_polling()

