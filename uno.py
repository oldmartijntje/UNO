import os
import json
import accounts_omac
import tkinter
from tkinter import ttk
import random

appIDorName = 'UNO2byMarjinIDK'

bots = 4
players = 2
cardsPerPlayer = 7

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
            'wildInfo': {'played': False, 'chosenColor': 'blue'},
            'colors': [],
            'statistics': {'winOrder':[]}}

#without it there wouldn't be a folder to put the jsons in
accounts_omac.easy.createPathIfNotThere('gameData/')

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
        colors = data_cardsDictList[2]
else:
    if os.path.isfile(f"gameData/cardsCreation.json"):
        with open(f"gameData/cardsCreation.json") as json_file_cardsCreation:
            dataString_cardsCreation = json.load(json_file_cardsCreation)
            #this makes it so if u use a json beautifier that makes it not being a string anymore, it would still work
            if type(dataString_cardsCreation) == dict:
                data_cardsCreation = dataString_cardsCreation
            else:
                data_cardsCreation = json.loads(dataString_cardsCreation)
        
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

    def changeCards(name):
        nameLowered = name.lower()
        global data_cardsDict
        if 'reverse' in nameLowered:
                data_cardsDict[name]['reverse'] = True
        if 'skip' in nameLowered:
            test = nameLowered.split('skip')
            if accounts_omac.removeCharacters(test[1]).isnumeric():
                data_cardsDict[name]['skip'] = int(accounts_omac.removeCharacters(test[1]))
            else:
                data_cardsDict[name]['skip'] = 1
        if '+' in nameLowered:
            test = nameLowered.split('+')
            if accounts_omac.removeCharacters(test[1]).isnumeric():
                data_cardsDict[name]['plus'] = int(accounts_omac.removeCharacters(test[1]))
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
                data_cardsDict[name]['exchangeDecks'] = int(accounts_omac.removeCharacters(test[1]))
            else:
                data_cardsDict[name]['exchangeDecks'] = 1

    
    data_cardsList = []
    data_cardsDict = {}
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
            data_cardsList.append(f'{data_cardsCreation["colors"][x]} {data_cardsCreation["cardsPerColor"][y]}')

    for i in range(len(data_cardsCreation['special'])):
        data_cardsDict[f'{data_cardsCreation["special"][i]}'] = {'color': f'{data_cardsCreation["specialBG"]}',
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
        data_cardsList.append(f'{data_cardsCreation["special"][i]}')
    colors = data_cardsCreation['colors']
    data_cardsDictList = [data_cardsDict, data_cardsList, colors]    

    json_string_cardsDictList = json.dumps(data_cardsDictList)
    with open(f"gameData/cardsDict.json", 'w') as outfile:
        json.dump(json_string_cardsDictList, outfile)


'''
playerSelectWindow = tkinter.Tk()

def changedSomething(*args):
    print('e')

playersAmountSelect_var = tkinter.IntVar()
botsAmountSelect_var = tkinter.IntVar()
spinboxPlayers = ttk.Spinbox(playerSelectWindow, from_=float("0"), to=float("inf"), textvariable=playersAmountSelect_var).grid(column=1, row=0, ipadx=20, ipady=10)
spinboxBots = ttk.Spinbox(playerSelectWindow, from_=float("0"), to=float("inf"), textvariable=botsAmountSelect_var).grid(column=1, row=1, ipadx=20, ipady=10)
playerLabelSpinbox = tkinter.Label(playerSelectWindow, text = 'amount of players:').grid(column=0, row=0, ipadx=20, ipady=10)
botLabelSpinbox = tkinter.Label(playerSelectWindow, text = 'amount of bots:').grid(column=0, row=1, ipadx=20, ipady=10)
botsAmountSelect_var.trace('w', changedSomething)
playersAmountSelect_var.trace('w', changedSomething)
playerSelectWindow.mainloop()
'''

def createPlayer(botOrHuman, playerNumber, name = 'herman'):
    global gameData
    gameData['playerDict'][f'player {playerNumber}'] = {'type': botOrHuman,
                                                'name': name,
                                                'number': playerNumber + 1,
                                                'cards': [],
                                                'effect': {},
                                                'playedCards': {},
                                                'programSettings': {'typeOfSelect': 'default', 'showColor': True, 'defaultBGwidget': '#f0f0f0', 'defaultFGwidget': 'black','defaultBGwindow': '#f0f0f0'}}
    gameData['playerList'].append(f'player {playerNumber}')

num = 0
for x in range(players):
    createPlayer('Human', num)
    num += 1
for x in range(bots):
    createPlayer('Bot', num)
    num += 1

gameData['grabCardsDeck'] = list(data_cardsList)
gameData['cardInfo'] = data_cardsDict
gameData['colors'] = colors

random.shuffle(gameData['grabCardsDeck'])

for i in range(len(gameData['playerList'])):
    for _ in range(cardsPerPlayer):
        gameData['playerDict'][gameData['playerList'][i]]['cards'].append(gameData['grabCardsDeck'][0])
        gameData['grabCardsDeck'].pop(0)

gameData['playedCardsDeck'].append(gameData['grabCardsDeck'][0])
gameData['playerHistory'].append('NONE')
gameData['grabCardsDeck'].pop(0)

print(gameData['playerDict'])




print(gameData['playerDict'][gameData['playerList'][gameData['active']]])


turnWindow = tkinter.Tk()


defaultBG = gameData['playerDict'][gameData['playerList'][x]]['programSettings']['defaultBGwidget']
defaultFG = gameData['playerDict'][gameData['playerList'][x]]['programSettings']['defaultFGwidget']
defaultBGwindow = gameData['playerDict'][gameData['playerList'][x]]['programSettings']['defaultBGwindow']

turnWindow.configure(bg=defaultBGwindow)

nameList = list()
for x in range(len(gameData['playerList'])):
    nameList.append(f"{gameData['playerDict'][gameData['playerList'][x]]['number']}.{gameData['playerDict'][gameData['playerList'][x]]['name']}")

nameLabel = tkinter.Label(turnWindow, text =f"Player: {gameData['playerDict'][gameData['playerList'][gameData['active']]]['number']}.{gameData['playerDict'][gameData['playerList'][gameData['active']]]['name']}",borderwidth=2, relief="groove", fg = defaultFG, bg =defaultBG)
nameLabel.grid(column=0, row=0, ipadx=20, ipady=10, sticky="EW", columnspan= 2)

tkinter.Label(turnWindow,text='PlayerOrder:',bg = defaultBGwindow, fg =defaultFG).grid(column=2, row=0, ipadx=20, ipady=10, sticky="EW")
tkinter.Label(turnWindow,text='Last Played Card:', bg = defaultBGwindow, fg =defaultFG).grid(column=0, row=1, ipadx=20, ipady=10, sticky="EW")
tkinter.Label(turnWindow, text='By:', bg =defaultBGwindow, fg=defaultFG).grid(column=2, row=1, ipadx=20, ipady=10, sticky="EW")
tkinter.Label(turnWindow, bg = defaultBGwindow).grid(column=0, row=2, ipadx=20, ipady=10, sticky="EW",columnspan= 4)


lastPlayed = tkinter.Label(turnWindow, text = f"{gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]}",borderwidth=2, relief="groove")
if gameData['playerDict'][gameData['playerList'][x]]['programSettings']['showColor'] == True:
    lastPlayed.configure(bg = gameData['cardInfo'][gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]]['displayBGColor'], fg =gameData['cardInfo'][gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]]['displayFGColor'])
