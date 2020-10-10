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

        # 传入城市和天气信息
        msg = format_weather(weather_forecast['city'], weather_forecast['weather_forecast'])

        # f = open("text.html", 'a')  # 若文件不存在，系统自动创建。'a'表示可连续写入到文件，保留原内容，在原
        # f.write(msg)  # 将字符串写入文件中

        # days_weather = ""
        # for day in weather_forecast['weather_forecast']:
        #     days_weather += f"<h3>{day['date']}， 天气{day['cond_txt_d']}， 最高温度{day['tmp_max']}，" \
        #                     f"最低温度{day['tmp_min']}，湿度{day['hum']}， 风向{day['wind_dir']}，" \
        #                     f"风力{day['wind_sc']}级，风速{day['wind_spd']}m/s</h3>"
        # msg = f"<h2>{receiver['username']}您好，{receiver['location']}未来三日的天气预报</h2><hr>" \
        #       + days_weather + "<br><br><br><hr><small>该服务由程序自动发送</small>"

        # 使用邮箱发送
        if not send_mail.to(title, msg, receiver['email']):
            break


def format_weather(city, days_data):
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
    today = f"""<table id='index_table' width=500 border='0'>
				<tr style='height:60px'>
					<td  width=160>
					{city}
					</td>
					<td>
					</td>
					<td style='text-align:right;'  width=160>
					{time_str}
					</td>
				</tr>
				<tr>
					<td id='tmp'>
					<h1>{days_data[0]['tmp_max']}°</h1>
					</td>
					<td style='color:#8ec885'>
					<h5>{days_data[0]['cond_txt_d']}</h5>
					</td>
					<td>
					<h5>{days_data[0]['hum']}%</h5>
					</td>
				</tr>
				<tr style='height:40px'>
					<td class='tips'>
					<h6>{days_data[0]['wind_dir']} {days_data[0]['wind_sc']}级</h6>
					</td>
					<td class='tips'>
					<h6>今日天气</h6>
					</td>
					<td class='tips'>
					<h6>相对湿度</h6>
					</td>
				</tr>
			</table>"""

    content_2 = """		</div>
		<div>
		<div class='mid-body'>
		以下是未来三日的天气预报。
		</div>
		<table border="0" cellpadding="0" cellspacing="0" id='days'>
			<tr>
			<th> </th>
			<th><p>天气</p></th>
			<th><p>最高温度</p></th>
			<th><p>最低温度</p></th>
			<th><p>湿度</p></th>
			<th><p>风向</p></th>
			<th><p>风力</p></th>
			<th><p>风速</p></th>
		  </tr>"""

    content_3 = """		</table>
		<div class='footer'>
			感谢您的使用！
			<div>
			<a href='https://jiaruiblog.com'>
			<small>https://jiaruiblog.com</small>
			</a>
			</div>
		</div>
		</div>
	</div>
</body>
</html>"""

    forecast = ''
    date = ['今天', '明天', '后天']
    for i, day in enumerate(days_data):
        forecast += f"<tr>" \
                    f"<td>{date[i]}<br><small>{day['date']}</small></td>" \
                    f"<td>{day['cond_txt_d']}</td>" \
                    f"<td>{day['tmp_max']}°</td>" \
                    f"<td>{day['tmp_min']}°</td>" \
                    f"<td>{day['hum']}%</td>" \
                    f"<td>{day['wind_dir']}</td>" \
                    f"<td>{day['wind_sc']}级</td>" \
                    f"<td>{day['wind_spd']}m/s</td>" \
                    f"</tr>"

    content_1 = '''<html>
<header>
<style>
	body{
	padding:0;
	margin:0;
	}
	h1 {
	font: bold 64px sans-serif;
	margin:0px;
	vertical-align:center;
	}
	h3{
	font: normal 20px arial, sans-serif;
	margin:0px;
	vertical-align:bottom;
	}
	
	h4{
	font: normal 16px arial;
	margin:8px 0px;
	vertical-align:bottom;
	}
	
	h5{
	font: normal 20px arial, sans-serif;
	margin:0px;
	vertical-align:bottom;
	padding:20px 30px;
	}

	.page{
	margin:auto;
	width:500px;
	}


	.title{
		background-color:#262a32;
		color:#ffffff;
	}
	.container{
		display: flex;
		display: -webkit-flex; /* Safari */
	}

	
	.mid-body{
		padding:20px;
		height:30px;
	}
	
	table {
	width:100%;
	text-align: center;
	}
	th {
	height: 20px;
	border-bottom :1px solid #f3f3f3;
	color:#3e8ede;
	padding:5px;
	}
	p{
	font: 12px;
	}
	#days td {
	height: 40px;
	border-bottom :1px solid #f3f3f3;
	padding:10px;
	}
	
	.footer{
	background-color:#e6f1f7;
	height:80px;
	padding:20px;
	text-align:center;
	}
	
	#index_table{
		color:#fff;
	}
	
	.tips{
		padding:0px;
		vertical-align:top;
	}
	h6{
		margin:0px;
		font-size: 14px;
		font-weight:normal;
	}
</style>
<header>
<body>
	<div class='page'>
		<br>
		<div class='title'>'''

    result = content_1 + today + content_2 + forecast + content_3

    return result


if __name__ == '__main__':
    send_weather_to_email()
