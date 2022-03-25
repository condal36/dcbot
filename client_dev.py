#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/19 下午 07:27
# @Author : condal36
# @Site : 
# @File : enlinebot_command.py
# @Software: PyCharm
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get
from discord import FFmpegPCMAudio
from asyncio import run_coroutine_threadsafe as rct
from pytube import YouTube
import random
import asyncio
import datetime
import requests
import json

######################取得設定檔########################
load_dotenv()
TOKEN = os.getenv('DISCORD_DEV_TOKEN')
DAILY_CUTE = os.getenv('DAILY_CUTE_DIR')
GLOBAL_WEATHER_URL = os.getenv('GLOBAL_WEATHER_URL')
WEATHER_AUTHORIZATION=os.getenv('WEATHER_AUTH')
BIBO = int(os.getenv('BIBO'))
PUTINUM = int(os.getenv('PUTI'))

###################SETTING PARAMETER####################
song_queue = []
PUTILASTTIME=datetime.date(2022,3,18)
GGREPLY=['機...油..好...難...喝...逼逼逼逼','逼啵!','我們是機器人台','你已被管理員史丹利(relaxing234) 永久禁言']
client = discord.Client()



#######################FUNC##########################
def get_weather_global(City):

    url = GLOBAL_WEATHER_URL
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        data = json.loads(response.text)
        file = open(f'./weather/{City}', "w+")
        json.dump(data, file)
        file.close()
        localsites=data["cwbopendata"]["dataset"]["location"]
        for localsite in localsites:
            if(localsite["locationName"]==City):
                weather_elements = localsite["weatherElement"]
                start_time = weather_elements[0]["time"][0]["startTime"]
                end_time = weather_elements[0]["time"][0]["endTime"]
                weather_state = weather_elements[0]["time"][0]["elementValue"][0]["value"]
                rain_prob = weather_elements[0]["time"][0]["elementValue"][1]["value"]
                min_tem = weather_elements[2]["time"][0]["elementValue"]["value"]
                max_tem = weather_elements[1]["time"][0]["elementValue"]["value"]
                return(localsite["locationName"]+"天氣:"+weather_state+"\n降雨機率:"+rain_prob+" 氣溫:"+min_tem+"到"+max_tem+" 時間:"+start_time+" ~ "+end_time)  
        return "Can't get data!"
    else:
        return "Can't get data!"

def get_weather_data(City):

    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": WEATHER_AUTHORIZATION,
        "locationName": City,
    }
    print(City)
    response = requests.get(url, params=params)
    print(response.status_code)

    if response.status_code == 200:
        print(response.text)
        data = json.loads(response.text)
        file = open(f'./weather/{City}', "w+")
        json.dump(data, file)
        file.close()
        location = data["records"]["location"][0]["locationName"]
        if(len(location)!=0):
            weather_elements = data["records"]["location"][0]["weatherElement"]
            start_time = weather_elements[0]["time"][0]["startTime"]
            end_time = weather_elements[0]["time"][0]["endTime"]
            weather_state = weather_elements[0]["time"][0]["parameter"]["parameterName"]
            rain_prob = weather_elements[1]["time"][0]["parameter"]["parameterName"]
            min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"]
            comfort = weather_elements[3]["time"][0]["parameter"]["parameterName"]
            max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"]
            return(location+"天氣:"+weather_state+"\n降雨機率:"+rain_prob+" 體感:"+comfort+" 氣溫:"+min_tem+"到"+max_tem+" 時間:"+start_time+" ~ "+end_time)
        else:
            return "Can't get data!"
    else:
        return "Can't get data!"

def bird_shell():
    return random.randint(1,3)
def get_time_distance(datenew,dateold):
    return int((datenew - dateold).days)
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    game = discord.Game('機...油..好...難...喝...逼逼逼逼')
    await client.change_presence(status=discord.Status.idle, activity=game)
    print('------')
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if '菩提花' in message.author.name:
        global PUTILASTTIME
        todaydate = datetime.datetime.now().date()
        PUTILASTTIME = todaydate
        datedistance = get_time_distance(todaydate,PUTILASTTIME)
        if (datedistance > 2):
            perparemessage=f'菩提已經{datedistance}天沒說話了，大家好想你啊!剛從地下室出來?'
            await message.channel.send(perparemessage,reference=message)
    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')
    if '雞' in message.content.lower():
        await message.channel.send('母雞好可愛<3')
    if '胖' in message.content.lower():
        await message.channel.send('真的超胖')
    if '機器人' in message.content.lower():
        await message.channel.send(random.choice(GGREPLY),reference=message)
    if 'dailycute' in message.content.lower():
        await message.channel.send(file=discord.File(DAILY_CUTE+random.choice(os.listdir(DAILY_CUTE))),reference=message)
    if '嗨' in message.content.lower():
        await message.channel.send('Hello!', reference=message)
    if 'BOT' in message.content.lower():
        await message.channel.send('BNT?',reference=message)
    if '菩提' in message.content.lower():
        if bird_shell() % PUTINUM == 1:
            t=get_time_distance(datetime.datetime.now().date(),PUTILASTTIME)
            await message.channel.send(f'菩提不知道從地下室出來了沒?他已經{t}天沒說話了',reference=message)
    if '天氣' in message.content.lower():
        tmpreturn=get_weather_data(message.content.lower().split()[1])
        await message.channel.send(tmpreturn)
    if '海上' in message.content.lower():
        tmpreturn=get_weather_global(message.content.lower().split()[1])
        await message.channel.send(tmpreturn)
    if '清除鳥語' in message.content.lower():
        async for message in message.channel.history(limit = 1000):
            if message.author.id == client.user.id  :
                await message.delete()
    if '清除逼波' in message.content.lower():
        async for message in message.channel.history(limit = 1000):
            if message.author.id == BIBO :
                await message.delete()
client.run(TOKEN)