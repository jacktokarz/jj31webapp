from discord.ext import ipcx
import scavhunt.serializer as serializer
import asyncio


KETY = "meow"
class DiscordSender():
    def post_question(self, asked_question, team, addl_info):
        print("Hello world!")
        print(asked_question)
        asyncio.run(self.async_post_question(asked_question, team, addl_info))
        
    
    async def async_post_question(self, asked_question, team, addl_info):
        ipc_client = ipcx.Client(secret_key=KETY)
        await ipc_client.request("post_question", asked_question=serializer.QuestionSerializer(asked_question).data, addl_info=addl_info)
        await ipc_client.close()

    def update_leaderboard(self, output):
        asyncio.run(self.async_update_leaderboard(output))
        

    async def async_update_leaderboard(self, output):
        ipc_client = ipcx.Client(secret_key=KETY)
        await ipc_client.request("post_leaderboard", output=output)
        await ipc_client.close()