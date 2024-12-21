import time
import requests
from flask import Flask

app = Flask(__name__)

# URL to ping
RENDER_URL = "https://vcmusicuser.onrender.com/"

# Ping the Render app every 5 minutes (300 seconds)
def keep_alive():
    while True:
        try:
            response = requests.get(RENDER_URL)
            if response.status_code == 200:
                print("Successfully pinged Render app!")
            else:
                print(f"Failed to ping. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error pinging Render app: {e}")
        time.sleep(300)  # Sleep for 5 minutes

@app.route('/')
def home():
    return "Flask app is running and pinging the Render app!"

if __name__ == '__main__':
    # Start the keep_alive function in a separate thread to keep the app alive
    import threading
    threading.Thread(target=keep_alive, daemon=True).start()
    
    # Start Flask app
    app.run(host="0.0.0.0", port=8000)
