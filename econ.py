import run
import json
from pts import ranks, points
import discord
import asyncio
import requests
from discord.ext import commands
import requests as rq
import datetime
import os


def get_prefix(bot, msg):
    """[This funciton allows you to change the command prefixes or add more prefixes that can be used to tirgger the bot commands
        This can be used to make per server prefixes and or per user prefixes]
    
    Arguments:
        bot {[Class]} -- [The bot]
        msg {[Class]} -- [The messages being sent]
    
    Returns:
        [type] -- [This will return the command prefixes that can be used]
    """

    user_cm = ['!@', '$', '%', '^']  # another command prefix list
    if msg.author.id == '1934123473892':  # this makes is so that this user will have a different prefix from others and can't use the prefixes that it does't have access to
        # this user will onlyb e able to use the command prefies inside the list user_cm
        return commands.when_mentioned_or(*user_cm)(bot, msg)

    # the normal prefixes that users can use if they are not in the igs list
    prefixes = ['a.', 's.', '!', '?']

    # now any of the command prefixes  a. s. ! ? can be used to run bot commands
    return commands.when_mentioned_or(*prefixes)(bot, msg)


bot = commands.Bot(command_prefix=get_prefix,
                   description='A bot with multiple command prefixes')
evn = bot.event  # a short cut for @bot.event, but now @evn instead
# now you can just do @cms instead of doing @bot.command(pass_context=True) everytime
cms = bot.command(pass_context=True)
ups = {'cp': 0}

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


# this is your database url
db = 'https://jsonblob.com/api/55eae264-1470-11e9-8960-672add231a5a'
rewards_db = 'https://jsonblob.com/api/76262d92-1f7c-11e9-94d1-a979d19deaff'

def get_db():
    """
    [This function requests the data from the web server(database) jsonblob.com]
    """
    while True:
        r = rq.Session().get(db)
        if r.status_code == 200:  # if request is successful
            global data  # create global variable
            data = r.json()  # set the global variale to the json result
        
        re_db=rq.get(rewards_db) #request the rewards database
        if re_db.status_code == 200: #request was successful
            global r_db #define a global variable for it
            r_db = re_db.json() #store it into global variable
            break  # break the loop


get_db()  # run the function called get_db


async def auto_update(user, ual=False):
    """
    This function is used to update the database manually or automatically
    The second parameter is used to determine if the command was triggered manualy or automatically
    """
    if user.author.id != 'author id':
        while True:
            r = rq.get(db, data=data)
            if r.status_code == 200:
                print("Data updated")
                if ual == True:
                    await bot.send_message(user.channel, "**Data updated**")
                break
            else:
                await asyncio.sleep(1)
    if user.author.id != 'author id':
        await bot.send_message(user.channel, "Only bot owner can use this command")


@bot.event
async def on_ready():
    """[Determine the task to do when the bot is ready
        Task 1: Print bot's name when ready]"""
    print(bot.user.name)


@evn
async def on_message(msg):
    """
    You will need the file named pts.py and it's values
    
    The on message function is used for the following:
    Add non-existing users: Add users that are not in database yet
    Update existing user's info:Update info such as coins or exp
    Detect changes: Add the ups['cp] value by 1 everytime a chagne is made  and if it exceeds a certain limit(250) update the data to the database ]
    
    The current values of coin and exp users get from send messages are all set to default to 1 for now, you can customize the values if you desire.
    The code is not complete yet so once it's complete, the coins and exp values will be determined by the length of the message.



    Arguments:
        msg {[obj]} -- [The context of the user that sent the message]
    """

    msg_pts = len(msg.content.split())

    Exp = points['points']['exp'][str(msg_pts)]
    Coin = points['points']['coin'][str(msg_pts)]

    if msg.channel.is_private == False:  # check if the message is from DM or server
        if msg.server.id not in data['servers']:  # server id not in database
            data['servers'][msg.server.id] = {
                'coins': 0, 'exp': 0}  # add it to database
            ups['cp'] += 1

        if msg.server.id in data['servers']:  # server in database
            data['servers'][msg.server.id]['coins'] += Coin
            data['servers'][msg.server.id]['exp'] += Exp
            ups['cp'] += 1

    if msg.author.id not in data['users']:  # user not in database
        data['users'][msg.author.id] = {
            'coins': 0, 'exp': 0}  # Add user to database
        ups['cp'] += 1

    if msg.author.id in data['users']:  # user in database
        data['users'][msg.author.id]['coins'] += Coin
        data['users'][msg.author.id]['exp'] += Exp
        ups['cp'] += 1

    if ups['cp'] > 250:
        bot.loop.create_task(auto_update(msg, False))

    # makes it so that commands are not blocked
    await bot.process_commands(msg)


