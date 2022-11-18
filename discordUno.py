import datetime
import os
import json
import accounts_omac
import random
from tkinter.messagebox import showerror, showinfo, showwarning
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View

# logging types:
# deleteAfter
#
# none
# all
#
# error
# modify
# warning
# debug
# info
# needed
# stalk

# generated variables:
lastTimeRead = datetime.datetime.now()

logInTerminal = True
logType = ["all"]
logFile = 'logFiles/'
if not os.path.isdir(logFile):
    os.mkdir(logFile)
logFile = f"{logFile}/log{datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
logF = open(logFile, "w")
logF.close()

def logging(itemToLog: str = '', type = '', special = ''):
    global accountData
    if logFile != '':
        time = datetime.datetime.now().strftime(('%d/%m/%Y-%H:%M:%S'))
        message = f"[{time}] [{type.upper()}] {itemToLog}"
        logF = open(f'{logFile}', "a+")
        logF.write(f'{special}{message}\n')
        logF.close() 
        if logInTerminal:
            print(f'{message}')

def log(logMessage: str = '', typeOfLog: str = 'info'):
    if logMessage != '' and "none" not in logType:
        if typeOfLog == 'info' and 'all' in logType:
            logging(logMessage, typeOfLog)
        elif typeOfLog == 'warning' and ('all' in logType or 'warning' in logType):
            logging(logMessage, typeOfLog, '>')
        elif typeOfLog == 'error' and ('all' in logType or 'error' in logType):
            logging(logMessage, typeOfLog, '>')
        elif typeOfLog == 'modify' and ('all' in logType or 'modify' in logType):
            logging(logMessage, typeOfLog)
        elif typeOfLog in logType or 'all' in logType:
            logging(logMessage, typeOfLog)
        elif typeOfLog == 'needed':
            logging(logMessage, typeOfLog)

timeDelayToRecheck = 90
userDict = {}
gamesDict = {}
serverIdNumber = 1111111

secretsDict = {}

def checkTime():
    global lastTimeRead
    timesince = datetime.datetime.now() - lastTimeRead
    if timesince.total_seconds() > timeDelayToRecheck:
        log(f"checked time to see if {timesince.total_seconds()}s is more than {timeDelayToRecheck}s (it is)")
        lastTimeRead = datetime.datetime.now()
        return True
    else:
        log(f"checked time to see if {timesince.total_seconds()}s is more than {timeDelayToRecheck}s (it is not)")
        return False

def loadSecrets():
    try:
        if os.path.exists(f'secrets.json'):
            with open(f'secrets.json') as level_json_file:
                botKey = json.load(level_json_file)
                if type(botKey) != dict and type(botKey) != list:
                    botKey = json.loads(botKey)
                secretsDict = botKey
                log("secrets have been loaded")
                if secretsDict["BotToken"] == "":
                    raise ImportError("No \"Bot Token\" provided! Add your \"Bot Token\" to the \"secrets.json\"")
        else:
            with open(f'secrets.json', 'w') as outfile:
                json.dump({"BotToken": "", "authorizedUsers": []}, outfile, indent=4)
            raise ImportError("No \"Bot Token\" provided! Add your \"Bot Token\" to the \"secrets.json\"")
    except Exception as e:
        log(e, "error")
        exit()
    return secretsDict

secretsDict = loadSecrets()

bot = commands.Bot(command_prefix="uno!", intents = discord.Intents.all())

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        log(f"Synched {len(synced)} command(s)")
    except Exception as e:
        log(e, 'error')
    getBotStats(bot)

@bot.tree.command(name="make_server")
async def make_server(interaction: discord.Interaction, pincode: int = 0):
    log(f"{interaction.user.mention} tries to make a server with pincode: {pincode}", "stalk")
    if createServer(interaction, pincode):
        if pincode == 0:
            await interaction.response.send_message(f"Server created!\nServer ID: {userDict[interaction.user.mention]['server']}\nNo Pincode", ephemeral=False)
        else:
            await interaction.response.send_message(f"Server created!\nServer ID: {userDict[interaction.user.mention]['server']}\nPincode: {gamesDict[userDict[interaction.user.mention]['server']]['passcode']}", ephemeral=False)
    else:
        await interaction.response.send_message(f"An error accured, please try again.", ephemeral=False)

