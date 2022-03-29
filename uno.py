import os
import json
import accounts_omac
import tkinter
from tkinter import ttk
import random
from tkinter.messagebox import showwarning

appIDorName = 'UNO2byMarjinIDK'

bots = 4
players = 2
cardsPerPlayer = 7
whenReshuffle = 4
chosenWildColor = 'Red'

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

def grabCard(activePlayer):
    global gameData
    if len(gameData['grabCardsDeck']) <= whenReshuffle:
        for _ in range(len(gameData['playedCardsDeck'])-1):
            gameData['grabCardsDeck'].append(gameData['playedCardsDeck'][0])
            gameData['playedCardsDeck'].pop(0)
    gameData['playerDict'][gameData['playerList'][activePlayer]]['cards'].append(gameData['grabCardsDeck'][0])
    gameData['grabCardsDeck'].pop(0)


#give players cards
def giveDeckOfCards():
    global gameData
    for i in range(len(gameData['playerList'])):
        for _ in range(cardsPerPlayer):
            grabCard(i)
            
giveDeckOfCards()


#get the first card
gameData['playedCardsDeck'].append(gameData['grabCardsDeck'][0])
gameData['playerHistory'].append('NONE')
gameData['grabCardsDeck'].pop(0)

#print data for some reason
#print(gameData['playerDict'])
#print(gameData['playerDict'][gameData['playerList'][gameData['active']]])


######################## Turns of players / bots ########################


#to not get those nasty index out of range errors, you try to get item 20 out of 19 items, this will return you item 0
def noIndexError(number, maxNumber, minNumber = 0):
    '''to not get those nasty index out of range errors, you try to get item 20 out of 19 items, this will return you item 0'''
    while number > maxNumber or number < minNumber:
        if number > maxNumber:
            number -= maxNumber+1
        elif number < minNumber:
            number += maxNumber + 1
    return number


#play a card
def playCard(card):
    global gameData
    global wildWindow

    if gameData['playerDict'][gameData['playerList'][gameData['active']]]['type'] == 'Human':
        turnWindow.destroy()
    gameData['playerHistory'].append(gameData['playerList'][gameData['active']])
    if gameData['cardInfo'][card]['suckDragon']:
        for x in range(len(gameData['playerList'])):
            for _ in range(len(gameData['playerDict'][gameData['playerList'][x]]['cards'])):
                gameData['playerDict'][gameData['playerList'][x]]['cards'].pop(0)
        giveDeckOfCards()
    else:
        gameData['playerDict'][gameData['playerList'][gameData['active']]]['cards'].remove(card)    
        gameData['playedCardsDeck'].append(card)

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

    if gameData['cardInfo'][card]['wild']:
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
        wildWindow.mainloop()
    if gameData['cardInfo'][card]['plus'] > 0:
        gameData['plusCardActive'] += gameData['cardInfo'][card]['plus']


#is it playable tho??
def checkIfCardPlayable(selected,mode = True):
    if selected != '':
        if gameData['cardInfo'][selected]['alwaysPlayable'] == True:
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
        else:
            if mode == False:
                return False
    else:
        showwarning(title='Play',message ='Uno\nYou might want to pick a card')

def nextPlayer(card):
    direction = str(gameData['direction'])
    if gameData['cardInfo'][card]['shuffleOrder'] or gameData['cardInfo'][card]['dualWielding']:
        return gameData['active']
    else:
        if gameData['cardInfo'][card]['reverse']:
            direction = str(int(direction) * -1)
        if gameData['cardInfo'][card]['skip'] > 0:
            if int(direction) > 0:
                direction = str(int(direction)+gameData['cardInfo'][card]['skip'])
            else:
                direction = str(int(direction)-gameData['cardInfo'][card]['skip'])
        return noIndexError(gameData['active'] + int(direction), len(gameData['playerList'])-1)


#show what the card does
def generateCardTip(card):
    text = f"Card color: {gameData['cardInfo'][card]['color']}\nCard type: {gameData['cardInfo'][card]['type']}\n"
    if checkIfCardPlayable(card,False):
        text += 'This card is playable at this moment'
    else:
        text += 'This card is not playable at this moment'
    text += '\nIf you play this card right now, the following would happen:'
    if nextPlayer(card) != gameData['active']:
        nextPlayerReturn = gameData["playerList"][nextPlayer(card)]
        text += f'\nThe next player would be {gameData["playerDict"][nextPlayerReturn]["number"]}.{gameData["playerDict"][nextPlayerReturn]["name"]}'
    if gameData['cardInfo'][card]['suckDragon']:
        text += f'\nEveryones cards would be taken and be given {cardsPerPlayer} new cards.'
    if gameData['cardInfo'][card]['shuffleOrder']:
        text += f'\nThe order of player turns would be shuffled randomly.'
    if gameData['cardInfo'][card]['dualWielding']:
        text += f'\nAfter this card it\'s your turn again'
    if gameData['cardInfo'][card]['wild']:
        text += f'\nYou would be able to choose the color of the next card.'
    if gameData['cardInfo'][card]['reverse']and gameData['cardInfo'][card]['shuffleOrder'] == False:
        text += f'\nThe order of players is reversed'
    if gameData['cardInfo'][card]['plus'] > 0:
        text += f'\nThe next player will have to draw {gameData["cardInfo"][card]["plus"]} cards from the pile,\nunless they have a card with the simular function of making people draw cards.'
    if gameData['cardInfo'][card]['exchangeDecks'] > 0:
        text += f'\nYou would obtain the cards of the {gameData["cardInfo"][card]["exchangeDecks"]}th opponent, heading the opposite way of the playing direction'
    


    return text




######################## player turn ########################

