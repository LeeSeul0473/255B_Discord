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

load_dotenv()
PLAYER1 = os.getenv('PLAYER1')
PLAYER2 = os.getenv('PLAYER2')
PLAYER3 = os.getenv('PLAYER3')
PLAYER2_2 = os.getenv('PLAYER2_2')
PLAYER3_2 = os.getenv('PLAYER3_2')

class State(Enum):
    SUCCESS = '성공!'
    FAIL = '실패'
    NONE = '미 인증'

current_challenge_state = {
    PLAYER1 : [ State.NONE,State.NONE,State.NONE,State.NONE,State.NONE ],
    PLAYER2 : [ State.NONE,State.NONE,State.NONE,State.NONE,State.NONE ],
    PLAYER3 : [ State.NONE,State.NONE,State.NONE,State.NONE,State.NONE ],
    }

weekName = { 0 : "월", 1 : "화", 2 : "수", 3 : "목",  4 : "금"}

player_stack = []
week_stack = []

#######################################
##########func def Section#############
#######################################
def add_player_stack(message):
    global player_stack
    if "모두" in message.content:
        player_stack.append(PLAYER1)
        player_stack.append(PLAYER2)
        player_stack.append(PLAYER3)
        return

    if PLAYER1 not in message.content and PLAYER2 not in message.content and PLAYER3 not in message.content and PLAYER2_2 not in message.content and PLAYER3_2 not in message.content:
        player_stack.append(message.author.display_name)
        return

    if PLAYER1 in message.content:
        player_stack.append(PLAYER1)
    if (PLAYER2 in message.content) or (PLAYER2_2 in message.content):
        player_stack.append(PLAYER2)
    if (PLAYER3 in message.content) or (PLAYER3_2 in message.content):
        player_stack.append(PLAYER3)


def add_week_stack(message):
    global week_stack
    if ("월" not in message.content) & ("화" not in message.content) & ("수" not in message.content) & ("목" not in message.content) & ("금" not in message.content):
        tz = pytz.timezone("Asia/Seoul")
        day = datetime.now(tz).weekday()
        if("어제" in message.content):
            day -= 1
        if day < 5 :
            week_stack.append(day)
        return
    if ("월" in message.content) or ("월요일" in message.content):
        week_stack.append(0)
    if ("화" in message.content) or ("화요일" in message.content):
        week_stack.append(1)
    if ("수" in message.content) or ("수요일" in message.content):
        week_stack.append(2)
    if ("목" in message.content) or ("목요일" in message.content):
        week_stack.append(3)
    if ("금" in message.content) or ("금요일" in message.content):
        week_stack.append(4)


async def print_challenge_state(player):
    global current_challenge_state
    print_text = f"> ## {player}의 챌린지\n"

    for i in range(5) :
        print_text += f"> ### {weekName[i]} : " + current_challenge_state[player][i].value + "\n"

    await CHANNEL.send(print_text)

async def change_state(state):
    global current_challenge_state
    for p in player_stack:
        for w in week_stack:
            current_challenge_state[p][w] = state
            await CHANNEL.send(f"## {p} {weekName[w]}요일 {state.value}")
    save_csv()

async def reset_state():
    global current_challenge_state
    for i in range(5):
        current_challenge_state[PLAYER1][i] = State.NONE
        current_challenge_state[PLAYER2][i] = State.NONE
        current_challenge_state[PLAYER3][i] = State.NONE
    save_csv()
    await CHANNEL.send("이번주도 힘내요!")

async def check_yesterday(day):
    global current_challenge_state
    message = f"> ## {weekName[day-1]}요일 챌린지 실패!\n> ### "
    if current_challenge_state[PLAYER1][day-1] == State.NONE :
        current_challenge_state[PLAYER1][day - 1] = State.FAIL
        message += f"{PLAYER1} "
    if current_challenge_state[PLAYER2][day-1] == State.NONE :
        current_challenge_state[PLAYER2][day - 1] = State.FAIL
        message += f"{PLAYER2} "
    if current_challenge_state[PLAYER3][day-1] == State.NONE :
        current_challenge_state[PLAYER3][day - 1] = State.FAIL
        message += f"{PLAYER3} "
    save_csv()
    await CHANNEL.send(message)


