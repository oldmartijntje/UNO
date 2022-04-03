from datetime import datetime
import os
import json
import accounts_omac
import tkinter
from tkinter import ttk
import random
from tkinter.messagebox import showerror, showinfo, showwarning
import tkinter.messagebox

def on_closing(windowTitles = '<3'):
    global data, stopTheGame
    if tkinter.messagebox.askokcancel(windowTitles, f"Your program will be terminated\nShould we proceed?", icon ='warning'):
        data = accounts_omac.saveAccount(data, configSettings)
        exit()

stopTheGame = False

#app data
appIDorName = 'UNO2byMarjinIDK'
windowTitles = 'UNO'

#create seed
seed = accounts_omac.easy.stringToAscii(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
if True:
    seed = 4852474849475048505044324951585150585154
random.seed(seed)
print(seed)

#account login
configSettings = accounts_omac.configFileTkinter()
data = accounts_omac.defaultConfigurations.defaultLoadingTkinter(configSettings)
if data == False:
    exit()

if appIDorName not in data['appData']:
    data['appData'][appIDorName] = {}
if appIDorName not in data['collectables']:
    data['collectables'][appIDorName] = {}
if appIDorName not in data['achievements']:
    data['achievements'][appIDorName] = {}

#create achievements
def gotAchievement(title, description, message):
    global data
    now = datetime.now()
    if title not in data['achievements'][appIDorName]:
        data = accounts_omac.saveAccount(data, configSettings)
        data['achievements'][appIDorName][title] = {'title':title, 'description': description, 'message': message, 'date': now.strftime("%m/%d/%Y, %H:%M:%S"), 'timePlayedWhen':data["time"]}
        showinfo(title=windowTitles,message =f'''Congratulations, you got the {title} achievement!
AKA: {description}

{message}''')
        data = accounts_omac.saveAccount(data, configSettings)

def accountDataUpdate(thing):
    global data
    if thing not in data['appData'][appIDorName]:
        data['appData'][appIDorName][thing] = 1
    else:
        data['appData'][appIDorName][thing] += 1
    data = accounts_omac.saveAccount(data, configSettings)

oopsieErrorCode = '''OOPSIE WOOPSIE!!
UwU We made a fucky wucky!! A
wittle fucko boingo! The code
monkeys at our headquarters are
working VEWY HAWD to fix this!'''




bots = 4
players = 2
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

#without it there wouldn't be a folder to put the jsons in
accounts_omac.easy.createPathIfNotThere('gameData/')


######################## Read if JSON Exists ########################


#without this it can't load a json nor create a new json with the cards
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
    if os.path.isfile(f"gameData/cardsCreation.json"):
        with open(f"gameData/cardsCreation.json") as json_file_cardsCreation:
            dataString_cardsCreation = json.load(json_file_cardsCreation)
            #this makes it so if u use a json beautifier that makes it not being a string anymore, it would still work
            if type(dataString_cardsCreation) == dict:
                data_cardsCreation = dataString_cardsCreation
            else:
                data_cardsCreation = json.loads(dataString_cardsCreation)
        
        ######################## Basic JSON Creation ########################

    else:
        data_cardsCreation = {'colors': ['Red', 'Yellow', 'Green', 'Blue'],
                            'displayColorsBG' : ['red', 'yellow', 'green', 'blue'],
                            'displayColorsFG' : ['black', 'black', 'black', 'black'],
                            'cardsPerColor': [0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,'+2', '+2', 'Skip', 'Skip', 'Reverse', 'Reverse'],
                            'special': ['+4', 'Wild', '+4', 'Wild', '+4', 'Wild', '+4', 'Wild'],
                            'specialFG': 'white', 
                            'specialBG': 'black', 
                            'specialColor': 'Black'}

        json_string_cardsCreation = json.dumps(data_cardsCreation)
        with open(f"gameData/cardsCreation.json", 'w') as outfile:
            json.dump(json_string_cardsCreation, outfile)

    
######################## creation of the second json file ########################

    def changeCards(name):
        '''automatically creates card data based on the name, like \'skip\' will automatically be detected a s a skip card'''
        global data_cardsDict
        nameLowered = name.lower()
        if 'reverse' in nameLowered:
                data_cardsDict[name]['reverse'] = True
        if 'skip' in nameLowered:
            test = nameLowered.split('skip')
            if accounts_omac.removeCharacters(test[1]).isnumeric():
                data_cardsDict[name]['skip'] = int(accounts_omac.removeCharacters(test[1],"!\"#$%&'()*+,./:;<=>?@[\]^_`{|}~"))
            else:
                data_cardsDict[name]['skip'] = 1
        if '+' in nameLowered:
            test = nameLowered.split('+')
            if accounts_omac.removeCharacters(test[1]).isnumeric():
                data_cardsDict[name]['plus'] = int(accounts_omac.removeCharacters(test[1],"!\"#$%&'()*+,./:;<=>?@[\]^_`{|}~"))
            else:
                data_cardsDict[name]['plus'] = 1
        if 'wild' in nameLowered:
                data_cardsDict[name]['wild'] = True
        if 'shuffle' in nameLowered:
                data_cardsDict[name]['shuffleOrder'] = True
        if 'suckdragon' in nameLowered:
                data_cardsDict[name]['suckDragon'] = True
        if 'deck' in nameLowered:
            test = nameLowered.split('deck')
            if accounts_omac.removeCharacters(test[1]).isnumeric():
                data_cardsDict[name]['exchangeDecks'] = int(accounts_omac.removeCharacters(test[1],"!\"#$%&'()*+,./:;<=>?@[\]^_`{|}~"))
            else:
                data_cardsDict[name]['exchangeDecks'] = 1


    data_cardsList = []
    data_cardsDict = {}
    #creates the dict with card data, for every color the same set
    for x in range(len(data_cardsCreation['colors'])):
        for y in range(len(data_cardsCreation['cardsPerColor'])):
            data_cardsDict[f'{data_cardsCreation["colors"][x]} {data_cardsCreation["cardsPerColor"][y]}'] = {'color': f'{data_cardsCreation["colors"][x]}',
                                                                                                            'type': f'{data_cardsCreation["cardsPerColor"][y]}',
                                                                                                            'alwaysPlayable': False,
                                                                                                            'plus': 0,
                                                                                                            'reverse': False,
                                                                                                            'skip': 0,
                                                                                                            'wild': False,
                                                                                                            'dualWielding' : False,
                                                                                                            'shuffleOrder': False,
                                                                                                            'suckDragon': False,
                                                                                                            'exchangeDecks': 0,
                                                                                                            'displayBGColor': f'{data_cardsCreation["displayColorsBG"][x]}',
                                                                                                            'displayFGColor': f'{data_cardsCreation["displayColorsFG"][x]}'}
                                                                                             
            changeCards(f'{data_cardsCreation["colors"][x]} {data_cardsCreation["cardsPerColor"][y]}')
            #adds card to the list, so we know how many of each kind we have per game
            data_cardsList.append(f'{data_cardsCreation["colors"][x]} {data_cardsCreation["cardsPerColor"][y]}')

    #creates dict with card data for cards without colors
    for i in range(len(data_cardsCreation['special'])):
        data_cardsDict[f'{data_cardsCreation["special"][i]}'] = {'color': 'NONE',
                                                                'type': f'{data_cardsCreation["special"][i]}',
                                                                'alwaysPlayable': True,
                                                                'plus': 0,
                                                                'reverse': False,
                                                                'skip': 0,
                                                                'wild': False,
                                                                'dualWielding' : False,
                                                                'shuffleOrder': False,
                                                                'suckDragon': False,
                                                                'exchangeDecks': 0,
                                                                'displayBGColor': f'{data_cardsCreation["specialBG"]}',
                                                                'displayFGColor': f'{data_cardsCreation["specialFG"]}'}

        changeCards(f'{data_cardsCreation["special"][i]}')
        #adds card to the list, so we know how many of each kind we have per game
        data_cardsList.append(f'{data_cardsCreation["special"][i]}')

######################## almost done with creation ########################

    #adds colors to a list, without this you won't know what colors there are when selecting a color with a wild card   
    colorsInJson = data_cardsCreation['colors']
    data_cardsDictList = [data_cardsDict, data_cardsList, colorsInJson]    

    json_string_cardsDictList = json.dumps(data_cardsDictList)
    with open(f"gameData/cardsDict.json", 'w') as outfile:
        json.dump(json_string_cardsDictList, outfile)



######################## Player Select Menu ########################



playerSelectWindow = tkinter.Tk()

def changedSomething(*args):
    if playersAmountSelect_var.get() + botsAmountSelect_var.get() > 1:
        playButton.configure(state='normal')
    else:
        playButton.configure(state='disabled')

def selectedPlayers(*args):
    global data_cardsList
    global gameData
    global bots, players
    #amounts of times to import the carddeck
    totalAmount = playersAmountSelect_var.get() + botsAmountSelect_var.get()
    data_cardsList = [val for val in data_cardsList for _ in range((totalAmount + 10) // 10)]
    bots = botsAmountSelect_var.get()
    players = playersAmountSelect_var.get()
    gameData['active'] = random.randint(0,playersAmountSelect_var.get() + botsAmountSelect_var.get()-1)
    playerSelectWindow.destroy()

    



playersAmountSelect_var = tkinter.IntVar()
botsAmountSelect_var = tkinter.IntVar()
spinboxPlayers = ttk.Spinbox(playerSelectWindow, from_=float("0"), to=float("inf"), textvariable=playersAmountSelect_var).grid(column=1, row=0, ipadx=20, ipady=10)
spinboxBots = ttk.Spinbox(playerSelectWindow, from_=float("0"), to=float("inf"), textvariable=botsAmountSelect_var).grid(column=1, row=1, ipadx=20, ipady=10)
playerLabelSpinbox = tkinter.Label(playerSelectWindow, text = 'amount of players:').grid(column=0, row=0, ipadx=20, ipady=10)
botLabelSpinbox = tkinter.Label(playerSelectWindow, text = 'amount of bots:').grid(column=0, row=1, ipadx=20, ipady=10)
playButton = ttk.Button(playerSelectWindow, text='Play', state='disabled', command=selectedPlayers)
playButton.grid(column=0, row=2, ipadx=20, ipady=10,columnspan=2, sticky="EW")
botsAmountSelect_var.trace('w', changedSomething)
playersAmountSelect_var.trace('w', changedSomething)
playerSelectWindow.protocol("WM_DELETE_WINDOW", on_closing)
playerSelectWindow.mainloop()



######################## Game Setup ########################

def on_closing_turnWindow(windowTitles = '<3'):
    global data, stopTheGame
    if tkinter.messagebox.askokcancel(windowTitles, f"Your program will be terminated\nShould we proceed?", icon ='warning'):
        data = accounts_omac.saveAccount(data, configSettings)
        turnWindow.destroy()
        stopTheGame = True

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
        gotAchievement('oopsie Woopsie', 'You got this error code, noice' , oopsieErrorCode)

    else:
        if achievement:
            accountDataUpdate('grabs')
            if data['appData'][appIDorName]['grabs'] == 100:
                gotAchievement('100 cards', 'You got 100 cards, noice', 'you are either extremely bad, or you just played this a lot')
            elif data['appData'][appIDorName]['grabs'] == 1000:
                gotAchievement('1000 cards', 'You got 1000 cards, that\'s a lot', 'you didn\'t farm this achievement, right?')
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
accountDataUpdate('gamesPlayed')
if data['appData'][appIDorName]['gamesPlayed'] == 100:
    gotAchievement('100 times played', 'You played, or atleast, started this game 100 times', 'are you a fan of it? or are you just farming achievements?')
elif data['appData'][appIDorName]['gamesPlayed'] == 10000:
    gotAchievement('10000 times played', 'You played, or atleast, started this game 10000 times', 'seriously bro, stop it, or not if you like it. Tho i sthill think it\'s mental to play 10000 times')
######################## Turns of players / bots ########################

def someoneWon():
    global gameData
    gameData['statistics']['winOrder'].append(gameData['playerList'][gameData['active']])
    if gameData['playerDict'][gameData['playerList'][gameData['active']]]['type'] == 'Human':
        gotAchievement('first finish', 'the first human player to finish', 'good job little fella, your first win. you will be a legend someday')
        accountDataUpdate('finishes')
        if data['appData'][appIDorName]['finishes'] == 5:
            gotAchievement('5 finishes', '5 local players finished with your account logged in', 'good job, ur probably a pro UNO player now')
        elif data['appData'][appIDorName]['finishes'] == 69:
            gotAchievement('69 finishes', '69 local players finished with your account logged in', 'Even if you farmed this, it\'s still impressive. it probably took you a while')
    else:
        gotAchievement('first bot finish', 'the first bot player to finish', 'yeah, a bot just finished, i know, that\'s a thing that can happen, probably didn\'t know that, don\'t you?')
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
    global wildWindow
    global nameAndCardList
    if gameData['plusCardActive'] > 0 and gameData['cardInfo'][card]['plus'] == 0:
        for _ in range(gameData['plusCardActive']):
            grabCard(gameData['active'])
        if gameData['playerDict'][gameData['playerList'][gameData['active']]]['type'] == 'Human':
            showinfo(title=windowTitles,message =f'You grabbed {gameData["plusCardActive"]} cards, since the last card was a + card.\nSelect again which card you want to play')
            generateNameList()
            cardSelect.configure(values =gameData['playerDict'][gameData['playerList'][gameData['active']]]['cards'])
            playerOrderCombobox.configure(value=nameAndCardList)
        gameData['plusCardActive'] = 0
        return
    if gameData['playerDict'][gameData['playerList'][gameData['active']]]['type'] == 'Human':
        turnWindow.destroy()
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
        def clickedButton(*args):
            global gameData
            gameData['wildInfo']['chosenColor'] = color_var.get()
            gameData['wildInfo']['played'] = True
            wildWindow.destroy()
        def chooseColor(*args):
            chooseColorButton.configure(state='enabled')
        wildWindow = tkinter.Tk()
        tkinter.Label(wildWindow, text = 'choose a color:').grid(row=0,column=0,ipadx=20, ipady=10, sticky="EW")
        color_var = tkinter.StringVar()
        colorComboBox =ttk.Combobox(wildWindow,state='readonly',values = gameData['wildInfo']['colors'])
        colorComboBox.configure(textvariable=color_var)
        colorComboBox.grid(row=0,column=1,ipadx=20, ipady=10, sticky="EW")
        chooseColorButton = ttk.Button(wildWindow,state='disabled',text='Play', command=clickedButton)
        chooseColorButton.grid(row=1,column=0,columnspan=2,ipadx=20, ipady=10, sticky="EW")
        color_var.trace('w',chooseColor)
        wildWindow.protocol("WM_DELETE_WINDOW", on_closing_turnWindow)
        wildWindow.mainloop()

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
                if data['appData'][appIDorName]['can\'t play that'] == 100:
                    gotAchievement('100 nopes', 'u tried 100 times', 'You can\'t play that card right now')
                elif data['appData'][appIDorName]['can\'t play that'] == 1000:
                    gotAchievement('1000 nopes', 'u tried 1000 times', 'you still can\'t play that card right now')
    else:
        showwarning(title=windowTitles,message ='Uno\nYou might want to pick a card')
        if 'pickACardError' not in data['appData'][appIDorName]:
            data['appData'][appIDorName]['pickACardError'] = 1
        else:
            data['appData'][appIDorName]['pickACardError'] += 1
        if data['appData'][appIDorName]['pickACardError'] == 69:
            gotAchievement('fergot to pick a card', 'you fergot to pick a card 69 times.', 'that you forget to pick a card once, okay, 7 times, sure. but 69 times?????')

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
        cardSelect.configure(values =gameData['playerDict'][gameData['playerList'][gameData['active']]]['cards'])
        playerOrderCombobox.configure(value=nameAndCardList)
        return
    else:
        grabCard(gameData['active'])
    if gameData['playerDict'][gameData['playerList'][gameData['active']]]['type'] == 'Human':
        turnWindow.destroy()



######################## player turn ########################

def playerTurn():
    global cardSelect
    global turnWindow
    global gameData
    global playerOrderCombobox
    global nameAndCardList, nameList
    activePlayer = gameData['active']

    #create window
    turnWindow = tkinter.Tk()

    #easy accessable items
    defaultBG = gameData['playerDict'][gameData['playerList'][activePlayer]]['programSettings']['defaultBGwidget']
    defaultFG = gameData['playerDict'][gameData['playerList'][activePlayer]]['programSettings']['defaultFGwidget']
    defaultBGwindow = gameData['playerDict'][gameData['playerList'][activePlayer]]['programSettings']['defaultBGwindow']

    #change the window
    turnWindow.configure(bg=defaultBGwindow)

    #the combobox with player order
    generateNameList()

    #labels
    nameLabel = tkinter.Label(turnWindow, text =f"Current player: {gameData['playerDict'][gameData['playerList'][activePlayer]]['number']}.{gameData['playerDict'][gameData['playerList'][gameData['active']]]['name']}",borderwidth=2, relief="groove", fg = defaultFG, bg =defaultBG)
    nameLabel.grid(column=0, row=0, ipadx=20, ipady=10, sticky="EW", columnspan= 2)
    tkinter.Label(turnWindow,text='PlayerOrder:',bg = defaultBGwindow, fg =defaultFG).grid(column=2, row=0, ipadx=20, ipady=10, sticky="EW")
    tkinter.Label(turnWindow,text='Last played card:', bg = defaultBGwindow, fg =defaultFG).grid(column=0, row=1, ipadx=20, ipady=10, sticky="EW")
    tkinter.Label(turnWindow, text='By:', bg =defaultBGwindow, fg=defaultFG).grid(column=2, row=1, ipadx=20, ipady=10, sticky="EW")
    tkinter.Label(turnWindow, bg = defaultBGwindow).grid(column=0, row=2, ipadx=20, ipady=10, sticky="EW",columnspan= 4)
    tkinter.Label(turnWindow,text = 'Select card to play:', bg =defaultBGwindow, fg= defaultFG).grid(column=0, row=4, ipadx=20, ipady=10, sticky="EW")  

    #what happends when you touch the label with the last played card
    def entering(cardToShow):
        global infoWindow
        try:
            infoWindow = tkinter.Tk()
            infoWindow.geometry(f'+{infoWindow.winfo_pointerx()-infoWindow.winfo_rootx()+2}+{infoWindow.winfo_pointery()-infoWindow.winfo_rooty()+2}')
            infoLabel = ttk.Label(infoWindow)
            infoLabel.configure(text=generateCardTip(cardToShow))
            infoLabel.pack(ipadx=20, ipady=10)
        except Exception as e:
            showwarning(title=windowTitles,message =f'Uno\nCatastrophic failure')

    def enterPrevious(*args):
        entering(gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1])

    def enterSelected(*args):
        if card_var.get() != '':
            entering(card_var.get())
    #close the card info
    def leave(*args):
        try:
            infoWindow.destroy()
        except:
            pass

    #the label of the last played card
    lastPlayed = tkinter.Label(turnWindow, text = f"{gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]}",borderwidth=2, relief="groove")
    if gameData['playerDict'][gameData['playerList'][activePlayer]]['programSettings']['showColor']:
        if gameData['cardInfo'][gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]]['wild']:
            lastPlayed.configure(bg = gameData['wildInfo']['chosenColor'], fg =gameData['cardInfo'][gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]]['displayFGColor'])
        else:
            lastPlayed.configure(bg = gameData['cardInfo'][gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]]['displayBGColor'], fg =gameData['cardInfo'][gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]]['displayFGColor'])
    else:
        lastPlayed.configure(bg = gameData['playerDict'][gameData['playerList'][activePlayer]]['programSettings']['defaultBGwidget'], fg =gameData['playerDict'][gameData['playerList'][x]]['programSettings']['defaultFGwidget'])
    lastPlayed.grid(column=1, row=1, ipadx=20, ipady=10, sticky="EW")
    lastPlayed.bind('<Enter>',enterPrevious)
    lastPlayed.bind('<Leave>',leave)


    #show who played the last card
    playerPlayed = tkinter.Label(turnWindow,borderwidth=2, relief="groove", fg = defaultFG, bg =defaultBG)
    playerPlayed.grid(column=3, row=1, ipadx=20, ipady=10, sticky="EW")
    if gameData['playerHistory'][len(gameData['playerHistory'])-1] == "NONE":
        playerPlayed.configure(text = 'Nobody, it\'s the first card')
    else:
        playerPlayed.configure(text =f"{gameData['playerDict'][gameData['playerHistory'][len(gameData['playerHistory'])-1]]['number']}.{gameData['playerDict'][gameData['playerHistory'][len(gameData['playerHistory'])-1]]['name']}")

    #the combobox of the players
    nextPlayer_var = tkinter.StringVar(value=f'Next player: {nameList[0]}')
    playerOrderCombobox = ttk.Combobox(turnWindow,state='readonly',values = nameAndCardList, textvariable=nextPlayer_var)
    nextPlayer_var.trace('w',lambda *args: nextPlayer_var.set(f'Next player: {nameList[0]}'))
    playerOrderCombobox.grid(column=3, row=0, ipadx=20, ipady=10, sticky="EW")
    
    
    #your cards in combobox or spinbox
    card_var = tkinter.StringVar()
    if gameData['playerDict'][gameData['playerList'][activePlayer]]['programSettings']['typeOfSelect'] == 'default':
        cardSelect = ttk.Combobox(turnWindow)
    else:
        cardSelect = ttk.Spinbox(turnWindow)
    cardSelect.configure(state='readonly', textvariable=card_var, values =gameData['playerDict'][gameData['playerList'][activePlayer]]['cards'])
    cardSelect.grid(column=1, row=4, ipadx=20, ipady=10, sticky="EW",columnspan= 2)

    #info about the selected card
    dataCard= tkinter.Label(turnWindow, text='Card Information',borderwidth=2, relief="groove", fg = defaultFG, bg =defaultBG)
    dataCard.grid(column=3, row=4, ipadx=20, ipady=10, sticky="EW")
    dataCard.bind('<Enter>',enterSelected)
    dataCard.bind('<Leave>',leave)
    
    def closeSettings():
        SettingsWindow.destroy()
        playerTurn()


    def settings():
        def changeSettings(*args):
            global gameData
            if cardColor_var.get() == 1:
                gameData['playerDict'][gameData['playerList'][activePlayer]]['programSettings']['showColor'] = True
            else:
                gameData['playerDict'][gameData['playerList'][activePlayer]]['programSettings']['showColor'] = False
        global SettingsWindow
        turnWindow.destroy()
        SettingsWindow = tkinter.Tk()
        tkinter.Label(SettingsWindow,text='Settings',borderwidth=2, relief="groove").grid(column = 0,row = 0, ipadx=20, ipady=10, sticky="EW",columnspan=4)
        ttk.Label(SettingsWindow,text="show card color:",font=("Comic_Sans",10)).grid(column = 0,row = 1, ipadx=20, ipady=10, sticky="EW")
        cardColor_var = tkinter.IntVar()
        checkbutton_cardColor = tkinter.Checkbutton(SettingsWindow, variable=cardColor_var,onvalue = 1,offvalue = 0)
        checkbutton_cardColor.grid(column = 2,row = 1, ipadx=20, ipady=10, sticky="EW")
        if gameData['playerDict'][gameData['playerList'][activePlayer]]['programSettings']['showColor']:
            cardColor_var.set(1)
        cardColor_var.trace('w',changeSettings)
        SettingsWindow.protocol("WM_DELETE_WINDOW", closeSettings)
        SettingsWindow.mainloop()


    ttk.Button(text="Settings",command=settings).grid(column = 3,row = 5, ipadx=20, ipady=10, sticky="EW")

    ttk.Button(turnWindow, command =lambda: checkIfCardPlayable(card_var.get()), text='Play Selected Card').grid(column = 0,row = 5, ipadx=20, ipady=10, sticky="EW",columnspan= 2)
    grabButton = ttk.Button(turnWindow,text='Grab card from pile',command=grabFromPile)
    grabButton.grid(column = 2,row = 5, ipadx=20, ipady=10, sticky="EW",columnspan= 1)

    

    turnWindow.protocol("WM_DELETE_WINDOW", on_closing_turnWindow)
    turnWindow.mainloop()


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


