
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='a.')

saki_chans = []
channel_name='Kurusaki-Text-Channel'

async def get_world_channels():
    """
    Get all the channels that has the same names as the variable value `channel_name`
    """

    for i in bot.servers:
        for x in i.channels:
            if x.name == channel_name and x.id not in saki_chans:
                saki_chans.append(x.id)



@bot.event
async def on_ready():
    await get_world_channels()
    print(bot.user.name)

@bot.event
async def on_channel_create(channel):
    """
    This will add new world chat channels into the list allowing the bot to send the message to the other new channels that are added
    """
    if channel.name == channel_name and channel.id not in saki_chans:
        saki_chans.append(channel.id)


@bot.event
async def on_message(msg):
    if msg.author.bot == False and msg.channel.name == channel_name: #check to see if author is human and channel name is equal to the `channel_name`
        for i in saki_chans:
            if i != msg.channel.id: #prevent the channel from sending the message to the channel that started the message
                await bot.send_message(discord.Object(id=i),msg.content)

    await bot.process_commands(msg)


bot.run('TOKEN')
