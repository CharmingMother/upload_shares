import discord
import asyncio
import requests as rq
from discord.ext import commands 
import os
import random
import time


bot=commands.Bot(command_prefix='a.')
evn=bot.event
cms=bot.command(pass_context=True)



async def this_is_a_background_task():
    for i in range(11):
        print(i)
        await asyncio.sleep(1)






@evn
async def on_ready():
    bot.loop.create_task(this_is_a_background_task())
    # asyncio.get_event_loop().create_task(this_is_a_background_task())
    
    print(bot.user.name)



@cms
async def run_bg(con):
    bot.loop.create_task(this_is_a_background_task())
    # asyncio.get_event_loop().create_task(this_is_a_background_task())
