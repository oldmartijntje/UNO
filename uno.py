import os
import json
import accounts_omac
import tkinter

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
                            'secialBG': 'black', 
                            'specialColor': 'Black'}

        json_string_cardsCreation = json.dumps(data_cardsCreation)
        with open(f"gameData/cardsCreation.json", 'w') as outfile:
            json.dump(json_string_cardsCreation, outfile)

    def changeCards(name):
        global data_cardsDict
        if 'Reverse' in name or 'reverse' in name:
                data_cardsDict[name]['reverse'] = 1
        if 'Skip' in name or 'skip' in name:
            test = name.split('Skip')
            if accounts_omac.removeCharacters(test[1]).isnumeric():
                data_cardsDict[name]['skip'] = int(accounts_omac.removeCharacters(test[1]))
            else:
                data_cardsDict[name]['skip'] = 1
        if '+' in name:
            test = name.split('+')
            if accounts_omac.removeCharacters(test[1]).isnumeric():
                data_cardsDict[name]['plus'] = int(accounts_omac.removeCharacters(test[1]))
            else:
                data_cardsDict[name]['plus'] = 1
        if 'Wild' in name or 'wild' in name:
                data_cardsDict[name]['wild'] = True
    
    data_cardsList = []
    data_cardsDict = {}
    for x in range(len(data_cardsCreation['colors'])):
        for y in range(len(data_cardsCreation['cardsPerColor'])):
            data_cardsDict[f'{data_cardsCreation["colors"][x]} {data_cardsCreation["cardsPerColor"][y]}'] = {'color': f'{data_cardsCreation["colors"][x]}',
                                                                                                            'type': f'{data_cardsCreation["cardsPerColor"][y]}',
                                                                                                            'alwaysPlayable': False,
                                                                                                            'plus': 0,
                                                                                                            'reverse': 0,
                                                                                                            'skip': 0,
                                                                                                            'wild': False,
                                                                                                            'dualWielding' : False,
                                                                                                            'displayBGColor': f'{data_cardsCreation["displayColorsBG"][x]}',
                                                                                                            'displayFGColor': f'{data_cardsCreation["displayColorsFG"][x]}'}
                                                                                             
            changeCards(f'{data_cardsCreation["colors"][x]} {data_cardsCreation["cardsPerColor"][y]}')
            data_cardsList.append(f'{data_cardsCreation["colors"][x]} {data_cardsCreation["cardsPerColor"][y]}')

    for i in range(len(data_cardsCreation['special'])):
        data_cardsDict[f'{data_cardsCreation["special"][i]}'] = {'color': f'{data_cardsCreation["special"][i]}',
                                                                'type': f'{data_cardsCreation["special"][i]}',
                                                                'alwaysPlayable': True,
                                                                'plus': 0,
                                                                'reverse': 0,
                                                                'skip': 0,
                                                                'wild': False,
                                                                'dualWielding' : False,
                                                                'displayBGColor': f'{data_cardsCreation["secialBG"][x]}',
                                                                'displayFGColor': f'{data_cardsCreation["specialFG"][x]}'}
        changeCards(f'{data_cardsCreation["special"][i]}')
        data_cardsList.append(f'{data_cardsCreation["special"][i]}')
    data_cardsDictList = [data_cardsDict, data_cardsList]    

    json_string_cardsDictList = json.dumps(data_cardsDictList)
    with open(f"gameData/cardsDict.json", 'w') as outfile:
        json.dump(json_string_cardsDictList, outfile)

window = tkinter.Tk()

def changedSomething(*args):
    print('e')
playersAmountSelect_var = tkinter.IntVar()
botsAmountSelect_var = tkinter.IntVar()

spinboxPlayers = tkinter.Spinbox(window, from_=float("0"), to=float("inf"), textvariable=playersAmountSelect_var).grid(column=1, row=0, ipadx=20, ipady=10)
spinboxBots = tkinter.Spinbox(window, from_=float("0"), to=float("inf"), textvariable=botsAmountSelect_var).grid(column=1, row=1, ipadx=20, ipady=10)
playerLabelSpinbox = tkinter.Label(window, text = 'amount of players:').grid(column=0, row=0, ipadx=20, ipady=10)
botLabelSpinbox = tkinter.Label(window, text = 'amount of bots:').grid(column=0, row=1, ipadx=20, ipady=10)
botsAmountSelect_var.trace('w', changedSomething)
playersAmountSelect_var.trace('w', changedSomething)
window.mainloop()