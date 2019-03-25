import json
import urllib.request
import time
import datetime

import smtplib
import ssl


def weather_forecast(city_name):
    url_first_half = "http://api.openweathermap.org/data/2.5/weather?q="
    url_second_half = ",us&appid=8da995db2c96601bd55534c67e8856db"
    full_url = url_first_half + city_name + url_second_half

    response = urllib.request.urlopen(full_url)
    result = json.loads(response.read())

    time_stamp = result["dt"]  # Time of weather report
    weather_description = result["weather"][0]["main"]  # Description of the weather
    current_temperature = result["main"]["temp"]  # Current temperature
    min_temperature = result["main"]["temp_min"]  # Min temperature
    max_temperature = result["main"]["temp_max"]  # Max temperature

    # Converting Temperature from kevin to fahrenheit
    current_temperature = round(temp_k_to_f(current_temperature), 2)
    min_temperature = round(temp_k_to_f(min_temperature), 2)
    max_temperature = round(temp_k_to_f(max_temperature), 2)

    weather_list = [weather_description, current_temperature, min_temperature, max_temperature, time_stamp]

    return weather_list


def temp_k_to_f(kevin):
    fahrenheit = (kevin - 273.15) * (9 / 5) + 32

    return fahrenheit


def email_weather(city_name, weather_list, email_information):
    port = 587
    smtp_server = "smtp.gmail.com"

    sender_email = email_information[0]
    password = email_information[1]
    receiver_email = email_information[2]

    weather_description = weather_list[0]
    current_temperature = weather_list[1]
    min_temperature = weather_list[2]
    max_temperature = weather_list[3]
    time_stamp = weather_list[4]

    # Main body content is typed here to be sent.
    message = """\
    Subject: Weather for {0}

    {1} Weather Status: {2}

    Current Temperature: {3} F
    High  Temperature: {4} F
    Low   Temperature: {5} F
    """.format(time.ctime(time_stamp), city_name, weather_description,
               current_temperature, max_temperature, min_temperature)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


city = "Irvine"

userName = input("Gmail account: ")
userPassword = input("Password: ")
receiverName = input("Send to: ")

emailInformation = [userName, userPassword, receiverName]

while True:
    dt = datetime.datetime.now()  # Current time

    if dt.strftime('%I:%M %p') == '06:00 AM':
        todayWeather = weather_forecast(city)
        email_weather(city, todayWeather, emailInformation)
        time.sleep(60)
    else:
        time.sleep(1)
