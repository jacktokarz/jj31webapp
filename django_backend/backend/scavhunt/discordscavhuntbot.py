import discord
import os
from discord.ext import tasks, commands, ipcx
import serializer


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class DiscordBot(discord.Client):

    def __init__(self, *, intents, **options):
        super().__init__(intents=intents, **options)
        self.ipc = ipcx.Server(self, secret_key="meow")

    async def setup_hook(self):
         await self.ipc.start()

    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        self.jj = self.get_user(112950701281337344)
        print("On Ready complete")

bot = DiscordBot(intents=intents)    

TEST_CHANNEL = 1372019348364853308
GENERAL_CHANNEL = 1368396579576352843

@bot.ipc.route()
async def post_question(data):
        asked_question = serializer.QuestionSerializer(data=data.asked_question)
        channel = bot.get_channel(TEST_CHANNEL)
        channel = bot.get_channel(data.team.discord_id)
        await channel.send(f"Hi {bot.jj.mention}! The team has a question for you: **{asked_question.initial_data['title']}**")
        if asked_question.additional_info:
            await channel.send(f"With additional info: {asked_question.addl_info}")

@bot.ipc.route()
async def post_leaderboard(data):
     print("Got the leaderboard!")
     channel = bot.get_channel(TEST_CHANNEL)
     print("Got the Channel!")
     await channel.send(data.output)

with open(os.path.dirname(os.path.realpath(__file__)) + "/etc/discord_token.txt") as f:
    discord_token = f.read().strip()

bot.run(discord_token)
