import discord
from discord.ext import commands
import asyncio


bot=commands.Bot(command_prefix='a.)


saki_chans=[]
async def get_saki_chans():
	"""
	This gets the ids of channels that are called kurusaki_text_channel and it can be named anything else you'd like just make sure to change it in other areas of your code as well if it requires it
	The ids are stored in the variable `saki_chans`
	"""
    for i in bot.servers:
        for x in i.channels:
            if x.type == discord.ChannelType.text and x.name == 'kurusaki_text_channel' and x.id not in saki_chans:
                saki_chans.append(x.id)
    print(saki_chans)



@bot.event
async def on_channel_create(chan):
	"""
	This event function will add the new channels that are created to the channel if they are named kurusaki_text_channel and their ids aren't in the list
	"""
    if chan.id not in saki_chans:
        saki_chans.append(chan.id)
                 

                 
@bot.event
async def on_ready():
    bot.loop.create_task(get_saki_chans())
    """WHEN BOT IS READY, PRINT MESSAGE IN TERMINAL"""
    print("I am running on " + bot.user.name)


  
  
@bot.event
async def on_message(msg):
    if msg.server and msg.channel.name == 'kurusaki_text_channel' and msg.author.id != bot.user.id:
        for i in saki_chans:
            if i == msg.channel.id:
                pass
            else:
                if msg.attachments != []:  # message has files
                    emb = discord.Embed()
                    emb.set_image(url=msg.attachments[0]['url'])
                    emb.set_footer(text="Image sent by: {}".format(msg.author.name))
                    emb.set_thumbnail(url=msg.author.avatar_url)

                    await bot.send_message(discord.Object(id=i), embed=emb)

                if msg.embeds != []:
                    emb = discord.Embed()
                    emb.set_footer(text="Sent by: {}".format(msg.author.name))
                    try:
                        emb.set_image(url=msg.embeds[0]['image']['url'])
                        emb.set_thumbnail(url=msg.author.avatar_url)
                        await bot.send_message(discord.Object(id=i), embed=emb)
                    except:
                        pass

                if msg.attachments == [] and msg.embeds == []:  # message has no files
                    emb=discord.Embed(title=msg.author.name,description=msg.content)
                    emb.set_thumbnail(url=msg.author.avatar_url)
                    emb.set_footer(text="From {}".format(msg.server.name))
                    await bot.send_message(discord.Object(id=i),embed=emb)

	await bot.process_commands(msg)
  
bot.run('TOKEN')
