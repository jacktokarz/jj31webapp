import discord
import os
from discord.ext import ipcx
import serializer
import socket


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

TEST_CHANNEL = 1372019348364853308
GENERAL_CHANNEL = 1368396579576352843
NOISY_ANNOUNCEMENTS = 1368433478772981800
# HOST = socket.gethostbyname('ipc_server_dns_name')
HOST = "bot"
# HOST = "localhost"
class DiscordBot(discord.Client):

    def __init__(self, *, intents, **options):
        super().__init__(intents=intents, **options)
        self.ipc = ipcx.Server(self, host=HOST, port=4243, secret_key="meow")

    async def setup_hook(self):
         await self.ipc.start()

    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        self.jj = self.get_user(112950701281337344)
        # await self.get_channel(GENERAL_CHANNEL).send("Keep Ian away from me JJ D:")
        print("On Ready complete")

bot = DiscordBot(intents=intents)    



@bot.ipc.route()
async def post_question(data):
        asked_question = serializer.QuestionSerializer(data=data.asked_question)
        team = serializer.TeamSerializer(data=data.team)
        channel = bot.get_channel(team.initial_data['discord_id'])
        await channel.send(f"Hi {bot.jj.mention}! The team has a question for you: **{asked_question.initial_data['title']}**")
        print("Finished posting the question")
        print(asked_question.initial_data)
        if asked_question.initial_data['additional_info'] == 'True':
            print("There is additional info!")
            print(data)
            await channel.send(f"With additional info: {data.addl_info}")

@bot.ipc.route()
async def post_leaderboard(data):
     print("Got the leaderboard!")
     channel = bot.get_channel(TEST_CHANNEL)
     print("Got the Channel!")
     await channel.send(data.output)

with open(os.path.dirname(os.path.realpath(__file__)) + "/etc/discord_token.txt") as f:
    discord_token = f.read().strip()

bot.run(discord_token)
