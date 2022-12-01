import telebot
import requests
import json
from weater_bot import time_now


API_KEY = 'YOUR KEY' # Here is your key from FatherBot
bot = telebot.TeleBot(API_KEY)


def weather(city='London'):
    API_KEY = 'YOUR KEY' # Here is your key from Openweathermap
    URL_LOCATION = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}'

    try:
        r = requests.get(URL_LOCATION).json()
        country = r[0]['country']
        lon = r[0]['lon']
        lat = r[0]['lat']
        lang = 'en'
        part = 'hourly,daily'


        with open('country_codes.json', 'r') as f:
            text = json.load(f)
        for state in text:
            if state['Code'] == country:
                state_name = state['Name']
        URL_WEATHER = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&lang={lang}'
        r_weater = requests.get(URL_WEATHER).json()
        current_datetime = time_now(lon, lat)
        weather_desription = r_weater['weather'][0]['description'].capitalize()
        temp = round(r_weater['main']['temp'] - 273.15, 1)
        temp_feel = round((r_weater['main']['feels_like'] - 273.15), 1)
        wind = r_weater['wind']['speed']
        return [weather_desription, temp, temp_feel, wind, state_name, current_datetime]
    except:
        return ["------", "------", "------", "------", "------", "------"]


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, f'Hello {message.chat.first_name} {message.chat.last_name or ""}')


@bot.message_handler(content_types=['text'])
def joker(message):
#    if message.text.isalpha():
        weather_list = weather(message.text)
        weather_message = f'City: {message.text.capitalize()}\nCountry: {weather_list[4]}\nTimezone: {weather_list[5][0]}. Current time: {weather_list[5][1]}\n{weather_list[0]}\nTemperature: {weather_list[1]}°С\nFeels like: {weather_list[2]}°С, Wind: {weather_list[3]} m/s.'
        bot.send_message(message.chat.id, weather_message)


bot.polling()