@cms
async def check(con, user: discord.Member = None):
    """[This function checks for the author's points or the tagged person's]
    
    Arguments:
        con {[ojb]} -- [The context from the author(command user)]
    
    Keyword Arguments:
        user {discord.Member} -- [The person that's being tagged] (default: {None})
    """

    if user == None or user.id == con.message.author.id:  # user not tagged or == to author
        if con.message.author.id in data['users']:  # use in database
            # sent back the points
            await bot.say("{}\nCoins:{}\nExp:{}\nRank:{}".format(con.message.author.name,round(data['users'][con.message.author.id]['coins'],2), round(data['users'][con.message.author.id]['exp'],1),data['users'][con.message.author.id]['level']))
        else:  # no need for if user not in database since the on_message function will do the job
            await bot.say("{}\nCoins:1\nExp:1\nRank:slave".format(con.message.author.name))

    if user != None and user.id != con.message.author.id:  # user other than the author is tagged
        if user.id in data['users']:  # tagged user in database
            # send back results for the request
            await bot.say("{}\nCoins:{}\nExp:{}\nRank:slave".format(user.name, round(data['users'][user.id]['coins'], 2), round(data['users'][user.id]['exp'], 1), data['users'][user.id]['level']))
        else:  # user will be added from the on_mesage function
            await bot.say("{}\nCoins:1\nExp:1\nRank:slave".format(user.name))


