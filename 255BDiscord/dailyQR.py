import os #기본
from dotenv import load_dotenv #.env사용
import discord #Discord사용
from enum import Enum
## time, loop
from discord.ext import tasks
from datetime import datetime
import pytz
import csv
import random

#######################################
##########data def Section#############
#######################################

CHANNEL_ID = 0
CHANNEL = None


##############################
##########run Bot#############
##############################
@tasks.loop(minutes=1)
async def daily_qr_alert():
    if CHANNEL == None:
        return

    tz = pytz.timezone("Asia/Seoul")
    now = datetime.now(tz)
    day = datetime.now(tz).weekday()

    if day < 0 or day > 4 :
        return

    #등원알림
    if now.hour == 9 and now.minute == 55:
        with open("helloQR.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            rand_index = random.randint(0, len(lines) - 1)
            await CHANNEL.send(lines[rand_index])
    
    #하원알림
    if now.hour == 17 and now.minute == 0:
        with open("byeQR.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            rand_index = random.randint(0, len(lines) - 1)
            await CHANNEL.send(lines[rand_index])

async def process_message(message):
    await CHANNEL.send("왜 불러 :) 심심해?")