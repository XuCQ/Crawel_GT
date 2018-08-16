#coding=utf-8
import os
from bs4 import BeautifulSoup
import requests
import time
import random
from fake_useragent import UserAgent
from urllib import parse
import pandas as pd
import progressbar

def judgenet():
    try:
        os.popen("ping www.baidu.com -n 1").read()
        return ("ok")
    except(Exception):
        print('网络连接失败')
def loadinfo(results,filename):
    dataframe = pd.DataFrame(results)
    dataframe.to_csv("Data/" +filename +".csv", sep=',',encoding="utf_8_sig",mode='a',index=0,columns=list(results[0].keys()))
    print("存储ok")

station_info=[]
with open('point.txt',encoding='utf-8', errors='ignore') as f:
    line = f.readline()
    while line:
        line = f.readline()
        try:
            station=line.split(',')[1][:-1]
            station_info.append(station)
        except Exception as e:
            break

session = requests.Session()
ua=UserAgent()
target_headers = {
                  'User-Agent': ua.random,
                  }
station_url='https://shike.gaotie.cn/zhan.asp?zhan={station}'
# station_info=['南京南']
train_infos=[]
station_infos=[]
if(judgenet()=='ok'):
    with progressbar.ProgressBar(max_value=len(station_info)) as bar:
        i=0
        for station in station_info:
            bar.update(i)
            i+=1
            station_encode=station.encode('gbk')
            station_encode = parse.quote(station_encode, 'utf-8')
            try:
                response = session.get(station_url.format(station=station_encode),
                                       headers=target_headers,
                                       timeout=20)
            except Exception as e:
                print("单个页面读取失败===" + e.__str__())
                print(station, 'error',station_url.format(station=station_encode))
                continue
            try:
                html = BeautifulSoup(response.text)
                html_tr=html.find_all('tr',attrs={'bgcolor':'#ffffff'})
                infonum=0
                for info_tr in html_tr:
                    html_td =info_tr.find_all('td')
                    if len(html_td)==7:
                        # print(html_td)
                        train_id=html_td[0].text
                        departure_terminal=html_td[2].text
                        departure_terminal=departure_terminal.replace(' ','').split('-')
                        departure=departure_terminal[0]
                        terminal=departure_terminal[-1]
                        arrival_time=html_td[3].text
                        query_station=html_td[4].text
                        departure_time=html_td[5].text
                        distance_time=html_td[6].text
                        train_info={
                            'query_station': query_station,
                            'train_id': train_id,
                            'departure_station': departure,
                            'arrival_time':arrival_time,
                            'departure_time':departure_time,
                            'departure_time':departure_time,
                            'distance&time':distance_time,
                        }
                        train_infos.append(train_info)
                        # print(train_info)
                        infonum+=1
                    else:
                        continue
                # print(station,infonum)
                station_infos.append({'station':station,'infonum':infonum})
                time.sleep(random.random() * 3)
            except Exception as e:
                print('页面解析失败===',e.__str__())
                print(station, 'error',station_url.format(station=station_encode))
loadinfo(train_infos,'stationinfo')
loadinfo(station_infos,'stationinfo_summary')


