from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
from bs4 import BeautifulSoup

today = datetime.now()

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_ids = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID2"]


def get_weather():
  url = "https://restapi.amap.com/v3/weather/weatherInfo?key=eeb15c5bfd597258152abaf5cf300c33&city=469028&extensions=all"
  print('获取天气url：',url)
  res = requests.get(url)
  print('获取天气结果：',res)
  print('获取天气结果JSON：',res.json())
  weather = res.json()['forecasts'][0]
  return weather['city'], weather['casts']
  
def calcPrice():
    # 链接
    url = 'https://www.ly.com/flights/itinerary/roundtrip/HGH-SYX?date=2024-07-26,2024-07-29&from=%E8%90%A7%E5%B1%B1%E6%9C%BA%E5%9C%BA&to=%E5%87%A4%E5%87%B0%E6%9C%BA%E5%9C%BA&fromairport=HGH&toairport=SYX&p=&childticket=1,0'

    # 发送GET请求
    response = requests.get(url)

    # 解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有具有特定类的标签
    airs_tags = soup.find_all('p', class_='flight-item-name')
    for tag in airs_tags:
        if tag.text == '厦门航空MF8321':
            air_name = tag.text
            index = airs_tags.index(tag)
            price_tags = soup.find_all('div', class_='head-prices')
            start_times = soup.find_all('div', class_='f-startTime f-times-con')
            end_times = soup.find_all('div', class_='f-endTime f-times-con')
            start_time = start_times[index].text.split(" ")[0]
            start_station = start_times[index].text.split(" ")[1]
            end_time = end_times[index].text.strip().split(" ")[0]
            end_station = end_times[index].text.strip().split(" ")[1]
            price = price_tags[index].text.strip()
            print(f"航空公司：{air_name}\n起飞时间：{start_time}\n起飞机场：{start_station}\n到达时间：{end_time}\n到达机场：{end_station}\n当天机票价格为：{price}")
    return air_name, start_time, start_station, end_time, end_station, price

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
city, casts = get_weather()
air_name, start_time, start_station, end_time, end_station, price = calcPrice()

data = {
    "city": {"value": city},
    "date0": {"value": casts[0]['date']},
    "date1": {"value": casts[1]['date']},
    "date2": {"value": casts[2]['date']},
    "date3": {"value": casts[3]['date']},
    "dayweather0": {"value": casts[0]['dayweather']},
    "dayweather1": {"value": casts[1]['dayweather']},
    "dayweather2": {"value": casts[2]['dayweather']},
    "dayweather3": {"value": casts[3]['dayweather']},
    "daytemp0": {"value": casts[0]['daytemp_float']},
    "daytemp1": {"value": casts[1]['daytemp_float']},
    "daytemp2": {"value": casts[2]['daytemp_float']},
    "daytemp3": {"value": casts[3]['daytemp_float']},
    "air_name": {"value": air_name},
    "start_time": {"value": start_time},
    "start_station": {"value": start_station},
    "end_time": {"value": end_time},
    "end_station": {"value": end_station},
    "price": {"value": price}
}
user_id_list = user_ids.split(",")
for user_id in user_id_list:
  res = wm.send_template(user_id, template_id, data)
  print(res)
