# encoding: utf-8
"""
@version: 1.0
@author: 
@file: main.py
@time: 2020/2/10 22:18
"""

import requests
import json
import csv
import datetime

# from SendEmail.sendemail import *

KEY = "ac123eeb7c16456a87a5ec3d322f09ff"
CITY = "彭山"
APIURL = "https://free-api.heweather.net/s6/weather/forecast"
USERNAME = ""
receiver = 'qiuyujie23@163.com'


# automail(title,msg,receiver)

class HeWeather(object):
    def __init__(self):
        pass

    def get_data(self):
        url = APIURL + '?location= ' + CITY + '&key=' + KEY
        res = requests.get(url)
        res = json.loads(res.text)  # Change the response to json.
        status = res['HeWeather6'][0]['status']  # api status.
        if status != 'ok':
            return
        forecast = res['HeWeather6'][0]['daily_forecast']
        location = res['HeWeather6'][0]['basic']
        text = {'city': location['parent_city'] + location['location']}  # add city key.
        msg = []
        for data in forecast:
            date = data['date']
            cond_txt_d = data['cond_txt_d']  # weather 天气描述
            tmp_max = data['tmp_max']  # max temperature.
            tmp_min = data['tmp_min']  # min tempereture.
            hum = data['hum']  # humanity
            wind_dir = data['wind_dir']  # wind direction.
            wind_sc = data['wind_sc']  # wind degree.
            wind_spd = data['wind_spd']  # wind speed.
            msg.append({"date": date,
                        "cond_txt_d": cond_txt_d,
                        "tmp_max": tmp_max,
                        "tmp_min": tmp_min,
                        "hum": hum,
                        "wind_dir": wind_dir,
                        "wind_sc": wind_sc,
                        "wind_spd": wind_spd})
        text['weather_forecast'] = msg
        return text


if __name__ == '__main__':
    he_weather = HeWeather()
    weather_forecast = he_weather.get_data()
    print(weather_forecast)
