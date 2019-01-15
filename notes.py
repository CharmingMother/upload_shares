import discord
import asyncio
import requests as rq
from discord.ext import commands 
import os



bot=commands.Bot(command_prefix='a.')
evn=bot.event
cms=bot.command(pass_context=True)

 

async def update_notes(say,con):
    while True:
        r=rq.Session().get('https://jsonblob.com/api/581e52a7-1506-11e9-8960-4916de474b22',data=data)#you can use your own url by creating your own database from jsonblob or other sources
        if r.status_code == 200:
            if say == True:
                await bot.send_message(con.message.channel,"**Notes updated!**")
            print("Notes Data updated")
            break


async def notes_db():
    while True:
        r=rq.Session().get('https://jsonblob.com/api/581e52a7-1506-11e9-8960-4916de474b22') #you can use your own url by creating your own database from jsonblob or other sources
        if r.status_code == 200:
            global data
            data=r.json()
            break


@bot.event
async def on_ready():
    svs=0
    bot.loop.create_task(notes_db())
    for i in bot.servers:
        svs+=1

    print(svs)
    print(bot.user.name)


@cms
async def node(con,*,note):
    if con.message.author.id in data['notes']:
        data['notes'][con.message.author.id].append(note)

    if con.message.author.id not in data['notes']:
        data['notes'][con.message.author.id]=[]
        data['notes'][con.message.author.id].append(note)

@cms
async def notes(con):
    result=''
    if con.message.author.id in data['notes']:
        for i in data['notes'][con.message.author.id]:
            result+=i+'\n'
        data['changes']+=1
        if data['changes'] >= 250:
            data['changes']=0
            bot.loop.create_task(update_notes(False,False))
        await bot.say(result+"**Your notes will always appear at the place you requested at**")
    else:
        await bot.say("You do not have any notes")

@cms
async def notes_update(con):
    bot.loop.create_task(update_notes(True,con))


bot.run(os.environ['bot_token'])
