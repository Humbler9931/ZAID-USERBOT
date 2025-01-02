import time
import requests
from flask import Flask

app = Flask(__name__)

# URLs to ping
URLS_TO_PING = [
    "https://vcmusicuser.onrender.com/",
    "https://frozenvcmusic.onrender.com/"
]

# Ping the Render apps every 5 minutes (300 seconds)
def keep_alive():
    while True:
        for url in URLS_TO_PING:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    print(f"Successfully pinged {url}!")
                else:
                    print(f"Failed to ping {url}. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error pinging {url}: {e}")
        time.sleep(300)  # Sleep for 5 minutes

@app.route('/')
def home():
    return "Flask app is running and pinging the Render apps!"

if __name__ == '__main__':
    # Start the keep_alive function in a separate thread to keep the app alive
    import threading
    threading.Thread(target=keep_alive, daemon=True).start()
    
    # Start Flask app
    app.run(host="0.0.0.0", port=8000)
