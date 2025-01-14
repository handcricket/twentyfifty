from decouple import config
import requests
import sys
import telepot


MY_ID = config("MY_ID")
API_KEY = config("API_KEY")

def getSpecials():

    return 'cleanest_specials'


def send_telegram_message(msg):

    bot = telepot.Bot(API_KEY)
    bot.getMe()
    bot.sendMessage(MY_ID, msg)


if __name__ == "__main__":

    # Get the specials
    meats = getSpecials()

    send_telegram_message(meats)