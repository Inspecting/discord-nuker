import requests
import time
import logging
import os
import json

# Read settings from config.json file
with open("config.json") as f:
    SETTINGS = json.load(f)

# Set up logging
logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

channels = SETTINGS.get("channels", [])
authorization = SETTINGS.get("authorization")
message = SETTINGS.get("message")

if not channels or not authorization or not message:
    print("Error: 'channels', 'authorization', and 'message' values must be specified in config file.")
    logging.error("'channels', 'authorization', and 'message' values must be specified in config file.")
    exit()

delay = SETTINGS.get("delay", 1)  # Default delay time if no delay specified in config
cooldown_time = SETTINGS.get("cooldown_time", 60)
message_count = 0  # Counter for number of messages sent

try:
    while True:
        for channel_url in channels:
            payload = {
                'content': message
            }

            r = requests.post(channel_url, data=payload, headers={'authorization': authorization})
            if r.ok:
                success_message = f"Message successfully sent to {channel_url}: {r.json()['content']}"
                print(success_message)
                logging.info(success_message)
            else:
                error_message = f"Error sending message to {channel_url}"
                print(error_message)
                logging.error(error_message)

            message_count += 1
            if message_count % 10 == 0:
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear console

            if message_count % 100 == 0:
                print(f"Pausing for cooldown ({cooldown_time} seconds remaining)...")
                print("Paused due to too many requests.")
                for i in range(cooldown_time, 0, -1):
                    print(f"\rResuming message sending in {i} seconds...", end="")
                    time.sleep(1)
                print("\n")

            time.sleep(delay)  # Rate limit delay

except Exception as e:
    print(f"Encountered an error: {e}")
    logging.error(f"Encountered an error: {e}")
finally:
    print("Discord message sender stopped.")
    logging.info("Discord message sender stopped.")
