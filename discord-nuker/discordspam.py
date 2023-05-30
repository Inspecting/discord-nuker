# Made by phantomonic#7836

import requests
import time
import logging
import os
import json
import datetime
from colorama import init, Fore

# Initialize colorama
init()

# Read settings from config.json file
with open("config.json") as f:
    SETTINGS = json.load(f)

# Set up logging
logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

discord_settings = SETTINGS.get("discord", {})
if discord_settings:
    message_list = discord_settings.get("message_list")
    authorization = discord_settings.get("authorization")
else:
    print(f"{Fore.RED}Error: 'discord' section missing from config file.{Fore.RESET}")
    logging.error("'discord' section missing from config file.")
    exit()

if not message_list or not authorization:
    print(f"{Fore.RED}Error: Discord 'message_list' and 'authorization' values must be specified in config file.{Fore.RESET}")
    logging.error("Discord 'message_list' and 'authorization' values must be specified in config file.")
    exit()

delay = SETTINGS.get("delay", 1)  # Default delay time if no delay specified in config
cooldown_time = SETTINGS.get("cooldown_time", 60)
message_count = 0  # Counter for number of messages sent
failed_urls = [] # List to store failed URLs
start_time = time.time() # Store start time for runtime display

try:
    while True:
        for message_obj in message_list:
            url = message_obj["url"]
            message = message_obj["message"]

            payload = {
                'content': message
            }

            r = requests.post(url, data=payload, headers={'authorization': authorization})
            if r.status_code == 200:
                success_message = f"{Fore.BLUE}Message '{message}' successfully sent to '{url}'{Fore.RESET}"
                print(success_message)
                logging.info(success_message)
            else:
                error_message = f"{Fore.RED}Error sending message '{message}'{Fore.RESET}"
                print(error_message)
                failed_urls.append(url)
                logging.error(f"{error_message} to '{url}'")

            message_count += 1
            if message_count % 10 == 0:
                # Clear console after every 10 messages
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"{Fore.GREEN}Running.{Fore.RESET}\n")

        if message_count % 50 == 0:
            print("Pausing for cooldown...")
            for i in range(cooldown_time, 0, -1):
                print(f"{Fore.YELLOW}\rResuming message sending in {i} seconds...", end="")
                time.sleep(1)
            print("\n") 

        time.sleep(delay)  # Rate limit delay

except Exception as e:
    error_message = f"{Fore.RED}Encountered an error: {e}{Fore.RESET}"
    print(error_message)
    logging.error(f"Encountered an error: {e}")
finally:
    if failed_urls:
        failed_message = f"{Fore.RED}The following URLs failed to send messages: {', '.join(failed_urls)}{Fore.RESET}"
        print(failed_message)
        logging.error(failed_message)

    runtime = time.time() - start_time
    print(f"Session runtime: {datetime.timedelta(seconds=runtime)}")

    print(f"{Fore.YELLOW}Discord message sender stopped.{Fore.RESET}")
    logging.info("Discord message sender stopped.")
