##########import Section#############
import os #기본
from dotenv import load_dotenv #.env사용
import discord #Discord사용
from enum import Enum
## time, loop
from discord.ext import tasks
from datetime import datetime
import pytz
import csv

#######################################
##########data def Section#############
#######################################

CHANNEL_ID = 0
CHANNEL = None

lunch_data = [
    ['','','','','','','','','','','','','',''],
    ['','','','','','','','','','','','','',''],
    ['','','','','','','','','','','','','',''],
    ['','','','','','','','','','','','','',''],
    ['','','','','','','','','','','','','','']
]

weekName = { 0 : "월", 1 : "화", 2 : "수", 3 : "목",  4 : "금"}

#######################################
##########func def Section#############
#######################################

def open_csv():
    global lunch_data
    with open("lunch.csv", "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        for r in range(5) :
            for c in range(14) :
                lunch_data[r][c] = reader[c][r]
    #print(lunch_data)

async def show_lunch(day):
    message = f"# {weekName[day]}요일 메뉴\n## A\n"
    for i in range(2):
        message += f"**{lunch_data[day][i]}**\n"
    for i in range(2,7):
        message += f"{lunch_data[day][i]}\n"
    message += "## B\n"
    for i in range(7,9):
        message += f"**{lunch_data[day][i]}**\n"
    for i in range(9, 14):
        message += f"{lunch_data[day][i]}\n"

    await CHANNEL.send(message)



##############################
##########run Bot#############
##############################

@tasks.loop(minutes=1)
async def daily_lunch_alert():
    if CHANNEL == None:
        return
    tz = pytz.timezone("Asia/Seoul")
    now = datetime.now(tz)
    day = datetime.now(tz).weekday()
    if day < 0 or day > 4 :
        return

    if now.hour == 9 and now.minute == 40:
        await show_lunch(day)


async def process_message(message):
    # print("message start : ", message.content)
    if "이번주" in message.content or "전체" in message.content:
        for w in range(5):
            await show_lunch(w)
            return

    tz = pytz.timezone("Asia/Seoul")
    now = datetime.now(tz)
    day = datetime.now(tz).weekday()

    if ("월" in message.content) or ("월요일" in message.content):
        day = 0
    elif ("화" in message.content) or ("화요일" in message.content):
        day = 1
    elif ("수" in message.content) or ("수요일" in message.content):
        day = 2
    elif ("목" in message.content) or ("목요일" in message.content):
        day = 3
    elif ("금" in message.content) or ("금요일" in message.content):
        day = 4
    elif ("내일" in message.content):
        day += 1
    elif ("어제" in message.content):
        day -= 1

    if day < 0 or day > 4:
        if (day == datetime.now(tz).weekday()):
            await CHANNEL.send("오늘은 점심이 없지! 🤭")
        else:
            await CHANNEL.send("그날은 점심이 없지! 🤭")
        return
    else :
        await show_lunch(day)


