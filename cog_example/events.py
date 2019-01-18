import discord
import asyncio
from discord.ext import commands


class Events:
    def __init__(self, bot):
        self.bot = bot




    async def on_ready(self):
        print(self.bot.user.name)


    async def on_message(self,msg):
        print(msg.content)


def setup(bot):
    bot.add_cog(Events(bot))