while len(gameData['playerList']) > 1 and not stopTheGame:
    betweenTruns()
if not stopTheGame:
    gotAchievement('first ending', 'the first time you played till the end of the game', 'you just witnessed a legendary moment, people don\'t come over here often\nMost of the time they already have left because of ragequitting')
else:
    gotAchievement('exit', 'you closed the game', 'you didn\'t like it? :\'(')
endingResultText = ''
for x in range(len(gameData['statistics']['winOrder'])):
    if x == 0:
        endingResultText += f"Winner: {gameData['playerDict'][gameData['statistics']['winOrder'][x]]['number']}.{gameData['playerDict'][gameData['statistics']['winOrder'][x]]['name']}\n"
    elif x == 1:
        endingResultText += f"Second place: {gameData['playerDict'][gameData['statistics']['winOrder'][x]]['number']}.{gameData['playerDict'][gameData['statistics']['winOrder'][x]]['name']}\n"
    elif x == 2:
        endingResultText += f"Third place: {gameData['playerDict'][gameData['statistics']['winOrder'][x]]['number']}.{gameData['playerDict'][gameData['statistics']['winOrder'][x]]['name']}\n"
    else:
        endingResultText += f"{x}th: {gameData['playerDict'][gameData['statistics']['winOrder'][x]]['number']}.{gameData['playerDict'][gameData['statistics']['winOrder'][x]]['name']}\n"
for y in range(len(gameData['playerList'])):
    endingResultText+= f"Not finished: {gameData['playerDict'][gameData['playerList'][y]]['number']}.{gameData['playerDict'][gameData['playerList'][y]]['name']}\n"
showinfo(title=windowTitles,message =f'{endingResultText}')