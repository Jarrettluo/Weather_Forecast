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
import json
from mail import SendMail


class HeWeather(object):
    def __init__(self, api_url, api_key):
        self.api_url = api_url  # api的url
        self.api_key = api_key  # api的key

    def get_data(self, location):
        url = self.api_url + '?location= ' + location + '&key=' + self.api_key
        res = requests.get(url)
        res = json.loads(res.text)  # Change the response to json.
        status = res['HeWeather6'][0]['status']  # api status.
        if status != 'ok':
            return
        forecast = res['HeWeather6'][0]['daily_forecast']
        location = res['HeWeather6'][0]['basic']
        if location['parent_city'] == location['location']:
            text = {'city': location['parent_city']}
        else:
            text = {'city': location['parent_city'] + location['location']}
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


def send_weather_to_email():
    """
        {
          "API": {
            "key": "*****************",
            "url": "https://free-api.heweather.net/s6/weather/forecast"
          },
          "SENDER": {
            "host" : "****",
            "username" : "****",
            "pwd" : "******"
          },
          "RECEIVER": [{
            "username":"****",
            "email": "*****",
            "location": "**"
          }]
        }
    :return:
    """
    # 读取配置文件
    with open('config.json', 'r', encoding='utf-8') as f:
        text = f.read()
    paras = json.loads(text)

    # 初始化天气预报数据读取
    he_weather = HeWeather(paras['API']['url'], paras['API']['key'])

    # 初始化邮件发送模块
    send_mail = SendMail(host=paras['SENDER']['host'],
                         user=paras['SENDER']['username'],
                         pwd=paras['SENDER']['pwd'])
    # 获取所有的接收者
    receivers = paras['RECEIVER']
    for receiver in receivers:
        weather_forecast = he_weather.get_data(receiver['location'])
        title = f"{weather_forecast['city']}未来3日天气预报，请查收！"
        days_weather = ""
        for day in weather_forecast['weather_forecast']:
            days_weather += f"<h3>{day['date']}， 天气{day['cond_txt_d']}， 最高温度{day['tmp_max']}，" \
                            f"最低温度{day['tmp_min']}，湿度{day['hum']}， 风向{day['wind_dir']}，" \
                            f"风力{day['wind_sc']}级，风速{day['wind_spd']}m/s</h3>"
        msg = f"<h2>{receiver['username']}您好，{receiver['location']}未来三日的天气预报</h2><hr>" \
              + days_weather + "<br><br><br><hr><small>该服务由程序自动发送</small>"
        # 使用邮箱发送
        if not send_mail.to(title, msg, receiver['email']):
            break


if __name__ == '__main__':
    send_weather_to_email()
