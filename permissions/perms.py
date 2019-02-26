import discord
import asyncio
from discord.ext import commands

b0t = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
  print(bot.user.name)
  
  

@commands.has_permissions(manage_roles=True)
@bot.command(pass_context=True)
async def createRole(con,*,Name):
  await bot.create_role(name=Name)
  
  
  
@commands.has_permissions(manage_messages=True,read_message_history=True)
@bot.command(pass_context=True)
async def clear(con,amt=50):
  await bot.purge_from(channel=con.message.channel,limit=amt)

bot.run('bot_token')
