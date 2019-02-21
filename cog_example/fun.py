import discord
import asyncio
from discord.ext import commands



class Fun:
  def __init__(self,bot):
    self.bot= bot


    
  @commands.command(pass_context=True)
  async def fun(con):
    await self.bot.say("This is fun!")


def setup(bot):
    bot.add_cog(Fun(bot))