@bot.tree.command(name="achievement")
@app_commands.describe(title = "title?")
@app_commands.describe(description = "description?")
@app_commands.describe(message = "message?")
async def achievement(interaction: discord.Interaction, title: str = '', description: str = '', message : str = ''):
    if title != '' and description != '':
        if (message == '' and len(title) + (len(title)*2) > 50) or len(title) + len(title) + len(message) > 50:
            await interaction.response.send_message(f"Too many characters", ephemeral=False)
        else:
            if message == '':
                message = description
            gotAchievement(title, description, f"{message}, (made by <{interaction.user.mention.split('@')[1]}")
            log(f"{interaction.user.mention} made an achievement: '{title}', '{description}', '{message}'", "stalk")
            embed=discord.Embed(title=title, description=description, color=0x15bcf4)
            embed.add_field(name="Message:", value=message, inline=True)
            await interaction.response.send_message(f"YEET",embed=embed, ephemeral=False)
            global accountData
            accountData = accounts_omac.saveAccount(accountData, configSettings)
    else:
        await interaction.response.send_message(f"Not enough data given", ephemeral=False)


@bot.tree.command(name="list_servers")
async def list_Servers(interaction: discord.Interaction):
    if checkTime():
        secretsDict = loadSecrets()
    if interaction.user.mention in secretsDict["authorizedUsers"]:
        log(f"{interaction.user.mention} was allowed to list all the servers")
        message = '=====Listed Servers=====\n'
        for server in list(gamesDict.keys()):
            if gamesDict[server]['passcode'] == 0:
                message = f"{message}Server ID: {server}\nHost: {gamesDict[server]['host']}\n=====YEET=====\n"
            else:
                message = f"{message}Server ID: {server}\nPicode: {gamesDict[server]['passcode']}\nHost: {gamesDict[server]['host']}\n=====YEET=====\n"
        message = f"{message}"
        await interaction.response.send_message(f"{message}", ephemeral=False)
    else:
        log(f"{interaction.user.mention} is not allowed to list all the servers, tried it from {interaction.guild_id}")
        await interaction.response.send_message(f"You are not an authorized user!", ephemeral=False)

@bot.tree.command(name="stop")
async def stop(interaction: discord.Interaction):
    global secretsDict
    if checkTime():
        secretsDict = loadSecrets()
    if interaction.user.mention in secretsDict["authorizedUsers"]:
        global accountData
        accountData = accounts_omac.saveAccount(accountData, configSettings)
        log(f"{interaction.user.mention} was allowed to stop the bot")
        if saveFile("botData", {"gamesDict": gamesDict, "userDict": userDict, "serverIdNumber": serverIdNumber}):
            await interaction.response.send_message(f"Oki Doki! Bai Bai!", ephemeral=False)
            exit()
        else:
            await interaction.response.send_message(f"Hmm yeah that didn't go as planned", ephemeral=False)
    else:
        log(f"{interaction.user.mention} is not allowed to stop the bot, tried it from {interaction.guild_id}")
        await interaction.response.send_message(f"You are not an authorized user!", ephemeral=False)

@bot.tree.command(name="omac")
async def omac(interaction: discord.Interaction):
    global accountData
    accountData = accounts_omac.saveAccount(accountData, configSettings)
    log(f"{interaction.user.mention} looked at the account data", "stalk")
    await interaction.response.send_message(f"{accountData}", ephemeral=False)

@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    log(f"{interaction.user.mention} likes to play pingpong", "stalk")
    await interaction.response.send_message(f"Pong!", ephemeral=False)

@bot.tree.command(name="my_uid")
async def my_uid(interaction: discord.Interaction):
    log(f"{interaction.user.mention} requested his own ID", "stalk")
    await interaction.response.send_message(f"Your user ID: <{interaction.user.mention.split('@')[1]}", ephemeral=False)

@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    log(f"{interaction.user.mention} needed help with the commands", "stalk")
    embed1=discord.Embed(title="Basic commands:", description="You're welcome :)", color=0x15bcf4)
    embed1.add_field(name="/make_server", value="It makes a server", inline=True)
    embed1.add_field(name="/ping", value="see if the bot works", inline=True)
    embed1.add_field(name="/my_uid", value="get your user ID", inline=True)
    embed1.add_field(name="/help", value="get this box", inline=True)
    button1 = Button(label="MORE!", style=discord.ButtonStyle.green)
    button2 = Button(label="I wanna go bacc :c", style=discord.ButtonStyle.blurple)
    embed2=discord.Embed(title="Admin commands:", description="U greedy basterd", color=0x15bcf4)
    embed2.add_field(name="/list_servers", value="List the servers", inline=True)
    embed2.add_field(name="/stop", value="stop the bot", inline=True)
    embed2.set_footer(text="Now happy?")

    view1 = View()
    view2 = View()
    view1.add_item(button1)
    view2.add_item(button2)

    async def button_callback2(interaction):
        log(f"{interaction.user.mention} navigated back to the first help page", "stalk")
        await interaction.response.send_message("You asked for help, so here i am!",embed=embed1, view=view1)
    async def button_callback1(interaction):
        log(f"{interaction.user.mention} navigated to the second help page", "stalk")
        await interaction.response.send_message("You asked for help, so here i am!",embed=embed2, view=view2)
    button1.callback = button_callback1
    button2.callback = button_callback2

    await interaction.response.send_message("You asked for help, so here i am!",embed=embed1, view=view1)

