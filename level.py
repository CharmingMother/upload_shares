import json
import discord
import asyncio
import requests
from discord.ext import commands
import requests as rq
import datetime
import os



bot=commands.Bot(command_prefix='a.') #the command prefix for the bot
evn=bot.event# a short cut for @bot.event, but now @evn instead
cms=bot.command(pass_context=True) #now you can just do @cms instead of doing @bot.command(pass_context=True) everytime
ups={'cp':0}

"""
Go to jsonblob.com and create a JSON in this format

{
  "servers": {},
  "users": {},
  "daily": {}
}

then click save and put api in the position after .com/  https://jsonblob.com/Put the word api here/55eae264-1470-11e9-8960-672add231a5a
example: 
Before: "https://jsonblob.com/55eae264-1470-11e9-8960-672add231a5a"
After: "https://jsonblob.com/api/55eae264-1470-11e9-8960-672add231a5a"



Once you've done all that replace the urls I that I have in the code with your own url that you made from jsonblob
"""


db = 'https://jsonblob.com/api/55eae264-1470-11e9-8960-672add231a5a' #this is your database url


def get_db():
    """
    [This function requests the data from the web server(database) jsonblob.com]
    """
    while True:
        r=rq.Session().get(db)
        if r.status_code == 200: #if request is successful
            global data #create global variable
            data=r.json() #set the global variale to the json result
            break #break the loop


get_db()# run the function called get_db




async def auto_update(user,ual=False):
    """
    This function is used to update the database manually or automatically
    The second parameter is used to determine if the command was triggered manualy or automatically
    """
    if user.author.id != 'author id':
        while True:
            r=rq.get('da',data=data)
            if r.status_code == 200:
                print("Data updated")
                if ual==True:
                    await bot.send_message(user.channel,"**Data updated**")
                break
            else:
                await asyncio.sleep(1)
    if user.author.id != 'author id':
        await bot.send_message(user.channel,"Only bot owner can use this command")




@bot.event
async def on_ready():
    """[Determine the task to do when the bot is ready
        Task 1: Print bot's name when ready]"""
    print(bot.user.name)


@evn
async def on_message(msg):
    """[The on message function is used for the following:
    Add non-existing users: Add users that are not in database yet
    Update existing user's info:Update info such as coins or exp
    Detect changes: Add the ups['cp] value by 1 everytime a chagne is made  and if it exceeds a certain limit(250) update the data to the database ]
    
    The current values of coin and exp users get from send messages are all set to default to 1 for now, you can customize the values if you desire.
    The code is not complete yet so once it's complete, the coins and exp values will be determined by the length of the message.



    Arguments:
        msg {[obj]} -- [The context of the user that sent the message]
    """

    if msg.channel.is_private == False: #check if the message is from DM or server
        if msg.server.id not in data['servers']: #server id not in database
            data['servers'][msg.server.id]={'coins':0,'exp':0} #add it to database
            ups['cp']+=1

        if msg.server.id in data['servers']: #server in database
            data['servers'][msg.server.id]['coins']+=1
            data['servers'][msg.server.id]['exp'] += 1 
            ups['cp']+=1

    if msg.author.id not in data['users']:# user not in database
        data['users'][msg.author.id]={'coins':0,'exp':0} #Add user to database
        ups['cp']+=1


    if msg.author.id in data['users']:#user in database
        data['users'][msg.author.id]['coins']+=1 
        data['users'][msg.author.id]['exp']+=1
        ups['cp']+=1

    if ups['cp'] > 250:
        bot.loop.create_task(auto_update(msg,False))


    await bot.process_commands(msg) #makes it so that commands are not blocked

