##########import Section#############
import os #기본
from dotenv import load_dotenv, set_key #.env사용
import discord #Discord사용


##내 정의 모듈
import dailyLunch as DL
import dailyChallenge as DC
import dailyQR as DQ


# TOKEN
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BOT_TEST_ID = 0
BOT_TEST_CHANNEL = None


# intents, client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


# bot start
@client.event
async def on_ready():
    DC.CHANNEL_ID = int(os.getenv('CHALLENGE_CHANNEL'))
    DL.CHANNEL_ID = int(os.getenv('LUNCH_CHANNEL'))
    DQ.CHANNEL_ID = int(os.getenv('QR_CHANNEL'))
    DC.CHANNEL = client.get_channel(DC.CHANNEL_ID)
    DL.CHANNEL = client.get_channel(DL.CHANNEL_ID)
    DQ.CHANNEL = client.get_channel(DQ.CHANNEL_ID)

    global BOT_TEST_ID, BOT_TEST_CHANNEL
    BOT_TEST_ID = int(os.getenv('BOT_TEST_CHANNEL'))
    BOT_TEST_CHANNEL = client.get_channel(BOT_TEST_ID)
    # DC.CHANNEL_ID = BOT_TEST_ID
    # DC.CHANNEL = BOT_TEST_CHANNEL
    DL.CHANNEL_ID = BOT_TEST_ID
    DL.CHANNEL = BOT_TEST_CHANNEL
    # DQ.CHANNEL_ID = BOT_TEST_ID
    # DQ.CHANNEL = BOT_TEST_CHANNEL

    DC.open_csv()
    DL.open_csv()
    DC.daily_challenge_check.start()
    DL.daily_lunch_alert.start()
    DQ.daily_qr_alert.start()
    print(f'We have logged in as {client.user}')

# process message
@client.event
async def on_message(message):
    if message.author == client.user:  # 봇이 보낸 메세지면 무시
        return

    if message.content.startswith('/미아') or message.content.startswith('/mc'):
        print("message start : ", message.content)
        match  message.channel.id:
            case DC.CHANNEL_ID:
                await DC.process_message(message)
            case DL.CHANNEL_ID:
                await DL.process_message(message)
            case DQ.CHANNEL_ID:
                await DQ.process_message(message)








# run
client.run(TOKEN)