def getBotStats(bot):
    log("bot is Up and Ready!")
    log("-----------------------------------------------")
    log(f"Bot logged in as: '{bot.user}'")
    log(f"Bot ID: {bot.user.id}")
    log(f"Version of Discord.py: {discord.__version__}")
    log(f"Servers: {len(bot.guilds)}")
    log("    Name: ID")
    for server in bot.guilds:
        log(f"    {server.name}: {server.id}")
    log("-----------------------------------------------")

def stringToAscii(seedString:str): #turns everything into ther ASCII value
    seedList = []
    for x in seedString:
        seedList.append(ord(x))#change every character into its ASCII value
    seedString = ''.join([str(elem) for elem in seedList])#add list together into string
    seed = int(seedString)
    return seed

def saveFile(file, data):
    log(f"{file}.json has been saved", "modify")
    with open(f'{file}.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    return True

def createServer(data: str = '', pincode: int = 0):
    global userDict, gamesDict, serverIdNumber
    while f"{serverIdNumber}" in gamesDict:
        serverIdNumber += 1
    serverId = f"{serverIdNumber}"
    gamesDict[f"{serverId}"] = {"host": data.user.mention, "passcode": pincode, "players": {data.user.mention : 'player1'}}
    if data.user.mention in userDict and "server" in userDict[data.user.mention]:
        userDict[data.user.mention]["server"] = f"{serverId}"
    else:
        userDict[data.user.mention] = {"server":f"{serverId}"}
    log(f"{data.user.mention} is now linked to a server: {serverId}", "debug")
    return True

stopTheGame = False

#app data
appIDorName = 'UNO3byMarjinIDKDiscordBotTesting'
windowTitles = 'UNO'

#create seed
seed = accounts_omac.easy.stringToAscii(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
#if True:
#    seed = 4852474849475048505044324951585150585154
random.seed(seed)
print(seed)

#account login
configSettings = accounts_omac.configFileTkinter()
accountData = accounts_omac.defaultConfigurations.defaultLoadingTkinter(configSettings)
if accountData == False:
    exit()

if appIDorName not in accountData['appData']:
    accountData['appData'][appIDorName] = {}
if appIDorName not in accountData['collectables']:
    accountData['collectables'][appIDorName] = {}
if appIDorName not in accountData['achievements']:
    accountData['achievements'][appIDorName] = {}

def accountDataUpdate(thing):
    global accountData
    if thing not in accountData['appData'][appIDorName]:
        accountData['appData'][appIDorName][thing] = 1
    else:
        accountData['appData'][appIDorName][thing] += 1
    accountData = accounts_omac.saveAccount(accountData, configSettings)

oopsieErrorCode = '''OOPSIE WOOPSIE!!
UwU We made a fucky wucky!! A
wittle fucko boingo! The code
monkeys at our headquarters are
working VEWY HAWD to fix this!'''




bots = 4
players = 0
cardsPerPlayer = 7
whenReshuffle = 4

playerDict = {}
playerList = []
gameData = {'playerDict': playerDict, 
            'playerList': playerList, 
            'turn': 0, 
            'active': 0, 
            'direction':'1', 
            'plusCardActive': 0,
            'grabCardsDeck': [],
            'playedCardsDeck': [],
            'playerHistory': [],
            'cardInfo' : {},
            'wildInfo': {'played': False, 'chosenColor': 'blue', 'colors': []},
            'statistics': {'winOrder':[]}}

def gotAchievement(title, description, message):
    global accountData
    now = datetime.datetime.now()
    if title not in accountData['achievements'][appIDorName]:
        notLinked = dict(accountData)
        accountData = accounts_omac.saveAccount(accountData, configSettings)
        accountData['achievements'][appIDorName][title] = {'title':title, 'description': description, 'message': message, 'date': now.strftime("%m/%d/%Y, %H:%M:%S"), 'timePlayedWhen':notLinked["time"]}
        accountData = accounts_omac.saveAccount(accountData, configSettings)


######################## Read if JSON Exists ########################


#without this it can't load a json nor create a new json with the cards
try:
    if os.path.isfile(f"gameData/cardsDict.json"):
        with open(f"gameData/cardsDict.json") as json_file_cardsDict:
            dataString_cardsDict = json.load(json_file_cardsDict)
            #this makes it so if u use a json beautifier that makes it not being a string anymore, it would still work
            if type(dataString_cardsDict) == list:
                data_cardsDictList = dataString_cardsDict
            else:
                data_cardsDictList = json.loads(dataString_cardsDict)
            data_cardsDict = data_cardsDictList[0]   
            data_cardsList = data_cardsDictList[1]
            colorsInJson = data_cardsDictList[2]
    else:
        raise ImportError("You need to create playingcards .json files somewhere else")
except Exception as e:
    log(e, "error")
    exit()

######################## Player Select Menu ########################

def selectedPlayers(*args):
    global data_cardsList
    global gameData
    global bots, players
    #amounts of times to import the carddeck
    totalAmount = bots + players
    data_cardsList = [val for val in data_cardsList for _ in range((totalAmount + 10) // 10)]
    gameData['active'] = random.randint(0,players + bots-1)

######################## Game Setup ########################

def createPlayer(botOrHuman, playerNumber, name = 'herman'):
    '''Creates a player or bot, depending on the input'''
    global gameData
    gameData['playerDict'][f'player {playerNumber}'] = {'type': botOrHuman,
                                                'name': name,
                                                'number': playerNumber + 1,
                                                'cards': [],
                                                'effect': {},
                                                'playedCards': {},
                                                'programSettings': {'typeOfSelect': 'default', 'showColor': True, 'defaultBGwidget': '#f0f0f0', 'defaultFGwidget': 'black','defaultBGwindow': '#f0f0f0'}}
    
    #without this, you wouldn't know which plaers would exist
    gameData['playerList'].append(f'player {playerNumber}')

#so you don't have the same player number for a bot and human
num = 0
#create bots and humans
for x in range(players):
    createPlayer('Human', num)
    num += 1
for x in range(bots):
    createPlayer('Bot', num)
    num += 1

#adding it to the gamedata, so it can be used in game
gameData['grabCardsDeck'] = list(data_cardsList)
gameData['cardInfo'] = dict(data_cardsDict)
gameData['wildInfo']['colors'] = colorsInJson

#would you want to play with a unshuffled deck of cards, me neither.
random.shuffle(gameData['grabCardsDeck'])

def grabCard(activePlayer, achievement = True):
    global gameData
    if len(gameData['grabCardsDeck']) <= whenReshuffle:
        if len(gameData['playedCardsDeck']) == 1:
            pass
        else:
            for _ in range(len(gameData['playedCardsDeck'])-1):
                gameData['grabCardsDeck'].append(gameData['playedCardsDeck'][0])
                gameData['playedCardsDeck'].pop(0)
    if len(gameData['grabCardsDeck']) == 0:
        showerror(title='Ewwor code: 0000001x1a',message =oopsieErrorCode)

    else:
        gameData['playerDict'][gameData['playerList'][activePlayer]]['cards'].append(gameData['grabCardsDeck'][0])
        gameData['grabCardsDeck'].pop(0)


#give players cards
def giveDeckOfCards(achievements = True):
    global gameData
    for i in range(len(gameData['playerList'])):
        for _ in range(cardsPerPlayer):
            grabCard(i, achievements)
        #gameData['playerDict'][gameData['playerList'][i]]['cards'].append('Wild')
            #gameData['playerDict'][gameData['playerList'][i]]['cards'].append('Red Skip')

            


#get the first card
gameData['playedCardsDeck'].append(gameData['grabCardsDeck'][0])
gameData['playerHistory'].append('NONE')
gameData['grabCardsDeck'].pop(0)
while gameData['cardInfo'][gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]]['wild'] == True:
    gameData['playedCardsDeck'].append(gameData['grabCardsDeck'][0])
    gameData['playerHistory'].append('NONE')
    gameData['grabCardsDeck'].pop(0)

giveDeckOfCards(False)

######################## Turns of players / bots ########################

def someoneWon():
    global gameData
    gameData['statistics']['winOrder'].append(gameData['playerList'][gameData['active']])
    gameData['playerList'].pop(gameData['active'])
    if int(gameData['direction']) > 0:
        gameData['active'] = noIndexError(gameData['active'] - 1,len(gameData['playerList'])-1)
    else:
        gameData['active'] = noIndexError(gameData['active'] + 1,len(gameData['playerList'])-1)






#to not get those nasty index out of range errors, you try to get item 20 out of 19 items, this will return you item 0
def noIndexError(number, maxNumber, minNumber = 0):
    '''to not get those nasty index out of range errors, you try to get item 20 out of 19 items, this will return you item 0'''
    while number > maxNumber or number < minNumber:
        if number > maxNumber:
            number -= maxNumber+1
        elif number < minNumber:
            number += maxNumber + 1
    return number

def generateNameList():
    global nameAndCardList, nameList
    activePlayer = gameData['active']
    nameAndCardList = list()
    nameList = list()
    for x in range(len(gameData['playerList'])):
        if int(gameData['direction']) < 0 or gameData['direction'] == '-0':
            nameList.append(f"{gameData['playerDict'][gameData['playerList'][noIndexError(activePlayer -(1+x), len(gameData['playerList'])-1)]]['number']}.{gameData['playerDict'][gameData['playerList'][noIndexError(activePlayer -(1+x), len(gameData['playerList'])-1)]]['name']}")
            nameAndCardList.append(f"{nameList[x]} ({len(gameData['playerDict'][gameData['playerList'][noIndexError(activePlayer -(1+x), len(gameData['playerList'])-1)]]['cards'])} cards) ")
        else:
            nameList.append(f"{gameData['playerDict'][gameData['playerList'][noIndexError(activePlayer + x +1, len(gameData['playerList'])-1)]]['number']}.{gameData['playerDict'][gameData['playerList'][noIndexError(activePlayer + x + 1, len(gameData['playerList'])-1)]]['name']}")
            nameAndCardList.append(f"{nameList[x]} ({len(gameData['playerDict'][gameData['playerList'][noIndexError(activePlayer + x +1, len(gameData['playerList'])-1)]]['cards'])} cards) ")


#play a card
def playCard(card):
    global gameData
    global nameAndCardList
    if gameData['plusCardActive'] > 0 and gameData['cardInfo'][card]['plus'] == 0:
        for _ in range(gameData['plusCardActive']):
            grabCard(gameData['active'])
        if gameData['playerDict'][gameData['playerList'][gameData['active']]]['type'] == 'Human':
            showinfo(title=windowTitles,message =f'You grabbed {gameData["plusCardActive"]} cards, since the last card was a + card.\nSelect again which card you want to play')
            generateNameList()
        gameData['plusCardActive'] = 0
        return
    if gameData['playerDict'][gameData['playerList'][gameData['active']]]['type'] == 'Human':
        pass
    gameData['playerHistory'].append(gameData['playerList'][gameData['active']])
    if gameData['cardInfo'][card]['suckDragon']:
        gameData['playerDict'][gameData['playerList'][gameData['active']]]['cards'].remove(card)    
        for x in range(len(gameData['playerList'])):
            for _ in range(len(gameData['playerDict'][gameData['playerList'][x]]['cards'])):
                gameData['playedCardsDeck'].append(gameData['playerDict'][gameData['playerList'][x]]['cards'][0])
                gameData['playerDict'][gameData['playerList'][x]]['cards'].pop(0)
        gameData['playedCardsDeck'].append(card)
        giveDeckOfCards()
    else:
        gameData['playerDict'][gameData['playerList'][gameData['active']]]['cards'].remove(card)    
        gameData['playedCardsDeck'].append(card)
    if gameData['cardInfo'][card]['exchangeDecks'] > 0:
        listOfDecks = []
        for x in range(len(gameData['playerList'])):
            listOfDecks.append(gameData['playerDict'][gameData['playerList'][x]]['cards'])
        for x in range(len(gameData['playerList'])):
            gameData['playerDict'][gameData['playerList'][x]]['cards'] = listOfDecks[noIndexError(x-gameData['cardInfo'][card]['exchangeDecks'], len(gameData['playerList'])-1)]

    if gameData['cardInfo'][card]['shuffleOrder']:
        placeholder = gameData['playerList'][gameData['active']]
        gameData['playerList'].pop(gameData['active'])
        random.shuffle(gameData['playerList'])
        gameData['playerList'].append(placeholder)
        gameData['active'] = len(gameData['playerList'])-1

    if gameData['cardInfo'][card]['dualWielding']:
        if int(gameData['direction']) > 0:
            gameData['direction'] = '0'
        else:
            gameData['direction'] = '0'

    if gameData['cardInfo'][card]['wild'] and gameData['playerDict'][gameData['playerList'][gameData['active']]]['type'] == 'Human':
        pass


    elif gameData['cardInfo'][card]['wild'] and gameData['playerDict'][gameData['playerList'][gameData['active']]]['type'] == 'Bot':
        activePlayer = gameData['active']
        colorsDict = {}
        for i in range(len(gameData['playerDict'][gameData['playerList'][activePlayer]]['cards'])):
            current = gameData['playerDict'][gameData['playerList'][activePlayer]]['cards'][i]
            if gameData['cardInfo'][current]['color'] in colorsDict:
                colorsDict[gameData['cardInfo'][current]['color']] += 1
            else:
                colorsDict[gameData['cardInfo'][current]['color']] = 1
        while max(colorsDict, key=colorsDict.get) not in gameData['wildInfo']['colors']:
            del colorsDict[max(colorsDict, key=colorsDict.get)]
        gameData['wildInfo']['chosenColor'] = max(colorsDict, key=colorsDict.get)
        gameData['wildInfo']['played'] = True

    else:
        gameData['wildInfo']['played'] = False
    if gameData['cardInfo'][card]['plus'] != 0:
        gameData['plusCardActive'] += gameData['cardInfo'][card]['plus']
    if gameData['cardInfo'][card]['reverse']:
        if gameData['direction'] == '0':
            gameData['direction'] = '-0'
        gameData['direction'] = str(int(gameData['direction']) * -1) 
    if gameData['cardInfo'][card]['skip'] > 0:
        if int(gameData['direction']) > 0:
            gameData['direction'] = str(int(gameData['direction'])+gameData['cardInfo'][card]['skip'])
        else:
            gameData['direction'] = str(int(gameData['direction'])-gameData['cardInfo'][card]['skip'])
    if gameData['cardInfo'][card]['dualWielding']:
        if int(gameData['direction']) > 0:
            gameData['direction'] = str(int(gameData['direction'])-1)
        else:
            gameData['direction'] = str(int(gameData['direction'])+1)
    if len(gameData['playerDict'][gameData['playerList'][gameData['active']]]['cards']) == 0:
        someoneWon()
    


#is it playable tho??
def checkIfCardPlayable(selected,mode = True):
    if selected != '':
        if gameData['cardInfo'][selected]['alwaysPlayable']:
            if mode == False:
                return True
            else:
                playCard(selected)
        elif gameData['cardInfo'][selected]['type'] == gameData['cardInfo'][gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]]['type']:
            if mode == False:
                return True
            else:
                playCard(selected)
        elif gameData['cardInfo'][selected]['color'] == gameData['cardInfo'][gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]]['color']:
            if mode == False:
                return True
            else:
                playCard(selected)
        elif gameData['cardInfo'][gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]]['alwaysPlayable'] and not gameData['cardInfo'][gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]]['wild']:
            if mode == False:
                return True
            else:
                playCard(selected)
        elif gameData['wildInfo']['played'] and gameData['cardInfo'][selected]['color'] == gameData['wildInfo']['chosenColor']:
            if mode == False:
                return True
            else:
                playCard(selected)
        else:
            if mode == False:
                return False
            else:
                accountDataUpdate('can\'t play that')
    else:
        showwarning(title=windowTitles,message ='Uno\nYou might want to pick a card')
        if 'pickACardError' not in accountData['appData'][appIDorName]:
            accountData['appData'][appIDorName]['pickACardError'] = 1
        else:
            accountData['appData'][appIDorName]['pickACardError'] += 1