@cms
async def check(con,user:discord.Member=None):
    """[This function checks for the author's points or the tagged person's]
    
    Arguments:
        con {[ojb]} -- [The context from the author(command user)]
    
    Keyword Arguments:
        user {discord.Member} -- [The person that's being tagged] (default: {None})
    """

    if user == None or user.id == con.message.author.id: #user not tagged or == to author
        if con.message.author.id in data['users']: #use in database
            await bot.say("Coins:{}\nExp:{}".format(data['users'][con.message.author.id]['coins'],data['users'][con.message.author.id]['exp'])) #sent back the points
        else: #no need for if user not in database since the on_message function will do the job
            await bot.say("Coins:1\nExp:1")

    if user !=None and user.id != con.message.author.id: #user other than the author is tagged
        if user.id in data['users']: #tagged user in database
            await bot.say("{}\nCoins:{}\nExp:{}".format(user.name, data['users'][user.id]['coins'], data['users'][user.id]['exp'])) #send back results for the request
        else: #user will be added from the on_mesage function
            await bot.say("{}\nCoins:1\nExp:1".format(user.name))


@cms
async def gift(con,user:discord.Member,amt:int):
    """[This function gifts the person tagged even if user is not in database
    The gift value must not exceed the person gifting's balance else it won't work]
    
    Arguments:
        con {[ojb]} -- [The context of from the author]
        user {discord.Member} -- [The user that is being tagged]
        amt {int} -- [The gift value]
    """

    if con.message.author.id in data['users']: #author in database
        if data['users'][con.message.author.id]['coins'] < amt: #gift amount exceeds gifter's value
            await bot.say("Your balance exceeds your gift amount by {}".format(amt-data['users'][con.message.author.id]['coins'])) #reply back saying gift value exceeds balance
        
        if data['users'][con.message.author.id]['coins'] >= amt:# balance >= gift value
            if user.id in data['users']: #Tagged user in database
                data['users'][con.message.author.id]['coins']-=amt #subtract and from gifter
                data['users'][user.id]['coins'] += amt ## add to tagged user

            if user.id not in data['users']: #tagged user not in database
                data['users'][con.message.author.id]['coins']-=amt
                data['users'][user.id]+{'coins':amt,'exp':0}# add to database



@cms
async def daily(con):
    """
    [The daily command gives users that use it 30 exp and 10 coin. 
    This command uses the datetime library and the day value to determine if use has already checked in or not

    `datetime.datetime.now().day 

    To customize the values of the amounts given change the following variables
    
    Exp: The amount of exp to give by default when using the daily command
    Coin: The amount of coin to give by default when this command is used
    
    Exp = 30 Default Value
    Coin = 10 Default Value
    ]
    """
    Exp= 30
    Coin = 10
    user=con.message.author
    if user.id in data['users']:
        if user.id in data['daily']:
            if datetime.datetime.now().day != data['daily'][user.id]['check']:
                data['users'][user.id]['coins']+=Coin
                data['users'][user.id]['exp']+=Exp
                await bot.say("You've been give {} exp and {} coins".format(Exp,Coin))
            if datetime.datetime.now().day == data['daily'][user.id]['check']:
                await bot.say("You've already checked in for today, please check in for daily rewards tomorrow ")

        if user.id not in data['daily']:
            data['users'][user.id]['coins']+=Coin
            data['users'][user.id]['exp'] += Exp
            data['daily'][user.id]={"check":datetime.datetime.now().day}
            await bot.say("You've been give {} exp and {} coins".format(Exp,Coin))


    if user.id not in data['users']:
        if user.id not in data['daily']:
            data['users'][user.id]['coins'] += Coin
            data['users'][user.id]['exp'] += Exp
            data['daily'][user.id] = {"check": datetime.datetime.now().day}
            await bot.say("You've been give {} exp and {} coins".format(Exp,Coin))




@cms
async def db_update(con):
    """[This function updates the database manually]
    
    Arguments:
        con {[obj]} -- [The context from the command user]"""
    bot.loop.create_task(auto_update(con.message,True))



#you can do 
#bot.run(os.environ['bot token']) to run it on heroku  or
#bot.run(os.get.environ['bot token'])

bot.run('BOT TOKEN HERE')
