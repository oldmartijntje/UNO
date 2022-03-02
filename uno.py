from logging.config import dictConfig
import os
import json

#without it there wouldn't be a folder to put the jsons in
if os.path.isdir('gameData/'):
    pass
else:   
    os.mkdir('gameData/')

#without this it can't load a json nor create a new json with the cards
if os.path.isfile(f"gameData/cardsDict.json"):
    with open(f"gameData/cardsDict.json") as json_file_cardsDict:
        dataString_cardsDict = json.load(json_file_cardsDict)
        #this makes it so if u use a json beautifier that makes it not being a string anymore, it would still work
        if type(dataString_cardsDict) == dict:
            data_cardsDict = dataString_cardsDict
        else:
            data_cardsDict = json.loads(dataString_cardsDict)
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
                            'cardsPerColor': [0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,'+2', '+2', 'Skip', 'Skip', 'Reverse', 'Reverse'],
                            'special': ['+4', 'Wild']}

        json_string_cardsCreation = json.dumps(data_cardsCreation)
        with open(f"gameData/cardsCreation.json", 'w') as outfile:
            json.dump(json_string_cardsCreation, outfile)
    print(data_cardsCreation)
        