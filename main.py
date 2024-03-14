import telebot
import requests
import json
import emoji

with open('country_data.json', 'r', encoding='utf-8') as file:
    countries_data = json.load(file)

bot = telebot.TeleBot('7076800111:AAGbQtHV1mVGm6WMca2ysWHCTywish0YKgc')

openweather_api_key = '1369dd6b5ae78fc9952261ab9aa236b4'

def get_flag_emoji(country_code):
    base = 127462 - ord('A')
    return chr(ord(country_code[0]) + base) + chr(ord(country_code[1]) + base)

def get_country_info(country_name):
    for country in countries_data:
        if country['name']['common'].lower() == country_name.lower():
            return country
    return "Country not found."

def get_weather_info(capital_city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={capital_city}&appid={openweather_api_key}&units=metric'
    response = requests.get(url).json()
    return response

def create_response_message(country_info, weather_info):
    try:
        weather_description = weather_info['weather'][0]['description']
        temperature = weather_info['main']['temp']
    except KeyError:
        weather_description = "No weather data available."
        temperature = "N/A"

    flag_emoji = get_flag_emoji(country_info['cca2'])

    message = (
        f"{flag_emoji} Country: {country_info['name']['common']}\n"
        f"{emoji.emojize('🏛️')} Capital: {', '.join(country_info['capital'])}\n"
        f"{emoji.emojize('💬')} Language: {', '.join(country_info['languages'].values())}\n"
        f"{emoji.emojize('💸')} Currency: {', '.join([f'{currency_data['name']} ({currency_data['symbol']})' for currency_data in country_info['currencies'].values()])}\n"
        f"{emoji.emojize('👥')} Population: {country_info['population']}\n"
        f"{emoji.emojize('🌡️')} Weather: {weather_description}, {emoji.emojize('🌡️')} Temperature: {temperature}°C"
    )
    return message

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me a country name and I'll provide you with its information and current weather.")

@bot.message_handler(func=lambda message: True)
def send_country_info(message):
    country_name = message.text.strip()
    country_info = get_country_info(country_name)
    if isinstance(country_info, str):
        bot.reply_to(message, country_info)
    else:
        capital_city = country_info['capital'][0]
        weather_info = get_weather_info(capital_city)
        response_message = create_response_message(country_info, weather_info)
        bot.reply_to(message, response_message)

bot.polling()