#who is the next player if you play this car
def nextPlayer(card = 'NONE'):
    if card == 'NONE':
        direction = str(gameData['direction'])
        return noIndexError(gameData['active'] + int(direction), len(gameData['playerList'])-1)
    else:
        direction = str(gameData['direction'])
        
        if gameData['cardInfo'][card]['reverse']:
            direction = str(int(direction) * -1)
        if gameData['cardInfo'][card]['skip'] > 0:
            if int(direction) > 0:
                direction = str(int(direction)+gameData['cardInfo'][card]['skip'])
            else:
                direction = str(int(direction)-gameData['cardInfo'][card]['skip'])
        if gameData['cardInfo'][card]['dualWielding']:
            if int(direction) > 0:
                direction = str(int(direction)-1)
            else:
                direction = str(int(direction)+1)
        return noIndexError(gameData['active'] + int(direction), len(gameData['playerList'])-1)


#show what the card does
def generateCardTip(card):
    text = f"Card color: {gameData['cardInfo'][card]['color']}\nCard type: {gameData['cardInfo'][card]['type']}\n"
    if checkIfCardPlayable(card,False):
        text += 'This card is playable at this moment'
    else:
        text += 'This card is not playable at this moment'
    text += '\nWhen you play this card, the following would happen:'
    if nextPlayer(card) != gameData['active']:
        nextPlayerReturn = gameData["playerList"][nextPlayer(card)]
        text += f'\nThe next player would be {gameData["playerDict"][nextPlayerReturn]["number"]}.{gameData["playerDict"][nextPlayerReturn]["name"]}'
    else:
        text += f'\nAfter this card it\'s your turn again'
    if gameData['cardInfo'][card]['suckDragon']:
        text += f'\nEveryones cards would be taken and be given {cardsPerPlayer} new cards.'
    if gameData['cardInfo'][card]['shuffleOrder']:
        text += f'\nThe order of player turns would be shuffled randomly.'
    if gameData['cardInfo'][card]['wild']:
        text += f'\nYou would be able to choose the color of the next card.'
    if gameData['cardInfo'][card]['reverse']and gameData['cardInfo'][card]['shuffleOrder'] == False:
        text += f'\nThe order of players is reversed'
    if gameData['cardInfo'][card]['plus'] != 0:
        if gameData['plusCardActive'] > 0:
            text += f'\nThe next player will have to draw {gameData["cardInfo"][card]["plus"]} cards from the pile + {gameData["plusCardActive"]} from previous cards,\nunless they have a card with the simular function of making people draw cards.'
        else:
            text += f'\nThe next player will have to draw {gameData["cardInfo"][card]["plus"]} cards from the pile,\nunless they have a card with the simular function of making people draw cards.'
    elif gameData['plusCardActive'] > 0:
        text += f'\nYou will have to draw {gameData["plusCardActive"]} cards because of previous cards.'
    if gameData['cardInfo'][card]['exchangeDecks'] > 0:
        if gameData['cardInfo'][card]['exchangeDecks'] == 1:
            text += f'\nEveryone switches cards with the {gameData["cardInfo"][card]["exchangeDecks"]}st player before them'
        elif gameData['cardInfo'][card]['exchangeDecks'] == 2:
            text += f'\nEveryone switches cards with the {gameData["cardInfo"][card]["exchangeDecks"]}nd player before them'
        elif gameData['cardInfo'][card]['exchangeDecks'] == 3:
            text += f'\nEveryone switches cards with the {gameData["cardInfo"][card]["exchangeDecks"]}rd player before them'
        else:
            text += f'\nEveryone switches cards with the {gameData["cardInfo"][card]["exchangeDecks"]}th player before them'
    


    return text