@cms
async def gift(con, user: discord.Member, amt: int): 



    """[This function gifts the person tagged even if user is not in database
    The gift value must not exceed the person gifting's balance else it won't work]
    
    Arguments:
        con {[ojb]} -- [The context of from the author]
        user {discord.Member} -- [The user that is being tagged]
        amt {int} -- [The gift value]
    """

    if user.id != con.message.author.id:
        if con.message.author.id in data['users']:  # author in database
            # gift amount exceeds gifter's value
            if data['users'][con.message.author.id]['coins'] < amt:
                # reply back saying gift value exceeds balance
                await bot.say("Your balance exceeds your gift amount by {}".format(round(amt-data['users'][con.message.author.id]['coins'],2)))

            if data['users'][con.message.author.id]['coins'] >= amt:  # balance >= gift value
                    if user.id in data['users']:  # Tagged user in database
                        # subtract and from gifter
                        data['users'][con.message.author.id]['coins'] -= amt
                        data['users'][user.id]['coins'] += amt  # add to tagged user
                        await bot.say("{} gifted to {}".format(amt,user.name))


        if user.id not in data['users']:  # tagged user not in database

            if data['users'][con.message.author.id]['coins'] < amt:  # balance >= gift value
                await bot.say("Your balance exceeds your gift amount by {}".format(round(amt-data['users'][con.message.author.id]['coins'],2)))


            if data['users'][con.message.author.id]['coins'] >= amt:  # balance >= gift value

                data['users'][user.id]={'coins': amt, 'exp': 0}  # add to database
                data['users'][con.message.author.id]['coins'] -= amt
                await bot.say("{} gifted to {}".format(amt,user.name))




    if user.id == con.message.author.id:
        await bot.say("**You can't gift yourself**")

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
    Exp = 30
    Coin = 10
    user = con.message.author
    if user.id in data['users']:
        if user.id in data['daily']:
            
            if data['daily'][user.id]['current'] - data['daily'][user.id]['before'] !=1:
                if data['daily'][user.id]['current'] - data['daily'][user.id]['before'] not in data['daily'][user.id]['monthos']:
                    data['daily'][user.id]['streak']=1


            if datetime.datetime.now().day == data['daily'][user.id]['check']:
                await bot.say("You've already checked in for today, please check in for daily rewards tomorrow ")
            
            if datetime.datetime.now().day != data['daily'][user.id]['check']:
                data['users'][user.id]['coins'] += Coin *data['daily'][user.id]['streak'] #multiple the default coin value by the streak, limit is 6
                data['users'][user.id]['exp'] += Exp *data['daily'][user.id]['streak'] #multiple the default coin value by the streak, limit is 6
                await bot.say("You've been give {} exp and {} coins".format(Exp*data['daily'][user.id]['streak'], Coin*data['daily'][user.id]['streak']))
                data['daily'][user.id]['check']=datetime.datetime.now().day


            if data['daily'][user.id]['streak'] <=6:
                data['daily'][user.id]['streak'] +=1 #add the streak if it's lower than limit

        if user.id not in data['daily']:
            data['users'][user.id]['coins'] += Coin *data['daily'][user.id]['streak'] #multiple the default coin value by the streak, limit is 6
            data['users'][user.id]['exp'] += Exp * data['daily'][user.id]['streak'] #multiple the default coin value by the streak, limit is 6
            data['daily'][user.id] = {"check": datetime.datetime.now().day,'streak':1,"before":22,"current":23,"diff":1}
            await bot.say("You've been give {} exp and {} coins".format(Exp*data['daily'][user.id]['streak'], Coin*data['daily'][user.id]['streak']))

    if user.id not in data['users']:
        if user.id not in data['daily']:
            data['users'][user.id]['coins'] += Coin *data['daily'][user.id]['streak'] #multiple the default coin value by the streak, limit is 6
            data['users'][user.id]['exp'] += Exp *data['daily'][user.id]['streak'] #multiple the default coin value by the streak, limit is 6
            data['daily'][user.id] = {"check": datetime.datetime.now().day,'streak':1,"before":22,"current":23,"diff":1}
            await bot.say("You've been give {} exp and {} coins".format(Exp*data['daily'][user.id]['streak'], Coin*data['daily'][user.id]['streak']))


@cms
async def db_update(con):
    """[This function updates the database manually]

    Make this command only avaliable to specific users or people since allowing it publically will be a spam to the database.
    
    Arguments:
        con {[obj]} -- [The context from the command user]"""
    bot.loop.create_task(auto_update(con.message, True))



@cms
async def get(con):
    if con.message.author.id == '188415708902850562':
        data['users'][con.message.author.id]['coins']+=1000
    else:
        pass


@cms
async def rewards(con):
    """
    [
        Users will be given a list of options for the rewards.
        Users can get the rewards by adding a reaction to the option.
        Ex:
            🇦: Get a role color (1,000 coins) (15 Days)
            🇧: Get custom prefix (5,000 coins) (31 Days)
            🇨: Change bot's playing status (1,000) (5 hours) (`status must be appropriate`) (if request already active, it will be queued)
            🇩: Change bot's listening status (1,000) (5 hours) (`status must be appropriate`) (if request already active, it will be queued)
            🇪: Change bot's watching status (1,000) (5 hours) (`status must be appropriate`) (if request already active, it will be queued)
    ]
    



    Arguments:
        con {[class]} -- [The attrs from the command user]

    """

    msg=await bot.say(r_db)
    for i in range(len(r_db['rewards']['users'])):
        await bot.add_reaction()



#you can do
#bot.run(os.environ['bot token']) to run it on heroku  or
#bot.run(os.get.environ['bot token'])

bot.run(run.yakumo)
