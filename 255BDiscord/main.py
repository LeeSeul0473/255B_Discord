##########import Section#############
import os #기본
from dotenv import load_dotenv, set_key #.env사용
import discord #Discord사용


##내 정의 모듈
import dailyLunch as DL
import dailyChallenge as DC


# TOKEN
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# intents, client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


# bot start
@client.event
async def on_ready():
    DC.CHANNEL = client.get_channel(int(os.getenv('CHALLENGE_CHANNEL')))
    DL.CHANNEL = client.get_channel(int(os.getenv('LUNCH_CHANNEL')))
    DC.open_csv()
    DL.open_csv()
    print(f'We have logged in as {client.user}')

# process message
@client.event
async def on_message(message):
    if message.author == client.user:  # 봇이 보낸 메세지면 무시
        return

    if message.content.startswith('/미아') or message.content.startswith('/mc'):

        match  message.channel.id:
            case DC.CHANNEL_ID:
                await DC.process_message(message)
            case DL.CHANNEL_ID:
                await DL.process_message(message)








# run
client.run(TOKEN)
