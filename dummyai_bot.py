"""Main Bot program."""

import os

from flask import Flask
from flask import request
import telebot
from telebot import types
from tokenfile import botToken
import botweather

bot = telebot.TeleBot(botToken)
server = Flask(__name__)


@bot.message_handler(commands=['weather'])
def handle_weather(message):
    if len(message.text) < 9:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard_agree = types.KeyboardButton('Sure, what could go wrong?', request_location=True)
        markup.row(keyboard_agree)
        bot.send_message(message.chat.id, "Share your location, ot type '/weather <your_city>'.", reply_markup=markup)
    else:
        a = botweather.type_weather(message.text[9:len(message.text)])
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, a, reply_markup=markup)


@bot.message_handler(content_types=["location"])
def we_got_location(message):
    if message.location:
        lat = message.location.latitude
        lon = message.location.longitude
        a = botweather.ask_weather(lat, lon)
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, a, reply_markup=markup)
    else:
        bot.reply_to(message.text, 'hey')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    start_msg = ("""
Hi there!
This bot can tell you about current weather at your location.
Or you can tell him your city by typing it in chat!
Just don't forget to use commands, okay?
Right now it's pretty basic.
But hey, little later I'll teach him some more tricks.
You can always ask me a question or tell me about bugs.
To see my contacts, just type /info.
To get some help, just type /help.
        """)
    bot.reply_to(message, start_msg)


@bot.message_handler(commands=['help'])
def send_help(message):
    help_msg = ("""
So here we are, right?
For now, this bot knows only 4 commands.
Type /weather, to get current weather on your location.
Type /weather <city>, to get weather in <city>.
Type /start, to see start message(oh well, maybe you liked it).
Type /help, to see help message(you don't say huh?).
Type /info, to get some info about developer(that's me).
        """)
    bot.reply_to(message, help_msg)


@bot.message_handler(commands=['info'])
def send_info(message):
    info_msg = ("""
This bot created by @dunaldo
Feel free to email me at dunaldo66@gmail.com
If you want to run this bot or look "under the hood", get it on git-hub.
www.linkishere.com
If you like this bot, you can rate it at:
https://telegram.me/storebot?start=dummyai_bot
        """)
    bot.reply_to(message, info_msg)


@server.route('/' + botToken, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "200 OK", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(
        url='https://dummyaibot.herokuapp.com/' + botToken)
    return "200 OK", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