def playerTurn():
    global turnWindow
    global gameData
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
    nameAndCardList = list()
    nameList = list()
    for x in range(len(gameData['playerList'])):
        if int(gameData['direction']) < 0 or gameData['direction'] == '-0':
            nameList.append(f"{gameData['playerDict'][gameData['playerList'][noIndexError(activePlayer -(1+x), len(gameData['playerList'])-1)]]['number']}.{gameData['playerDict'][gameData['playerList'][noIndexError(activePlayer -(1+x), len(gameData['playerList'])-1)]]['name']}")
            nameAndCardList.append(f"{nameList[x]} ({len(gameData['playerDict'][gameData['playerList'][noIndexError(activePlayer -(1+x), len(gameData['playerList'])-1)]]['cards'])} cards) ")
        else:
            nameList.append(f"{gameData['playerDict'][gameData['playerList'][noIndexError(activePlayer + x +1, len(gameData['playerList'])-1)]]['number']}.{gameData['playerDict'][gameData['playerList'][noIndexError(activePlayer + x + 1, len(gameData['playerList'])-1)]]['name']}")
            nameAndCardList.append(f"{nameList[x]} ({len(gameData['playerDict'][gameData['playerList'][noIndexError(activePlayer + x +1, len(gameData['playerList'])-1)]]['cards'])} cards) ")



    #labels
    nameLabel = tkinter.Label(turnWindow, text =f"Current player: {gameData['playerDict'][gameData['playerList'][activePlayer]]['number']}.{gameData['playerDict'][gameData['playerList'][gameData['active']]]['name']}",borderwidth=2, relief="groove", fg = defaultFG, bg =defaultBG)
    nameLabel.grid(column=0, row=0, ipadx=20, ipady=10, sticky="EW", columnspan= 2)
    tkinter.Label(turnWindow,text='PlayerOrder:',bg = defaultBGwindow, fg =defaultFG).grid(column=2, row=0, ipadx=20, ipady=10, sticky="EW")
    tkinter.Label(turnWindow,text='Last played card:', bg = defaultBGwindow, fg =defaultFG).grid(column=0, row=1, ipadx=20, ipady=10, sticky="EW")
    tkinter.Label(turnWindow, text='By:', bg =defaultBGwindow, fg=defaultFG).grid(column=2, row=1, ipadx=20, ipady=10, sticky="EW")
    tkinter.Label(turnWindow, bg = defaultBGwindow).grid(column=0, row=2, ipadx=20, ipady=10, sticky="EW",columnspan= 4)
    tkinter.Label(turnWindow,text = 'Select card to play:', bg =defaultBGwindow, fg= defaultFG).grid(column=0, row=3, ipadx=20, ipady=10, sticky="EW")  

    #what happends when you touch the label with the last played card
    def enter(*args):
        global infoWindow
        try:
            infoWindow = tkinter.Tk()
            infoWindow.geometry(f'+{infoWindow.winfo_pointerx()-infoWindow.winfo_rootx()+2}+{infoWindow.winfo_pointery()-infoWindow.winfo_rooty()+2}')
            infoLabel = ttk.Label(infoWindow)
            infoLabel.configure(text=generateCardTip(gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]))
            infoLabel.pack(ipadx=20, ipady=10)
        except Exception as e:
            showwarning(title='Play',message =f'Uno\nCatastrophic failure')

    #close the card info
    def leave(*args):
        try:
            infoWindow.destroy()
        except:
            showwarning(title='Play',message ='Uno\nCatastrophic failure')

    #the label of the last played card
    lastPlayed = tkinter.Label(turnWindow, text = f"{gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]}",borderwidth=2, relief="groove")
    if gameData['playerDict'][gameData['playerList'][x]]['programSettings']['showColor']:
        lastPlayed.configure(bg = gameData['cardInfo'][gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]]['displayBGColor'], fg =gameData['cardInfo'][gameData['playedCardsDeck'][len(gameData['playedCardsDeck'])-1]]['displayFGColor'])
    else:
        lastPlayed.configure(bg = gameData['playerDict'][gameData['playerList'][activePlayer]]['programSettings']['defaultBGwidget'], fg =gameData['playerDict'][gameData['playerList'][x]]['programSettings']['defaultFGwidget'])
    lastPlayed.grid(column=1, row=1, ipadx=20, ipady=10, sticky="EW")
    lastPlayed.bind('<Enter>',enter)
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
    if gameData['playerDict'][gameData['playerList'][x]]['programSettings']['typeOfSelect'] == 'default':
        cardSelect = ttk.Combobox(turnWindow)
    else:
        cardSelect = ttk.Spinbox(turnWindow)
    cardSelect.configure(state='readonly', textvariable=card_var, values =gameData['playerDict'][gameData['playerList'][activePlayer]]['cards'])
    cardSelect.grid(column=1, row=3, ipadx=20, ipady=10, sticky="EW",columnspan= 2)

    #info about the selected card combobox
    dataCard= ttk.Combobox(turnWindow, state='readonly')
    dataCard.grid(column=3, row=3, ipadx=20, ipady=10, sticky="EW")
    #if you select a card, the info combobox will change
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
        tkinter.Checkbutton(SettingsWindow).grid(column = 2,row = 1, ipadx=20, ipady=10, sticky="EW")
        SettingsWindow.mainloop()


    SettingsButton = ttk.Button(text="Settings",command=settings).grid(column = 3,row = 4, ipadx=20, ipady=10, sticky="EW")

    playButton = ttk.Button(turnWindow, command =lambda: checkIfCardPlayable(card_var.get()), text='Play Selected Card').grid(column = 0,row = 4, ipadx=20, ipady=10, sticky="EW",columnspan= 3)



    turnWindow.mainloop()
playerTurn()
