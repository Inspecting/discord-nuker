# Made by phantomonic#7836

import requests
import time
import logging
import os
import json
import datetime
import concurrent.futures
import asyncio
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
message_limit = SETTINGS.get("message_limit", 50)
send_count = SETTINGS.get("send_count", 1)
message_count = 0  # Counter for number of messages sent
failed_urls = [] # List to store failed URLs
start_time = time.time() # Store start time for runtime display
concurrency = SETTINGS.get("concurrency", 10)  # Number of concurrent requests


def send_message(url, message, authorization):
    payload = {
        'content': message
    }
    response = requests.post(url, data=payload, headers={'authorization': authorization})
    if response.status_code == 200:
        success_message = f"{Fore.BLUE}Message '{message}' successfully sent to '{url}'{Fore.RESET}"
        print(success_message)
        logging.info(success_message)
    else:
        error_message = f"{Fore.RED}Error sending message '{message}'{Fore.RESET}"
        print(error_message)
        failed_urls.append(url)
        logging.error(error_message)


async def dispatch_messages(message_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        loop = asyncio.get_running_loop()
        futures = []
        for message_obj in message_list:
            for _ in range(send_count):
                url = message_obj["url"]
                message = message_obj["message"]
                futures.append(loop.run_in_executor(
                    executor,
                    send_message,
                    url,
                    message,
                    authorization
                ))
        await asyncio.gather(*futures)


async def main():
    global message_count
    while True:
        await dispatch_messages(message_list)
        message_count += len(message_list) * send_count
        if message_count % message_limit == 0:
            print(f"Pausing for {cooldown_time} seconds...")
            for i in range(cooldown_time, 0, -1):
                print(f"{Fore.YELLOW}\rResuming message sending in {i} seconds...", end="")
                await asyncio.sleep(1)
            print("\n")
        if message_count % (message_limit // 10) == 0:
            # Clear console after every 10% of message limit
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Fore.GREEN}Running.{Fore.RESET}\n")
        await asyncio.sleep(delay)  # Rate limit delay


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except Exception as e:
        error_message = f"{Fore.RED}Encountered an error: {e}{Fore.RESET}"
        print(error_message)
        logging.error(f"Encountered an error: {e}")
    finally:
        if failed_urls:
            failed_message = f"{Fore.RED}{len(failed_urls)} messages failed to send.{Fore.RESET}"
            print(failed_message)
            logging.error(failed_message)

        runtime = time.time() - start_time
        print(f"Session runtime: {datetime.timedelta(seconds=runtime)}")

        print(f"{Fore.YELLOW}Nebula Nuker stopped.{Fore.RESET}")
        logging.info("Nebula Nuker stopped.")