def grabFromPile(*args):
 
    if gameData['plusCardActive'] > 0:
        for _ in range(gameData['plusCardActive']):
            grabCard(gameData['active'])
        showinfo(title=windowTitles,message =f'You grabbed {gameData["plusCardActive"]} cards, since the last card was a + card.\nSelect again which card you want to play')
        gameData['plusCardActive'] = 0
        generateNameList()
        return
    else:
        grabCard(gameData['active'])
    if gameData['playerDict'][gameData['playerList'][gameData['active']]]['type'] == 'Human':
        pass



######################## player turn ########################

def playerTurn():
    global gameData
    global nameAndCardList, nameList
    activePlayer = gameData['active']

    #the combobox with player order
    generateNameList()
    

def botTurn():
    global gameData
    
    lastPlayed = gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]
    activePlayer = gameData['active']
    listOfMoves = []
    colorsDict = {}
    for i in range(len(gameData['playerDict'][gameData['playerList'][activePlayer]]['cards'])):
        current = gameData['playerDict'][gameData['playerList'][activePlayer]]['cards'][i]
        if gameData['cardInfo'][current]['color'] in colorsDict:
            colorsDict[gameData['cardInfo'][current]['color']] += 1
        else:
            colorsDict[gameData['cardInfo'][current]['color']] = 1

    playerWithCards= {}    
    for i in range(len(gameData['playerList'])):
        playerWithCards[gameData['playerList'][i]] = len(gameData['playerDict'][gameData['playerList'][i]]['cards'])


    for i in range(len(gameData['playerDict'][gameData['playerList'][activePlayer]]['cards'])):
        current = gameData['playerDict'][gameData['playerList'][activePlayer]]['cards'][i]     
        if not checkIfCardPlayable(current, False):
            listOfMoves.append(-1)
        else:
            listOfMoves.append(1)
            if gameData['cardInfo'][current]['wild']:
                if gameData['cardInfo'][lastPlayed]['color'] in colorsDict:
                    listOfMoves[i] += 3
                else:
                    listOfMoves[i] += 5
            if gameData['cardInfo'][lastPlayed]['type'] == gameData['cardInfo'][current]['type']:
                if max(colorsDict, key=colorsDict.get) == gameData['cardInfo'][current]['color']:
                    listOfMoves[i] += 8
                else:
                    listOfMoves[i] += 6
            if gameData['cardInfo'][current]['suckDragon']:
                listOfMoves[i] -= 1
            if gameData['playerList'][nextPlayer(current)] == gameData['playerList'][activePlayer]:
                if gameData['cardInfo'][current]['plus'] > 0:
                    listOfMoves[i] -= 2
                else:
                    listOfMoves[i] += (gameData['cardInfo'][current]['plus'] + 3)
            elif gameData['playerList'][nextPlayer(current)] == min(playerWithCards, key=playerWithCards.get):
                if gameData['cardInfo'][current]['shuffleOrder']:
                    listOfMoves[i] += 2
                elif gameData['cardInfo'][current]['plus'] > 0:
                    listOfMoves[i] += 5
                else:
                    listOfMoves[i] -= 2
            else:
                listOfMoves[i] += 2
            if len(gameData['playerDict'][gameData['playerList'][nextPlayer(current)]]['cards']) > len(gameData['playerDict'][gameData['playerList'][nextPlayer()]]['cards']):
                if not gameData['cardInfo'][current]['shuffleOrder']:
                    listOfMoves[i] += 2
            if gameData['cardInfo'][current]['alwaysPlayable']:
                listOfMoves[i] -= 2
            if gameData['cardInfo'][current]['exchangeDecks'] > 0:
                numberOfYourCards = len(gameData['playerDict'][gameData['playerList'][activePlayer]]['cards'])
                numberOfCards = len(gameData['playerDict'][gameData['playerList'][noIndexError(activePlayer-gameData['cardInfo'][current]['exchangeDecks'], len(gameData['playerList'])-1)]]['cards'])
                if numberOfCards < numberOfYourCards-1:
                    listOfMoves[i] += (3 + ((numberOfYourCards-1) - numberOfCards))
                elif numberOfCards == numberOfYourCards-1:
                    listOfMoves[i] += 2
                else:
                    listOfMoves[i] -= 2
                numberOfNextPlayersCards = len(gameData['playerDict'][gameData['playerList'][nextPlayer(current)]]['cards'])
                numberOfCards = len(gameData['playerDict'][gameData['playerList'][noIndexError(nextPlayer(current)-gameData['cardInfo'][current]['exchangeDecks'], len(gameData['playerList'])-1)]]['cards'])
                if numberOfCards < numberOfNextPlayersCards-1:
                    listOfMoves[i] -= (1 + ((numberOfNextPlayersCards) - numberOfCards))
                elif numberOfCards == numberOfNextPlayersCards:
                    listOfMoves[i] += 1
                else:
                    listOfMoves[i] += (2 + (numberOfCards - (numberOfNextPlayersCards)))
            if listOfMoves[i] < 1:
                listOfMoves[i] = 1
            

                




    if gameData['playerDict'][gameData['playerList'][activePlayer]]['cards'][listOfMoves.index(max(listOfMoves))] == '+4':
        pass
    if max(listOfMoves) != -1: 
        playCard(gameData['playerDict'][gameData['playerList'][activePlayer]]['cards'][listOfMoves.index(max(listOfMoves))])
    else:
        grabCard(gameData['active'],False)