else:
    lastPlayed.configure(bg = gameData['playerDict'][gameData['playerList'][x]]['programSettings']['defaultBGwidget'], fg =gameData['playerDict'][gameData['playerList'][x]]['programSettings']['defaultFGwidget'])
lastPlayed.grid(column=1, row=1, ipadx=20, ipady=10, sticky="EW")


playerPlayed = tkinter.Label(turnWindow,borderwidth=2, relief="groove", fg = defaultFG, bg =defaultBG)
playerPlayed.grid(column=3, row=1, ipadx=20, ipady=10, sticky="EW")
if gameData['playerHistory'][len(gameData['playerHistory'])-1] == "NONE":
    playerPlayed.configure(text = 'Nobody, it\'s the first card')
else:
    playerPlayed.configure(text =f"{gameData['playerDict'][gameData['playerHistory'][len(gameData['playerHistory'])-1]]['number']}.{gameData['playerDict'][gameData['playerHistory'][len(gameData['playerHistory'])-1]]['name']}")


playerOrderCombobox = ttk.Combobox(turnWindow,state='readonly',values = nameList)
playerOrderCombobox.grid(column=3, row=0, ipadx=20, ipady=10, sticky="EW")

tkinter.Label(turnWindow,text = 'select card to play:', bg =defaultBGwindow, fg= defaultFG).grid(column=0, row=3, ipadx=20, ipady=10, sticky="EW")

card_var = tkinter.StringVar()

if gameData['playerDict'][gameData['playerList'][x]]['programSettings']['typeOfSelect'] == 'default':
    cardSelect = ttk.Combobox(turnWindow)
else:
    cardSelect = ttk.Spinbox(turnWindow)
cardSelect.configure(state='readonly', textvariable=card_var, values =gameData['playerDict'][gameData['playerList'][x]]['cards'])
cardSelect.grid(column=1, row=3, ipadx=20, ipady=10, sticky="EW",columnspan= 2)

dataCard= ttk.Combobox(turnWindow, state='readonly')
dataCard.grid(column=3, row=3, ipadx=20, ipady=10, sticky="EW")
def cardData(*args):
    listOfThings = list(gameData['cardInfo'][card_var.get()].keys())
    listOfData = list()
    for x in range(len(listOfThings)):
        listOfData.append(f"{listOfThings[x]}: {gameData['cardInfo'][card_var.get()][listOfThings[x]]}")
    dataCard.configure(values =listOfData)


card_var.trace('w', cardData)
def settings():
    
    SettingsWindow = tkinter.Tk()
    ttk.Label(SettingsWindow,text="Settings",font=("Comic_Sans",10)).grid(column = 0,row = 1, ipadx=20, ipady=10, sticky="EW")
    ttk.Label(SettingsWindow,text="show card color",font=("Comic_Sans",10)).grid(column = 1,row = 1, ipadx=20, ipady=10, sticky="EW")
    ttk.Checkbutton(SettingsWindow).grid(column = 2,row = 1, ipadx=20, ipady=10, sticky="EW")
    SettingsWindow.mainloop()


SettingsButton = tkinter.Button(text="Settings",command=settings).grid(column = 7,row = 7, ipadx=20, ipady=10, sticky="EW")





turnWindow.mainloop()