async def check_week():
    await print_challenge_state(PLAYER1)
    await print_challenge_state(PLAYER2)
    await print_challenge_state(PLAYER3)

    message = "> ## 금주 챌린지 결과!\n"
    p1_money = 0
    p2_money = 0
    p3_money = 0
    for s in current_challenge_state[PLAYER1] :
        if s == State.FAIL :
            p1_money+=2000
    for s in current_challenge_state[PLAYER2] :
        if s == State.FAIL :
            p2_money+=2000
    for s in current_challenge_state[PLAYER3] :
        if s == State.FAIL :
            p3_money+=2000
    if p1_money == 0 :
        p1_money += 10000
    if p2_money == 0 :
        p1_money += 10000
    if p3_money == 0 :
        p1_money += 10000
    message += f"> ### {PLAYER1} : {p1_money}\n"
    message += f"> ### {PLAYER2} : {p2_money}\n"
    message += f"> ### {PLAYER3} : {p3_money}\n"

    await CHANNEL.send(message)


def open_csv():
    global current_challenge_state
    with open("state.csv", "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        for i in range(5) :
            match int(reader[0][i]) :
                case 0 :
                    current_challenge_state[PLAYER1][i] = State.FAIL
                case 1 :
                    current_challenge_state[PLAYER1][i] = State.SUCCESS
                case _ :
                    current_challenge_state[PLAYER1][i] = State.NONE
        print(f"{PLAYER1} 챌린지 데이터 로드 완료. {current_challenge_state[PLAYER1]}")
        for i in range(5) :
            match int(reader[1][i]) :
                case 0 :
                    current_challenge_state[PLAYER2][i] = State.FAIL
                case 1 :
                    current_challenge_state[PLAYER2][i] = State.SUCCESS
                case _ :
                    current_challenge_state[PLAYER2][i] = State.NONE
        print(f"{PLAYER2} 챌린지 데이터 로드 완료. {current_challenge_state[PLAYER2]}")
        for i in range(5) :
            match int(reader[2][i]) :
                case 0 :
                    current_challenge_state[PLAYER3][i] = State.FAIL
                case 1 :
                    current_challenge_state[PLAYER3][i] = State.SUCCESS
                case _ :
                    current_challenge_state[PLAYER3][i] = State.NONE
        print(f"{PLAYER3} 챌린지 데이터 로드 완료. {current_challenge_state[PLAYER3]}")

def save_csv():
    with open("state.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for player in [PLAYER1, PLAYER2, PLAYER3]:
            row = []
            for s in current_challenge_state[player]:
                match s:
                    case State.FAIL:
                        row.append(0)
                    case State.SUCCESS:
                        row.append(1)
                    case _:
                        row.append(2)
            writer.writerow(row)




##############################
##########run Bot#############
##############################
@tasks.loop(minutes=1)
async def daily_challenge_check():
    if CHANNEL == None:
        return

    tz = pytz.timezone("Asia/Seoul")
    now = datetime.now(tz)
    if now.hour == 13 and now.minute == 00:
        day = datetime.now(tz).weekday()
        if day == 0 :
            await reset_state()
        elif day > 0 & day < 6 :
            await check_yesterday(day)
        if day == 5 :
            await check_week()


async def process_message(message):
    global player_stack
    global week_stack

    ##### set player
    add_player_stack(message)
    ##### set day
    add_week_stack(message)

    # print(player_stack, " : ", len(player_stack))
    # print(week_stack, " : ", len(week_stack))

    if "상태" in message.content:
        for player in player_stack:
            await print_challenge_state(player)
    elif "성공" in message.content:
        await change_state(State.SUCCESS)
    elif "실패" in message.content:
        await change_state(State.FAIL)
    elif "초기화" in message.content:
        await reset_state()
    elif "체크" in message.content:
        tz = pytz.timezone("Asia/Seoul")
        now = datetime.now(tz)
        day = datetime.now(tz).weekday()
        if day > 0 & day < 6 :
            await check_yesterday(day)
        else :
            await CHANNEL.send("챌린지가 없어요!")
    elif "결과" in message.content:
        await check_week()

    ##### clear list
    player_stack.clear()
    week_stack.clear()