def betweenTruns():
    gameData['active'] = noIndexError(gameData['active'] + int(gameData['direction']), len(gameData['playerList'])-1)
    if int(gameData['direction']) > 0:
        gameData['direction'] = '1'
    else:
        gameData['direction'] = '-1'
    if gameData['playerDict'][gameData['playerList'][gameData['active']]]['type'] == 'Human':
        playerTurn()
    else:
        botTurn()


# while len(gameData['playerList']) > 1 and not stopTheGame:
#     betweenTruns()
# endingResultText = ''
# for x in range(len(gameData['statistics']['winOrder'])):
#     if x == 0:
#         endingResultText += f"Winner: {gameData['playerDict'][gameData['statistics']['winOrder'][x]]['number']}.{gameData['playerDict'][gameData['statistics']['winOrder'][x]]['name']}\n"
#     elif x == 1:
#         endingResultText += f"Second place: {gameData['playerDict'][gameData['statistics']['winOrder'][x]]['number']}.{gameData['playerDict'][gameData['statistics']['winOrder'][x]]['name']}\n"
#     elif x == 2:
#         endingResultText += f"Third place: {gameData['playerDict'][gameData['statistics']['winOrder'][x]]['number']}.{gameData['playerDict'][gameData['statistics']['winOrder'][x]]['name']}\n"
#     else:
#         endingResultText += f"{x}th: {gameData['playerDict'][gameData['statistics']['winOrder'][x]]['number']}.{gameData['playerDict'][gameData['statistics']['winOrder'][x]]['name']}\n"
# for y in range(len(gameData['playerList'])):
#     endingResultText+= f"Not finished: {gameData['playerDict'][gameData['playerList'][y]]['number']}.{gameData['playerDict'][gameData['playerList'][y]]['name']}\n"
# showinfo(title=windowTitles,message =f'{endingResultText}')

bot.run(token=secretsDict["BotToken"])