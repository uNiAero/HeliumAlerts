import ast
from discord_webhook import DiscordWebhook
import time
import requests
import json
import os

# Global Variables
# Paste your Discord webhook URL below
webhook_url = ""
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
wallet_data_new = {}
wallet_data_old = {}
discord_message = ""
wallet_difference = ""


# Pulls my wallet information from the API
def get_account_data():
    global wallet_data_new
    
    # Just paste your wallet address after https://api.helium.io/v1/accounts/
    account_endpoint = (
        "https://api.helium.io/v1/accounts/")

    account_response = requests.get(account_endpoint, headers=headers)

    print(account_response.json)
    # If response is 200
    if account_response.ok:
        to_dict = account_response.text
        wallet_data_new = json.loads(to_dict)
    else:
        time.sleep(15)
        main()


# Compares wallet balance and posts to Discord if there is an update
def get_wallet_data():
    global wallet_data_new, wallet_data_old, discord_message, wallet_difference

    # Sets value to divide balance by to display correct number of coins
    balance_to_hnt = 100000000
    wallet_difference = (wallet_data_new['data']['balance'] - wallet_data_old['data']['balance']) / balance_to_hnt

    # Updates wallet_data_old with the newest information for the next comparison
    wallet_data_old = wallet_data_new


# Updates newly created log file with first entry of wallet_data_old
def update_log_wallet_data():
    global wallet_data_new, wallet_data_old

    # Updates wallet_data_old with the newest information for the next comparison
    wallet_data_old = wallet_data_new


# Sends Discord message
def send_discord_notification():
    global discord_message, wallet_difference

    try:
        if wallet_difference != 0.0:
            discord_message = "Kaching! Reward in wallet for " + str(wallet_difference) + " HNT!"
            webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True, content=discord_message)
            response = webhook.execute()

        else:
            print("No wallet update at this time.")

    except:
        print("Error encountered when sending Discord message!")


# Write most up-to-date wallet info to file
def write_to_file():
    global wallet_data_old
    file = open("log.txt", "a")
    file.write(str(wallet_data_old) + "\n")
    file.close()


# Reads last line from log and sets it as wallet_data_old
def read_from_file():
    global wallet_data_old
    with open('log.txt') as f:
        for line in f:
            pass
            last_line = line
        wallet_data_old = ast.literal_eval(last_line)
        f.close()


# Checks to see if a log file is already created, if not it will create one and update it with the newest Wallet Info.
def create_log_file():
    if not os.path.exists("log.txt"):
        open("log.txt", 'w').close()
        get_account_data()
        update_log_wallet_data()
        write_to_file()


def main():
    global discord_message, wallet_data_old
    create_log_file()
    read_from_file()
    get_account_data()
    get_wallet_data()
    write_to_file()
    send_discord_notification()


# Runs main function before any others
if __name__ == '__main__':
    main()

