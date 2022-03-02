import os
import pathlib
import random
import time
import ast
import pickle
from datetime import datetime

pluginEquipped = False
try:
    from examplePlugin import *
    pluginEquipped = True
except:
    print("no plugins (plugin.py) found")

historyOfCards = list()
historyPlayersThatPlayedACard = list()

#settings: seed0, difficulty1, normal cards2, special cards3, player amount4, starting cards5

class player(): #player and computer
    def __init__(self, playerOrComputer, userName, cardsDeck, statusEffects, memory, playerNumber, difficulty = 'Exercise') -> None:
        amountBullied = 0
        takenFromPile = 0
        cardsGrabbed = 0
        self.name = userName
        self.cards = cardsDeck
        self.effect = statusEffects
        self.memory = memory
        self.type = playerOrComputer
        self.number = playerNumber
        self.bullied = amountBullied
        self.grabbedCard = cardsGrabbed
        self.cardsFromPile = takenFromPile
        self.difficulty = difficulty

def saveAnState(player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedCards, turn):
    ownPath = pathlib.Path().resolve()
    allDataTogether = [player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedCards, turn]
    allListsInOne = [cardTypes,cardTypesNames,cardColors,yellowGreenColorblindCardColorsNames,blueRedColorblindCardColorsNames,colorblindCardColorsNames,cardColorsNames,specials,specialsNames]
    old_state = random.getstate()
    statistics = [mostPlayedColor, mostPlusCards, mostSkipCards, mostReverseCards, mostTimesGrabbedFromPile, mostTimesBullied, mostTimesGrabbedACardInsteadOfPlaying, orderOfWinners, wins, playerListEndOfGame, historyPlayersThatPlayedACard, historyOfCards]
    allInOne = [allDataTogether, allListsInOne, old_state, statistics]
    name = input("what do you want to call the save state (it will not overwrite existing ones)")
    newName = name
    looped = 0
    while os.path.isfile(f"{newName}.UNOSAV"):
        looped += 1
        newName = name + f"({looped})"
    print(f"it will now save to {ownPath}/my_saves/{newName}.UNOSAV")
    try:
        pickle.dump( allInOne, open( f"{ownPath}/my_saves/{newName}.UNOSAV", "wb" ) )
        print("it correctly saved")
    except Exception as e:
        print(e)
        print("it failed")

def loadAnState():
    ownPath = pathlib.Path().resolve()
    name = input("what save state do you want to open? (only say the name, we put .UNOSAV behind it ourselves)")
    if os.path.isfile(f"{ownPath}/my_saves/{name}.UNOSAV"):
        print("okay, please wait")
        returnedValues = pickle.load( open( f"{ownPath}/my_saves/{name}.UNOSAV", "rb" ))
        return returnedValues
    else:
        print("that is not a file, please try again")
        return False

def loadedStateToData(loadedData):
    try:
        allDataTogether, allListsInOne, old_state, statistics = loadedData
        player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedCards, turn = allDataTogether
        cardTypes,cardTypesNames,cardColors,yellowGreenColorblindCardColorsNames,blueRedColorblindCardColorsNames,colorblindCardColorsNames,cardColorsNames,specials,specialsNames = allListsInOne
        mostPlayedColor, mostPlusCards, mostSkipCards, mostReverseCards, mostTimesGrabbedFromPile, mostTimesBullied, mostTimesGrabbedACardInsteadOfPlaying, orderOfWinners, wins, playerListEndOfGame, historyPlayersThatPlayedACard, historyOfCards = statistics
        extra = [cardTypes,cardTypesNames,cardColors,yellowGreenColorblindCardColorsNames,blueRedColorblindCardColorsNames,colorblindCardColorsNames,cardColorsNames,specials,specialsNames,mostPlayedColor, mostPlusCards, mostSkipCards, mostReverseCards, mostTimesGrabbedFromPile, mostTimesBullied, mostTimesGrabbedACardInsteadOfPlaying, orderOfWinners, wins, playerListEndOfGame, historyPlayersThatPlayedACard, historyOfCards]
        random.seed(settings[0])
        random.setstate(old_state)
        if type(lastPlayedCards) != list:
            lastPlayedCardss = list()
            lastPlayedCardss.append(lastPlayedCards)
            return player, cards, lastPlayedCardss, playerList, settings, playingDirection, activePlayer, win, playedCards, turn, extra
    except Exception as e:
        print(e)
        print(f"seed: {setting[0]}")
        print(f"maybe loaded seed: {settings[0]}")
    return player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedCards, turn, extra

def saveStates(player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedCards, turn, extra = []):
    print("\nWelcome to the Savestate menu, here you can pause your game and continue it next time")
    print("you can create infinite save states\nyou can load save states, even if they have other settings, the settings will automatically change to how it was saved")
    if not os.path.exists('my_saves'):
        os.makedirs('my_saves')
    loop3 = True
    while loop3 == True:
        try:
            optionChosen = int(input("what do you want to do?\n1.save\n2.load\n3.go back\n>>>"))
        except Exception as e:
            print(e)
        if optionChosen > 0 and optionChosen < 4:
            if optionChosen == 3:
                return player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedCards, turn
            elif optionChosen == 1:
                saveAnState(player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedCards, turn)
                loop3 = False
            elif optionChosen == 2:
                loaded = loadAnState()
                if loaded != False:
                    player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedCards, turn, extra = loadedStateToData(loaded)
                    loop3 = False
        else:
            print("that is not an option")
        
    return player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedCards, turn, extra

def pluginLoad(cardTypes, cardTypesNames, cardColors, yellowGreenColorblindCardColorsNames, blueRedColorblindCardColorsNames, colorblindCardColorsNames, cardColorsNames, specials, specialsNames):
    ownPath = pathlib.Path().resolve()
    if os.path.isfile(f"{ownPath}/plugin.ini"):
        pluginTXT = open(f"{ownPath}/plugin.ini", "r")
        reading = pluginTXT.read().split('\n')
        readingIsList = list()
        for x in range(len(reading)):
            if reading[x][0] != "#":
                try:
                    readingIsList.append(ast.literal_eval(reading[x]))
                except:
                    readingIsList.append(reading[x].strip('][').split(', '))
        input(readingIsList)
        cardTypes, cardTypesNames, cardColors, yellowGreenColorblindCardColorsNames, blueRedColorblindCardColorsNames, colorblindCardColorsNames, cardColorsNames, specials, specialsNames = readingIsList
    return cardTypes, cardTypesNames, cardColors, yellowGreenColorblindCardColorsNames, blueRedColorblindCardColorsNames, colorblindCardColorsNames, cardColorsNames, specials, specialsNames

def pleaseFixTheConfigFile(exception = ""):#tells u there is a problem with your config
    input(f"There is a problem with \"{ownPath}/Config.ini\" Go fix it, or Delete it\nPress Enter to close")
    print(exception)
    exit()

#get the programs path
ownPath = pathlib.Path().resolve()

def stringToSeed(seedString): #turns everything into ther ASCII value
    seedList = []
    for x in seedString:
        seedList.append(ord(x))#change every character into its ASCII value
    seedString = ''.join([str(elem) for elem in seedList])#add list together into string
    seed = int(seedString)
    return seed

def cardIdToName(ID, effect = 0):#input the card id: 1.6 and turns it into blue 6
    card = ""
    splitted = ID.split(".")
    splitted[0] = int(splitted[0])
    splitted[1] = int(splitted[1])
    try:
        splitted[2] = int(splitted[2])

        #a wild card has a chosen color
        if effect == 1:
            card = f'{specialsNames[splitted[1]]} with chosen color {yellowGreenColorblindCardColorsNames[splitted[2]]}'
        elif effect == 2:
            card = f'{specialsNames[splitted[1]]} with chosen color {blueRedColorblindCardColorsNames[splitted[2]]}'
        elif effect == 3:
            card = f'{specialsNames[splitted[1]]} with chosen color {colorblindCardColorsNames[splitted[2]]}'
        else:
            card = f'{specialsNames[splitted[1]]} with chosen color {cardColorsNames[splitted[2]]}'
    except:
        if splitted[0] == 4:
            card = f"{specialsNames[splitted[1]]}"
        else:
            if effect == 1:
                card = f'{yellowGreenColorblindCardColorsNames[splitted[0]]} {cardTypesNames[splitted[1]]}'
            elif effect == 2:
                card = f'{blueRedColorblindCardColorsNames[splitted[0]]} {cardTypesNames[splitted[1]]}'
            elif effect == 3:
                card = f'{colorblindCardColorsNames[splitted[0]]} {cardTypesNames[splitted[1]]}'
            else:
                card = f'{cardColorsNames[splitted[0]]} {cardTypesNames[splitted[1]]}'
    return card

def lookAtCards(listOfPlayers):
    for x in range(len(listOfPlayers)):
        for y in range(len(listOfPlayers[x].cards)):
            print(f"{listOfPlayers[x].number}, {listOfPlayers[x].name} has {cardIdToName(listOfPlayers[x].cards[y])}")

def clear_console(): # clear the console
    try:
        os.system('cls')
    except:
        try:
            os.system('clear')
        except:
            e = 0

def takeCardFromDeck(amount, cardPile, lastPlayedCard, player, playedCards, mode = 0):#grab the amount of cards and add it to your deck
    gift = list()
    if mode == 0 : print(f"you drew {amount} cards:")
    if mode == 1 : print(f"player {player.number + 1}, {player.name} drew {amount} cards")
    for x in range(amount):
        succes = True
        while succes == True:
            try:
                playerListEndOfGame[player.number].cardsFromPile += 1    
                if len(cardPile) > 1:
                    if cardPile[0].split('.')[1] == '0' and int(cardPile[0].split('.')[0]) == len(cardColors)-1:
                        cardPile[0] = f'{len(cardColors)-1}.0'
                    gift.append(cardPile[0])
                    if mode == 0 :print(f"you have grabbed a {cardIdToName(cardPile[0], player.effect)}")
                    cardPile.pop(0)
                    succes = False
                else:#add the played pile to the new cards
                    placeholderList = list()
                    print("shuffling cards...")
                    if len(lastPlayedCard) > 1:
                        for _ in range(1, len(lastPlayedCard)):
                            placeholderList.append(lastPlayedCard[1])
                            lastPlayedCard.pop(1)
                    for _ in range(0, len(playedCards)):
                        placeholderList.append(playedCards[0])
                        playedCards.pop(0)
                    if len(placeholderList) == 0:
                        print("there are 0 cards left on the pile to give")
                        succes = False
                        return gift, cardPile, lastPlayedCard, playedCards
                    else:
                        random.shuffle(placeholderList)
                        for x in range(len(placeholderList)):
                            cardPile.append(placeholderList[x])
                        if type(cardPile[0]) == list: cardPile = cardPile[0]
                        if cardPile[0].split('.')[1] == '0' and int(cardPile[0].split('.')[0]) == len(cardColors)-1:
                            cardPile[0] = f'{len(cardColors)-1}.0'
                        gift.append(cardPile[0])
                        if mode == 0 : print(f"you have grabbed a {cardIdToName(cardPile[0], player.effect)}")
                        cardPile.pop(0)
            except Exception as e:
                print(e)
                succes = True
                lookAtCards(playerList)
                try:
                    print(lastPlayedCard)
                except:
                    print("lastPlayedCard")
                try:
                    print( placeholderList)
                except:
                    print("placeholderList")
                try:
                    print(cardPile )
                except:
                    print('cardPile')
                input()
    return gift, cardPile, lastPlayedCard, playedCards

def checkForUno(playerList, player):
    num = 0
    for x in range(len(playerList)):
        if player.number != playerList[x].number and len(playerList[x].cards) == 1:
            print(f"player {playerList[x].number + 1}, {playerList[x].name} has 1 card left")
            num += 1
    if num > 0:
        print("input -1 to see stats like these of other people, and other tools")
    return

def createConfig(ownPath):#creates the config file
    #open settings if .settings.txt exists
    if os.path.isfile(f"{ownPath}/Config.ini"):
        settings = open(f"{ownPath}/Config.ini", "r+")
    #rename settings.txt to .settings.txt if settings.txt exists
    elif os.path.isfile(f"{ownPath}/Config.txt"):
        os.rename(f"{ownPath}/Config.txt", f"{ownPath}/Config.ini")
        settings = open(f"{ownPath}/Config.ini", "r+")
    #create .settings.txt
    else:
        settings = open(f"{ownPath}/Config.ini", "x")
        settings.write("#if you leave empty lines, or with other characters(unless the line starts with #, then it is okay), the program will choose by itself"+
    "\n#\n#\n#BE AWARE THAT \"True\" AND \"False\" NEED TO HAVE THE FIRST LETTER CAPITALIZED\n#\n#"+
    "\n#if you want to use a seed, put it here, else, make it False\nFalse"+
    "\n#choose a gamemode, these are the gamemodes:\n#Easy\n#Normal\n#Impossible\n#Exercise\nExercise"+
    "\n#choose the amount of normal cards (how many times a set of 13 cards x color) default is 1\n1"+
    "\n#choose the amount of special cards (4 by default)\n4"+
    "\n#choose the amount of Players 2-10 (per set of cards (combined with computer players)) (1 by default)\n1"+
    "\n#choose the amount of Computer players 2-10 (per set of cards (combined with players)) (3 by default)\n3"+
    "\n#do you want to use playernames? (if not, it will randomly select one) if yes, type True, if not type False\nTrue"+
    "\n#choose the amount of starting cards (might break if no cards are left) (7 by default)\n7"+
    "\n#do you want to use status effects? if yes, type True, if not type False\nTrue")
    settings.close()

def readConfig():#reads the config file lines and ignores # lines
    #check the settings
    settings = open(f"{ownPath}/Config.ini", "r")
    settingsNotSplitted = settings.read()
    settings.close()
    #split at every enter
    settingsSplitted = settingsNotSplitted.split("\n")
    #create list with things that aren't comments
    settingsWithoutComments = list()
    #for all lines, if the line starts with a # ignore it, else, add it to the list with settings
    for x in range(len(settingsSplitted)):
        try:
            if settingsSplitted[x][0] != "#":
                settingsWithoutComments.append(settingsSplitted[x])
        except Exception as e:
            pleaseFixTheConfigFile(e)
    return settingsWithoutComments

def rawSettingsToSettings(rawSettings): #turns settings into settings the program can use
    try:
        gamemodeList = ["Easy", "Normal", "Impossible", "Exercise"]
        settings = [False, "Exercise"]
        if rawSettings[0] == "False":#check if seed in entered
            settings[0] = stringToSeed(str(datetime.now()))
        else:
            try:
                settings[0] = int(rawSettings[0])
            except:
                settings[0] = stringToSeed(rawSettings[0])
        if rawSettings[1] not in gamemodeList:#check difficulty
            settings[1] = "Exercise"
        else:
            match rawSettings[1]: #select chosen difficulty
                case 'Easy':
                    settings[1] = "Easy"
                case 'Normal':
                    settings[1] = "Normal"
                case 'Impossible':        
                    settings[1] = "Impossible"
                case 'Exercise':        
                    settings[1] = "Exercise"
        if rawSettings[2] != "":#check amount of normal cards
            settings.append(int(rawSettings[2]))
        else:
            pleaseFixTheConfigFile()
        if rawSettings[3] != "":#check amount of special cards
            settings.append(int(rawSettings[3]))
        else:
            pleaseFixTheConfigFile()
        
        settings.append(int(rawSettings[4])) #set amount of players
        if settings[4] > 10*settings[2] or settings[4] < 0:
            settings[4] = 1

        settings.append(int(rawSettings[5])) #set amount of computer players
        if settings[5] + settings[4] > 10*settings[2] or settings[4] + settings[5] < 2:
            settings[5] = 3

        settings.append(rawSettings[6])
        if rawSettings[6] == "False":#check if they want names
            settings[6] = False
        else:
            settings[6] = True

        settings.append(int(rawSettings[7])) #set amount of starting cards

        settings.append(rawSettings[8])
        if rawSettings[8] == "False":#check if they want colorblindness
            settings[8] = False
        else:
            settings[8] = True

        return settings
    except Exception as e:
        print(settings)
        pleaseFixTheConfigFile(e)

def checkForPlus(card):
        test = False
        if int(card.split(".")[0]) == len(cardColors)-1 and card.split(".")[1] == '1':#check if it is a +4 card
            test = True
        elif card.split(".")[1] == '11':#check if it is a +2 card
            test = True
        return test

def chooseCard(player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playerdCard, turn, extra = []):
    lastPlayedCardName = cardIdToName(lastPlayedCards[len(lastPlayedCards)-1], player.effect)
    if turn != 1:
        print(f"The last player {historyPlayersThatPlayedACard[len(historyPlayersThatPlayedACard)-1]} played {lastPlayedCardName}")
    else:
        print(f"The starting card is {lastPlayedCardName}")
    cardsInDeckString = ""
    for x in range(len(player.cards)):#show all your cards
        cardsInDeckString += "| " + f"{x+1}."+cardIdToName(player.cards[x], player.effect)+" | "
    print(f"what card do you want to play? (say 0 to grab the cards from the pile, say -1 to see other options)\n{cardsInDeckString}")
    loop = True
    while loop == True:
        try:
            numberCard = input()
            numberCard = int(numberCard)
            if numberCard <= len(player.cards):#if he chose an existing card
                if numberCard == 0:
                    if (lastPlayedCards[len(lastPlayedCards)-1].split(".")[0] == "4" and lastPlayedCards[len(lastPlayedCards)-1].split(".")[1] == "1") or (lastPlayedCards[len(lastPlayedCards)-1].split(".")[1] == "11" and lastPlayedCards[len(lastPlayedCards)-1].split(".")[0] != "4"):
                        win.append("+")
                    cardsForPlayer, cards, lastPlayedCards, playerdCard = (takeCardFromDeck(1, cards, lastPlayedCards, player, playerdCard))#grab a card
                    for x in range(len(cardsForPlayer)):
                        player.cards.append(cardsForPlayer[x])
                    loop = False
                    historyOfCards.append("nothing, he grabbed a card")
                    playerListEndOfGame[player.number].grabbedCard += 1
                elif numberCard == -1:
                    print("settings:\n-2 to see how many cards everyone has\n-3 to see the history\n-4 to show your options\n-5 to show the seed\n-6 to disconnect this user\n-7 savestates\n-8 make user into a bot\n-9 change bot into user")
                elif numberCard == -2:
                    for x in range(len(playerList)):
                        print(f"player {playerList[x].number+1}, {playerList[x].name} has {len(playerList[x].cards)} cards")#show amount of cards everyone has
                elif numberCard == -3:
                    for x in range(len(historyOfCards)):
                        if historyOfCards[x] != "nothing, he grabbed a card" and historyOfCards[x] != "nothing, he disconnected":
                            print(f"{historyPlayersThatPlayedACard[x]} played {cardIdToName(historyOfCards[x], player.effect)}")
                        else:
                            print(f"{historyPlayersThatPlayedACard[x]} played {historyOfCards[x]}")
                elif numberCard == -4:
                    if turn != 1:
                        print(f"The last player {historyPlayersThatPlayedACard[len(historyPlayersThatPlayedACard)-1]} played {lastPlayedCardName}")
                    else:
                        print(f"The starting card is {cardIdToName(lastPlayedCards, player.effect)}")
                    cardsInDeckString = ""
                    for x in range(len(player.cards)):#show all your cards
                        cardsInDeckString += "| " + f"{x+1}."+cardIdToName(player.cards[x], player.effect)+" | "
                    print(f"what card do you want to play? (say 0 to grab the cards from the pile, say -1 to see other options)\n{cardsInDeckString}")
                elif numberCard == -5:
                    print(f"The seed is: {settings[0]}")
                elif numberCard == -6:
                    playerList.pop(player.number)
                    playingDirection = playingDirection * len(playerList)
                    print(f"u deleted {player.number+ 1}, {player.name} from the game")
                    historyOfCards.append("nothing, he disconnected")
                    loop = False
                elif numberCard == -7:
                    player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playerdCard, turn, extra = saveStates(player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playerdCard, turn, extra)
                    print("don't forget that u need to do -4 again to show ur options")
                elif numberCard == -8:
                    player.type = 0
                    print("okay, now u still gotta play a card tho")
                elif numberCard == -9:
                    id = int(input('what player id?'))
                    for x in range(len(playerList)):
                        if playerList[x].number == id-1:
                            playerList[x].type = 1
                elif numberCard == -10:
                    print("admin Tools:\n-10 this menu\n-11 add random colorblindness\n-12 instant win\n-13 add any card to your deck\n-14 to see which cards everyone has\n-15 print settings\n-16 to delete cards\n-17 to remove colorblindness\n-18 clear console\n-19 exit")
                elif numberCard == -11:
                    randomNumber = random.randint(0,100)
                    if randomNumber > 85:#the colorblind effect
                        player.effect = 3
                    elif randomNumber > 44:
                        player.effect = 2
                    else:
                        player.effect = 1
                elif numberCard == -12:
                    print("okay, now u still gotta play a card tho")
                    win[0] = True
                elif numberCard == -13:
                    adding = input("input ID\n>>>")
                    player.cards.append(adding)
                elif numberCard == -14:
                    lookAtCards(playerList)
                elif numberCard == -15:
                    print(settings)
                elif numberCard == -16:
                    for xyz in range(len(player.cards)):
                        player.cards.pop(0)
                elif numberCard == -17:
                    player.effect = 0
                elif numberCard == -18:
                    clear_console()
                elif numberCard == -19:
                    exit()
                else: #play the card
                    numberCard -= 1
                    splittedCard = player.cards[numberCard].split(".")
                    splittedLastCard = lastPlayedCards[len(lastPlayedCards)-1].split(".")
                    if int(splittedCard[0]) != len(cardColors)-1 and int(splittedLastCard[0]) != len(cardColors)-1: #check for wild or +4 card
                        if splittedCard[0] == splittedLastCard[0] or splittedCard[1] == splittedLastCard[1]:
                            lastPlayedCards.append(player.cards[numberCard])
                            player.cards.pop(numberCard)
                            print(f"you played {cardIdToName(lastPlayedCards[len(lastPlayedCards)-1], player.effect)}")
                            historyOfCards.append(lastPlayedCards[len(lastPlayedCards)-1])
                            loop = False
                            if len(player.cards) == 0:#check if someone has won
                                win[0] = True
                            if len(win) != 1:
                                while len(win) != 1:
                                    win.pop(1)
                            if len(lastPlayedCards) > 1:
                                playerdCard.append(lastPlayedCards[len(lastPlayedCards)-2])
                                lastPlayedCards.pop(len(lastPlayedCards)-2)
                        else:#it is not a available card
                            print("you can't play that card right now")
                    else:# play the wild or +4 card
                        if splittedCard[1] == '0' and int(splittedCard[0]) == len(cardColors)-1:#if you played a wild
                            loop1 = True
                            wildCardColorLoop = ""
                            for x in range(len(cardColors)-1):#show all your cards
                                wildCardColorLoop += f"| {x+1}.{cardColorsNames[x]} | "
                            while loop1 == True:
                                try:
                                    chosenColor = input(f"what color do you choose?\n{wildCardColorLoop}\n")#choose the color of the wild card
                                    chosenColor = int(chosenColor)
                                    if chosenColor-5 < len(cardColors)-1 and chosenColor-1 >= 0:
                                        lastPlayedCards.append(f"{len(cardColors)-1}.0.{chosenColor-1}")
                                        player.cards.pop(numberCard)
                                        if len(lastPlayedCards) > 1:
                                            playerdCard.append(lastPlayedCards[len(lastPlayedCards)-2])
                                            lastPlayedCards.pop(len(lastPlayedCards)-2)
                                        print(f"you played {cardIdToName(lastPlayedCards[len(lastPlayedCards)-1], player.effect)}")
                                        historyOfCards.append(lastPlayedCards[len(lastPlayedCards)-1])
                                        loop1 = False
                                        loop = False
                                        if chosenColor == -1:
                                            print("settings:\n-2 to see how many cards everyone has\n-3 to see the history\n-4 to show your options")
                                        elif chosenColor == -2:
                                            for x in range(len(playerList)):
                                                print(f"player {x}, {playerList[x].name+1} has {len(playerList[x].cards)} cards")
                                        elif chosenColor == -3:
                                            for x in range(len(historyOfCards)):
                                                if historyOfCards[x] != "nothing, he grabbed a card":
                                                    print(f"{historyPlayersThatPlayedACard[x]} played {cardIdToName(historyOfCards[x], player.effect)}")
                                                else:
                                                    print(f"{historyPlayersThatPlayedACard[x]} played {historyOfCards[x]}")
                                        elif chosenColor == -4:
                                            wildCardColorLoop = ""
                                            for x in range(len(cardColors)-1):#show all your cards
                                                wildCardColorLoop += f"| {x+1}.{cardColorsNames[x]} | "
                                    else:
                                        print("that is not an option")
                                        
                                except Exception as e:
                                    try:
                                        exec(chosenColor)
                                    except:
                                        print(e)
                                        print("please choose a number")
                        elif splittedLastCard[1] == '0' and int(splittedLastCard[0]) == len(cardColors)-1:
                            #someone has drawn a wild card, which cards can u play now
                            if len(splittedLastCard) == 3:
                                if splittedCard[0] == splittedLastCard[2]:
                                    lastPlayedCards.append(player.cards[numberCard])
                                    player.cards.pop(numberCard)
                                    if len(lastPlayedCards) > 1:
                                        playerdCard.append(lastPlayedCards[len(lastPlayedCards)-2])
                                        lastPlayedCards.pop(len(lastPlayedCards)-2)
                                    print(f"you played {cardIdToName(lastPlayedCards[len(lastPlayedCards)-1], player.effect)}")
                                    historyOfCards.append(lastPlayedCards[len(lastPlayedCards)-1])
                                    loop = False
                                    if len(player.cards) == 0:#check if someone has won
                                        win[0] = True
                                elif int(splittedCard[0]) == len(cardColors)-1:
                                    #if you want to play a +4 card
                                    lastPlayedCards.append(player.cards[numberCard])
                                    player.cards.pop(numberCard)
                                    if len(lastPlayedCards) > 1:
                                        playerdCard.append(lastPlayedCards[len(lastPlayedCards)-2])
                                        lastPlayedCards.pop(len(lastPlayedCards)-2)
                                    print(f"you played {cardIdToName(lastPlayedCards[len(lastPlayedCards)-1], player.effect)}")
                                    historyOfCards.append(lastPlayedCards[len(lastPlayedCards)-1])
                                    loop = False
                                    if len(player.cards) == 0:#check if someone has won
                                        win[0] = True
                                else:#it is not a available card
                                    print("you can't play that card right now")
                            else:
                                lastPlayedCards.append(player.cards[numberCard])
                                player.cards.pop(numberCard)
                                if len(lastPlayedCards) > 1:
                                    playerdCard.append(lastPlayedCards[len(lastPlayedCards)-2])
                                    lastPlayedCards.pop(len(lastPlayedCards)-2)
                                print(f"you played {cardIdToName(lastPlayedCards[len(lastPlayedCards)-1], player.effect)}")
                                historyOfCards.append(lastPlayedCards[len(lastPlayedCards)-1])
                                loop = False
                                if len(player.cards) == 0:#check if someone has won
                                    win[0] = True
                        else:
                            lastPlayedCards.append(player.cards[numberCard])
                            player.cards.pop(numberCard)
                            if len(lastPlayedCards) > 1:
                                playerdCard.append(lastPlayedCards[len(lastPlayedCards)-2])
                                lastPlayedCards.pop(len(lastPlayedCards)-2)
                            print(f"you played {cardIdToName(lastPlayedCards[len(lastPlayedCards)-1], player.effect)}")
                            historyOfCards.append(lastPlayedCards[len(lastPlayedCards)-1])
                            loop = False
                            if len(player.cards) == 0:#check if someone has won
                                win[0] = True                        
            else:
                print("you don't have a card in that slot")
        except Exception as e:
            try:
                exec(numberCard)
            except:
                print(e)
                print("try inputting a number")
    if checkForPlus(lastPlayedCards[len(lastPlayedCards)-1]) == True:
        for x in range(len(lastPlayedCards)-1):
            playerdCard.append(lastPlayedCards[len(lastPlayedCards)-2])
            lastPlayedCards.pop(len(lastPlayedCards)-2)
    return player, lastPlayedCards, playingDirection, win, playerdCard, turn, extra, playerList

def setupCardPile(color, types, special, settings): #shuffles and creates card deck
    cardPile = list()
    for y in range(settings[2]):#creates amount of color cards
        for x in range(len(color)-1):
            for i in range(len(types)):
                cardPile.append(f"{color[x]}.{types[i]}")
    for z in range(settings[3]):#creates special cards
        for x in range(len(special)):
            cardPile.append(f"{color[4]}.{special[x]}")
    random.shuffle(cardPile)
    return cardPile

def givePeoplePlayingCards(players, cards, settings):#give people starting amount of playing cards
    for x in range(len(players)):
        for y in range(settings[7]):
            players[x].cards.append(cards[0])
            cards.pop(0)
    return players, cards

def checkAmountOfCards(playerList):
        amount = list()
        for x in range(len(playerList)):
            amount.append(len(playerList[x].cards))
        return amount

def aiTurn(player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedCards, turn):

    def listIndexOutOfRange(amount, playerList):
        test = amount
        while test > len(playerList) -1 or test < 0:
            if test > len(playerList) -1: test -= len(playerList)
            elif test < 0: test += len(playerList)
        return test

    def transformWildIntoColorWild(card, bestColor):
        test = False
        if int(card.split(".")[0]) == len(cardColors)-1 and card.split(".")[1] == '0':#check if it is a wild card
            card += f".{bestColor[0]}"
        return card

    def checkNormalTurn(player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedPlusCards, bestColor, mode = 0):
        valueList = list()
        lastCard = lastPlayedCards[len(lastPlayedCards)-1]
        for x in range(len(player.cards)):
            testCard = player.cards[x]
            if testCard == -1:
                valueList.append(0)
            else:
                if int(testCard.split(".")[0]) != len(cardColors)-1 and int(lastCard.split('.')[0]) != len(cardColors)-1:#not a black card
                    if testCard.split(".")[0] == lastCard.split('.')[0] or testCard.split(".")[1] == lastCard.split('.')[1]:#if it's a playable colorcard
                        if checkForPlus(testCard) == True:#check if it is an pluscard
                            if uno[listIndexOutOfRange(player.number + playingDirection, playerList)] <= 3:
                                if testCard.split(".")[0] in bestColor:
                                    valueList.append(8)
                                else:
                                    valueList.append(7)
                            else:
                                if testCard.split(".")[0] in bestColor:
                                    valueList.append(5)
                                else:
                                    valueList.append(4)
                        elif testCard.split(".")[1] == "12":
                            if uno[listIndexOutOfRange(player.number + (-1 * playingDirection), playerList)] >= uno[listIndexOutOfRange(player.number +  playingDirection, playerList)]:
                                if testCard.split(".")[0] in bestColor:
                                    valueList.append(6)
                                else:
                                    valueList.append(5)
                            else:
                                if testCard.split(".")[0] in bestColor:
                                    valueList.append(2)
                                else:
                                    valueList.append(1)
                        elif testCard.split(".")[1] == "10":
                            if uno[listIndexOutOfRange(player.number + (2 * playingDirection), playerList)] >= uno[listIndexOutOfRange(player.number +  playingDirection, playerList)]:
                                if testCard.split(".")[0] in bestColor:
                                    valueList.append(7)
                                else:
                                    valueList.append(6)
                            else:
                                if testCard.split(".")[0] in bestColor:
                                    valueList.append(2)
                                else:
                                    valueList.append(1)
                        else:
                            if testCard.split(".")[0] in bestColor:
                                valueList.append(3)
                            else:
                                valueList.append(2)
                    else:
                        valueList.append(-1)
                else:#if it's a black card
                    if checkForPlus(testCard) == True:
                        if uno[listIndexOutOfRange(player.number + playingDirection, playerList)] <= len(player.cards):
                            
                                valueList.append(7)
                        else:
                            
                                valueList.append(3)
                    elif testCard.split('.')[1] == '0' and int(testCard.split('.')[0]) == len(cardColors)-1:#if you played a wild
                        if lastCard.split('.')[0] in bestColor: 
                            valueList.append(1)
                        else:
                            valueList.append(5)
                    elif lastCard.split('.')[1] == '0' and int(lastCard.split('.')[0]) == len(cardColors)-1:
                        if len(lastCard.split('.')) == 3:
                            if testCard.split(".")[0] == lastCard.split('.')[2]:#if it's a playable colorcard
                                if checkForPlus(testCard) == True:#check if it is an pluscard
                                    if uno[listIndexOutOfRange(player.number + playingDirection, playerList)] <= 3:
                                        if testCard.split(".")[0] in bestColor:
                                            valueList.append(8)
                                        else:
                                            valueList.append(7)
                                    else:
                                        if testCard.split(".")[0] in bestColor:
                                            valueList.append(5)
                                        else:
                                            valueList.append(4)
                                elif testCard.split(".")[1] == "12":
                                    if uno[listIndexOutOfRange(player.number + (-1 * playingDirection), playerList)] >= uno[listIndexOutOfRange(player.number +  playingDirection, playerList)]:
                                        if testCard.split(".")[0] in bestColor:
                                            valueList.append(6)
                                        else:
                                            valueList.append(5)
                                    else:
                                        if testCard.split(".")[0] in bestColor:
                                            valueList.append(2)
                                        else:
                                            valueList.append(1)
                                elif testCard.split(".")[1] == "10":
                                    valueList.append(3)
                                else:
                                    valueList.append(2)
                            else:
                                valueList.append(-1)
                    else:
                        if checkForPlus(testCard) == True:#check if it is an pluscard
                            if uno[player.number + playingDirection] <= 3:
                                if testCard.split(".")[0] in bestColor:
                                    valueList.append(8)
                                else:
                                    valueList.append(7)
                            else:
                                if testCard.split(".")[0] in bestColor:
                                    valueList.append(5)
                                else:
                                    valueList.append(4)
                        elif testCard.split(".")[1] == "12":
                            if uno[listIndexOutOfRange(player.number + (-1 * playingDirection), playerList)] >= uno[listIndexOutOfRange(player.number +  playingDirection, playerList)]:
                                if testCard.split(".")[0] in bestColor:
                                    valueList.append(6)
                                else:
                                    valueList.append(5)
                            else:
                                if testCard.split(".")[0] in bestColor:
                                    valueList.append(2)
                                else:
                                    valueList.append(1)
                        elif testCard.split(".")[1] == "10":
                            if uno[listIndexOutOfRange(player.number + (2 * playingDirection), playerList)] >= uno[listIndexOutOfRange(player.number +  playingDirection, playerList)]:
                                if testCard.split(".")[0] in bestColor:
                                    valueList.append(7)
                                else:
                                    valueList.append(6)
                            else:
                                if testCard.split(".")[0] in bestColor:
                                    valueList.append(2)
                                else:
                                    valueList.append(1)
                        else:
                            valueList.append(-1)

                        
                    
        return valueList

    #print(turn) #for if problems arise
    #if turn == 334: #for if problems arise
    #   print("placeholder") #for if problems arise
    uno = checkAmountOfCards(playerList)

    player.cards.append(-1)
    valueList = list()
    amountOfColor = list()
    bestColor = list()
    for x in range(len(cardColors)-1):#add 0 to list with color amount
        amountOfColor.append(0)
    #if turn == 188: print(player.cards)
    xx = 0
    for x in range(len(player.cards)-1):#check amount of cards of color
        if type(player.cards[xx]) == list:
            player.cards.pop(xx)
            xx -= 1
        elif int(player.cards[xx].split(".")[0]) != len(cardColors) - 1:
            amountOfColor[int(player.cards[xx].split(".")[0])] += 1
        xx += 1
    for x in range(len(amountOfColor)):
        testForHighest = 1
        for y in range(len(amountOfColor)): 
            if amountOfColor[x] < amountOfColor[y]:
                testForHighest = 0
        if testForHighest == 1:
            bestColor.append(x)
    for x in range(len(bestColor)):
        bestColor[x] = str(bestColor[x])


    if playingDirection > 0:
        playingDirection = 1
    else:
        playingDirection = -1
    stackedPlusCards = 0       
    lastPlayedCardID = lastPlayedCards[len(lastPlayedCards)-1]   
    if len(win) != 1 or turn == 1:
        pass   
    else:
        if int(lastPlayedCardID.split(".")[0]) == len(cardColors)-1 and lastPlayedCardID.split(".")[1] == '1':#check if it is a +4 card
            stackedPlusCards += 4
        elif lastPlayedCardID.split(".")[1] == '11':#check if it is a +2 card
            stackedPlusCards += 2
    if stackedPlusCards > 0:#if it was a + card, check how many of them are stacked
        check = 1
        for x in range(2, len(lastPlayedCards)):
            if check == 1:
                if int(lastPlayedCards[len(lastPlayedCards)- x].split(".")[0]) == len(cardColors)-1 and lastPlayedCards[len(lastPlayedCards)-x].split(".")[1] == '1':#check if it is a +4 card
                    stackedPlusCards += 4
                elif lastPlayedCards[len(lastPlayedCards)-x].split(".")[1] == '11':#check if it is a +2 card
                    stackedPlusCards += 2
                else:
                    check = 0
    yourAmountPlusCards = [0, 0]
    if stackedPlusCards > 0:
        for x in range(len(player.cards)): #check if you have any + card to counter
            if player.cards[x] != -1:
                if int(player.cards[x].split(".")[0]) == len(cardColors)-1 and player.cards[x].split(".")[1] == '1':
                    yourAmountPlusCards[1] += 1
                elif player.cards[x].split(".")[1] == '11':
                    yourAmountPlusCards[0] += 1
        if yourAmountPlusCards[0] + yourAmountPlusCards[1] == 0: #if you have no cards to counter the + card, automatically get the cards
            playerListEndOfGame[player.number].bullied += 1
            cardsForPlayer, cards, lastPlayedCards, playedCards = (takeCardFromDeck(stackedPlusCards, cards, lastPlayedCards, player, playedCards, 1))
            for x in range(len(cardsForPlayer)):
                player.cards.append(cardsForPlayer[x])
            win.append("+")
            valueList = checkNormalTurn(player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedPlusCards, bestColor, 1)
            stackedPlusCards = -1
        else:
            for x in range(len(player.cards)):#give value to cards
                testCard = player.cards[x]
                if testCard == -1:
                    valueList.append(0)
                else:
                    if int(testCard.split(".")[0]) == len(cardColors)-1 and testCard.split(".")[1] == "1":
                        if uno[listIndexOutOfRange(player.number + playingDirection, playerList)] <= 2:
                            valueList.append(7)
                        else:
                            valueList.append(4)
                    elif testCard.split(".")[1] == '11':
                        if testCard.split(".")[0] in bestColor:
                            valueList.append(6)
                        else:
                            valueList.append(5)
                    else:
                        if int(lastPlayedCardID.split(".")[0]) != len(cardColors)-1:#if it's a +2
                            if testCard.split(".")[0] == lastPlayedCardID.split(".")[0]:#if it's playable
                                if testCard.split(".")[0] in bestColor: #if it's your fav color
                                    valueList.append(3)
                                else:
                                    valueList.append(2)
                            else:
                                valueList.append(-1)
                        else:#if he played a wild
                            if testCard.split(".")[0] in bestColor: #if it's your fav color
                                valueList.append(1)
                            else:
                                valueList.append(0)
     
    else:
        valueList = checkNormalTurn(player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedPlusCards, bestColor)

    bestChoice = list()#look what the best option is
    for x in range(len(valueList)):
        testForHighest = 1
        for y in range(len(valueList)): 
            if valueList[x] < valueList[y]:
                testForHighest = 0
        if testForHighest == 1:
            bestChoice.append(x)



    if len(bestChoice) > 1:
        randomChosen = random.randint(0, len(bestChoice)-1)
        if player.cards[randomChosen] == -1:
            player.cards.remove(-1)
            cardsForPlayer, cards, lastPlayedCards, playedCards = (takeCardFromDeck(stackedPlusCards + 1, cards, lastPlayedCards, player, playedCards, 1))
            for x in range(len(cardsForPlayer)):
                player.cards.append(cardsForPlayer[x])
            playerListEndOfGame[player.number].grabbedCard += 1
            historyOfCards.append("nothing, he grabbed a card")
        else:
            if len(win) > 1:
                for i in range(len(win)-1):
                    win.pop(1)
            if checkForPlus(player.cards[randomChosen]) == False and stackedPlusCards > 0:
                playerListEndOfGame[player.number].bullied += 1
                player.cards.remove(-1)
                cardsForPlayer, cards, lastPlayedCards, playedCards = (takeCardFromDeck(stackedPlusCards + 1, cards, lastPlayedCards, player, playedCards, 1))
                for x in range(len(cardsForPlayer)):
                    player.cards.append(cardsForPlayer[x])
            lastPlayedCards.append(transformWildIntoColorWild(player.cards[bestChoice[randomChosen]], bestColor))
            historyOfCards.append(lastPlayedCards[len(lastPlayedCards)-1])
            player.cards.pop(bestChoice[randomChosen])
    else:
        if player.cards[bestChoice[0]] == -1:
            player.cards.remove(-1)
            cardsForPlayer, cards, lastPlayedCards, playedCards = (takeCardFromDeck(stackedPlusCards + 1, cards, lastPlayedCards, player, playedCards, 1))
            for x in range(len(cardsForPlayer)):
                player.cards.append(cardsForPlayer[x])
            playerListEndOfGame[player.number].grabbedCard += 1
            historyOfCards.append("nothing, he grabbed a card")
        else:
            if len(win) > 1:
                for i in range(len(win)-1):
                    win.pop(1)
            if checkForPlus(player.cards[bestChoice[0]]) == False and stackedPlusCards > 0:
                playerListEndOfGame[player.number].bullied += 1
                player.cards.remove(-1)
                cardsForPlayer, cards, lastPlayedCards, playedCards = (takeCardFromDeck(stackedPlusCards + 1, cards, lastPlayedCards, player, playedCards, 1))
                for x in range(len(cardsForPlayer)):
                    player.cards.append(cardsForPlayer[x])
            lastPlayedCards.append(transformWildIntoColorWild(player.cards[bestChoice[0]], bestColor))
            historyOfCards.append(lastPlayedCards[len(lastPlayedCards)-1])
            player.cards.pop(bestChoice[0])
    if stackedPlusCards == -1 and checkForPlus(lastPlayedCards[len(lastPlayedCards)-1]) == True:
        for x in range(len(lastPlayedCards)-1):
            playedPlusCards.append(lastPlayedCards[len(lastPlayedCards)-2])
            lastPlayedCards.pop(len(lastPlayedCards)-2)
    try:
        player.cards.remove(-1)
    except:
        pass
    historyPlayersThatPlayedACard.append(f"{player.number +1}, {player.name}")
    print(f"player {player.number+ 1}, {player.name} played: {cardIdToName(lastPlayedCards[len(lastPlayedCards)-1])}")
    if len(player.cards) == 0: win[0] = True
    return cards, lastPlayedCards, playerList, settings, playingDirection, win, playedCards

def playerTurn(player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedCards, turn, extra = []):

    
    stackedPlusCards = 0

    lastPlayedCard = cardIdToName(lastPlayedCards[len(lastPlayedCards)-1], player.effect)
    if settings[4] > 1: #only if it's not singleplayer
        clear_console()
        input(f"it's player number {player.number+1}, {player.name} their turn\nPress the enter button to play\n")
    checkForUno(playerList, player)
    lastPlayedCardID = lastPlayedCards[len(lastPlayedCards)-1]
    if len(win) != 1 or turn == 1:
        pass
    else:
        if int(lastPlayedCardID.split(".")[0]) == len(cardColors)-1 and lastPlayedCardID.split(".")[1] == '1':#check if it is a +4 card
            stackedPlusCards += 4
            if turn != 1:
                print(f"The last player {historyPlayersThatPlayedACard[len(historyPlayersThatPlayedACard)-1]} played {cardIdToName(lastPlayedCardID, player.effect)}")
            else:
                print(f"The starting card is {cardIdToName(lastPlayedCard, player.effect)}")
        elif lastPlayedCardID.split(".")[1] == '11':#check if it is a +2 card
            stackedPlusCards += 2
            if turn != 1:
                print(f"The last player {historyPlayersThatPlayedACard[len(historyPlayersThatPlayedACard)-1]} played {cardIdToName(lastPlayedCardID, player.effect)}")
            else:
                print(f"The starting card is {cardIdToName(lastPlayedCard, player.effect)}")
    if stackedPlusCards > 0:#if it was a + card, check how many of them are stacked
        check = 1
        for x in range(2, len(lastPlayedCards)):
            if check == 1:
                if int(lastPlayedCards[len(lastPlayedCards)- x].split(".")[0]) == len(cardColors)-1 and lastPlayedCards[len(lastPlayedCards)-x].split(".")[1] == '1':#check if it is a +4 card
                    stackedPlusCards += 4
                elif lastPlayedCards[len(lastPlayedCards)-x].split(".")[1] == '11':#check if it is a +2 card
                    stackedPlusCards += 2
                else:
                    check = 0
    yourAmountPlusCards = [0, 0]
    if stackedPlusCards > 0:
        for x in range(len(player.cards)): #check if you have any + card to counter
            if int(player.cards[x].split(".")[0]) == len(cardColors)-1 and player.cards[x].split(".")[1] == '1':
                yourAmountPlusCards[1] += 1
            elif player.cards[x].split(".")[1] == '11':
                yourAmountPlusCards[0] += 1
        if yourAmountPlusCards[0] + yourAmountPlusCards[1] == 0: #if you have no cards to counter the + card, automatically get the cards
            cardsForPlayer, cards, lastPlayedCards, playedCards = (takeCardFromDeck(stackedPlusCards, cards, lastPlayedCards, player, playedCards))
            playerListEndOfGame[player.number].bullied += 1
            for x in range(len(cardsForPlayer)):
                player.cards.append(cardsForPlayer[x])
            player, lastPlayedCards, playingDirection, win, playedCards, turn, extra, playerList= chooseCard(player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedCards, turn, extra)
        else:
            cardsInDeckString = ""
            for x in range(len(player.cards)):#show all your cards
                cardsInDeckString += "| " + f"{x+1}."+cardIdToName(player.cards[x], player.effect)+" | "
            print(f"what card do you want to play? (if you choose something that isn't a + card it will collect the cards, and ask again after you have collected the cards) \n(say 0 to grab the cards from the pile, say -1 to see other options)\n{cardsInDeckString}")
            loop = True
            while loop == True:
                try:
                    numberCard = input()
                    numberCard = int(numberCard)
                    if numberCard <= len(player.cards):#check if it's a card you have
                        if numberCard == 0:
                            if (lastPlayedCards[len(lastPlayedCards)-1].split(".")[0] == "4" and lastPlayedCards[len(lastPlayedCards)-1].split(".")[1] == "1") or (lastPlayedCards[len(lastPlayedCards)-1].split(".")[1] == "11" and lastPlayedCards[len(lastPlayedCards)-1].split(".")[0] != "4"):
                                win.append("+")
                            cardsForPlayer, cards, lastPlayedCards, playedCards = (takeCardFromDeck(stackedPlusCards + 1, cards, lastPlayedCards, player, playedCards))
                            for x in range(len(cardsForPlayer)):
                                player.cards.append(cardsForPlayer[x])
                            loop = False
                            playerListEndOfGame[player.number].grabbedCard += 1
                            playerListEndOfGame[player.number].bullied += 1
                            historyOfCards.append("nothing, he grabbed a card")
                        elif numberCard == -1:
                            print("settings:\n-2 to see how many cards everyone has\n-3 to see the history\n-4 to show your options\n-5 to show the seed\n-6 to disconnect this user\n-7 savestates\n-8 make user into a bot\n-9 change bot into user")
                        elif numberCard == -2:
                            for x in range(len(playerList)):
                                print(f"player {playerList[x].number+1}, {playerList[x].name} has {len(playerList[x].cards)} cards")#show amount of cards everyone has
                        elif numberCard == -3:
                            for x in range(len(historyOfCards)):
                                if historyOfCards[x] != "nothing, he grabbed a card" and historyOfCards[x] != "nothing, he disconnected":
                                    print(f"{historyPlayersThatPlayedACard[x]} played {cardIdToName(historyOfCards[x], player.effect)}")
                                else:
                                    print(f"{historyPlayersThatPlayedACard[x]} played {historyOfCards[x]}")
                        elif numberCard == -4:
                            if turn != 1:
                                print(f"The last player {historyPlayersThatPlayedACard[len(historyPlayersThatPlayedACard)-1]} played {cardIdToName(lastPlayedCard, player.effect)}")
                            else:
                                print(f"The starting card is {cardIdToName(lastPlayedCard, player.effect)}")
                            cardsInDeckString = ""
                            for x in range(len(player.cards)):#show all your cards
                                cardsInDeckString += "| " + f"{x+1}."+cardIdToName(player.cards[x], player.effect)+" | "
                            print(f"what card do you want to play? (say 0 to grab the cards from the pile, say -1 to see other options)\n{cardsInDeckString}")
                        elif numberCard == -5:
                            print(f"The seed is: {settings[0]}")
                        elif numberCard == -6:
                            playerList.pop(player.number)
                            playingDirection = playingDirection * len(playerList)
                            print(f"u deleted {player.number+ 1}, {player.name} from the game")
                            historyOfCards.append("nothing, he disconnected")
                            loop = False
                        elif numberCard == -7:
                            player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedCards, turn, extra = saveStates(player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedCards, turn, extra)
                            print("don't forget that u need to do -4 again to show ur options")
                        elif numberCard == -8:
                            player.type = 0
                            print("okay, now u still gotta play a card tho")
                        elif numberCard == -9:
                            id = int(input('what player id?'))
                            for x in range(len(playerList)):
                                if playerList[x].number == id-1:
                                    playerList[x].type = 1
                        elif numberCard == -10:
                            print("admin Tools:\n-10 this menu\n-11 add random colorblindness\n-12 instant win\n-13 add any card to your deck\n-14 to see which cards everyone has\n-15 print settings\n-16 to delete cards\n-17 to remove colorblindness\n-18 clear console\n-19 exit")
                        elif numberCard == -11:
                            randomNumber = random.randint(0,100)
                            if randomNumber > 85:#the colorblind effect
                                player.effect = 3
                            elif randomNumber > 44:
                                player.effect = 2
                            else:
                                player.effect = 1
                        elif numberCard == -12:
                            print("okay, now u still gotta play a card tho")
                            win[0] = True
                        elif numberCard == -13:
                            adding = input("input ID\n>>>")
                            player.cards.append(adding)
                        elif numberCard == -14:
                            lookAtCards(playerList)
                        elif numberCard == -15:
                            print(settings)
                        elif numberCard == -16:
                            for xyz in range(len(player.cards)):
                                player.cards.pop(0)
                        elif numberCard == -17:
                            player.effect = 0
                        elif numberCard == -18:
                            clear_console()
                        elif numberCard == -19:
                            exit()
                        else:
                            numberCard -= 1
                            if int(player.cards[numberCard].split(".")[0]) == len(cardColors)-1 and player.cards[numberCard].split(".")[1] == '1':#check if it is a +4 card
                                lastPlayedCards.append(player.cards[numberCard])
                                print(f"you played {cardIdToName(lastPlayedCards[len(lastPlayedCards)-1], player.effect)}")#show what you have played
                                historyOfCards.append(lastPlayedCards[len(lastPlayedCards)-1])
                                player.cards.pop(numberCard)
                                loop = False
                            elif player.cards[numberCard].split(".")[1] == '11':#check if it is a +2 card
                                lastPlayedCards.append(player.cards[numberCard])
                                print(f"you played {cardIdToName(lastPlayedCards[len(lastPlayedCards)-1], player.effect)}")#show what you have played
                                historyOfCards.append(lastPlayedCards[len(lastPlayedCards)-1])
                                player.cards.pop(numberCard)
                                loop = False
                            else:
                                playerListEndOfGame[player.number].bullied += 1
                                print("\nthe last player played a + card so we will grab your cards first, then you can choose which one to play\n")#get cards
                                time.sleep(1)
                                print(lastPlayedCards)
                                cardsForPlayer, cards, lastPlayedCards, playedCards = (takeCardFromDeck(stackedPlusCards, cards, lastPlayedCards, player, playedCards))
                                for x in range(len(cardsForPlayer)):#add cards to his deck
                                    player.cards.append(cardsForPlayer[x])
                                player, lastPlayedCards, playingDirection, win, playedCards, turn, extra, playerList = chooseCard(player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedCards, turn, extra)
                                loop = False
                    else:
                        print("you don't have a card in that slot")
                except Exception as e:
                    try:
                        exec(numberCard)
                    except:
                        print("try a number")
                        print(e)
    else:
        player, lastPlayedCards, playingDirection, win, playedCards, turn, extra, playerList= chooseCard(player, cards, lastPlayedCards, playerList, settings, playingDirection, activePlayer, win, playedCards, turn, extra)
    if settings[4] > 1: input(f"that was your turn {player.name}\npress enter so the next player can play\n")
    historyPlayersThatPlayedACard.append(f"{player.number +1}, {player.name}")
    if len(player.cards) == 0:
        win[0] = True
    return cards, lastPlayedCards, playerList, settings, playingDirection, win, playedCards, extra
                
def whoHasMost(compareList):
    best = list()  
    for x in range(len(compareList)):
        testForHighest = 1
        for y in range(len(compareList)): 
            if compareList[x] < compareList[y]:
                testForHighest = 0
        if testForHighest == 1:
            best.append(x)
    return best

def classDataToLists(list1, list2, list3):
    for x in range(len(playerListEndOfGame)):
        try:
            list1.append(playerListEndOfGame[x].cardsFromPile)
            list2.append(playerListEndOfGame[x].bullied)
            list3.append(playerListEndOfGame[x].grabbedCard)
        except Exception as e:
            print(e)
    return list1, list2, list3

def statsCalculationForMultipleFinishers(var, words):
    try:
        if len(whoHasMost(var)) == 1: 
            print(f"The player who played the most {words} was:\n{playerListEndOfGame[whoHasMost(var)[0]].number}, {playerListEndOfGame[whoHasMost(var)[0]].name} with {var[whoHasMost(var)[0]]} {words}")
        else:
            print(f"the players that played the most {words} were:")
            for x in range(len(whoHasMost(var))):
                print(f"{playerListEndOfGame[whoHasMost(var)[x]].number}, {playerListEndOfGame[whoHasMost(var)[x]].name}")
            print(f"with {var[whoHasMost(var)[0]]} {words}")
    except:
        print(f"crashed whilst trying to load stats about {words}")

#config thingys
createConfig(ownPath)
setting = rawSettingsToSettings(readConfig())
if setting[0] != False: random.seed(setting[0])#set seed if seed in config


#basic settings
cardTypes = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12]#1 deck of color cards per color
#all types of cards with a color 0-9 numbers, 10 skip, 11 +2, 12 reverse
cardTypesNames = ["zero", 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'skip', 'draw two', 'reverse']
cardColors = [0, 1, 2, 3, 4]#all colors, special, red, blue, green, yellow
yellowGreenColorblindCardColorsNames = ["red", 'blue', 'green or yellow', 'green or yellow', 'black']
blueRedColorblindCardColorsNames = ["red or blue", 'red or blue', 'green', 'yellow', 'black']
colorblindCardColorsNames = ["a color", 'a color', 'a color', 'a color', 'black']
cardColorsNames = ["red", 'blue', 'green', 'yellow', 'black']
specials = [0, 1]#the special cards, wild, draw 4
specialsNames = ["wild", 'draw four']
computerNameList = ['thomas', 'thom', 'muik', 'coen', 'staninna', 'stijn', 'florida man', 'mandrex', 'bob', 'grian', 'mumbo jumbo', 'scar', '[CLASSEFIED]', 'george',
'lianne', 'tommy', 'tiffany', 'katie', 'jase', 'lennert', 'mellodie', 'mark rutte', 'Master of scares', 'Null', 'Herobrine', 'None', 'Undefined', 'liam', 'anne', 'colorblind guy', 
'Ms.Kittens', 'attack helicopter', 'mr Blue Sky','joe','Vogeljongen', 'kaas', 'peter quill','Nat','Loki','Nick Furry','Vision', 'Eather', 'Mind Stone', 'Power Stone','Tesseract','Wanda', 'Soul Stone', 'Time Stone',
'Dr Strange','Coulson', 'Banner','Peter Parker','Tony Stark', 'Scott Lang','pjotter', 'Thanos', 'Thor', 'GLaDOS', 'chell', 'Phileine', 'emiel', 'twan', 'david', 'joelia', 'sneal', 'pieter', 'merijn', 'marjin','ScuttleBug','Coin','Skeeter','Snailcorn','Snow Spike','Fire Piranha','Spike Bass','Sushi','Bee Mario','Fly Mario','Ice Mario','Ranbow Mario','Luma','Rosalina','Honeybee',
'oldmartijntje', 'martijn', 'mercury', 'lara', 'steve jobs', 'mark zuckerburg', 'elon musk', 'sinterklaas', 'bart', 'ewood', 'mathijs', 'joris', 'zwarte piet','Gamora','Why Is Gamora?','I Am Groot','Rocket Raccoon','KORG','Crowber','Dry Bowser','Fury Bowser','Cat Bowser','Lakithunder','Clone Mario','MummiPokey','Monty Tank',
'izuku','bakugo','uraraka','iida','mineta','todoroki','Eris','Sylphiette','Rudeus','Roxy','Tomori','Ruijerd','neko','Dr Octopus','NoobSlayer69','Jeb_','DinnerBone','debaas','Goomba','smurf','bomb-omb','koopa','luigi','daisy','Thwomp','Frog Mario','Cheep Chomp','BlockHopper','Unagi','Boo Mario','Spring Mario',
'peach','piranha','Waluigi','shy-guy','toadette','king bob-omb','yoshi','Bullet Bill','birdo','banzai bill','Bowser','Cheep Cheep','chargin\' chuck','Buzzy Beetle','Dry Bones','Fish Bone','Fuzzle','Larry','Iggy','Lemmy','Ludwig','Morton','Roy','Wendy','Prinsess Toadstool','Mega Mole','Bowser jr','Fuzzy','Kamek',
'Blargg','Hammer Brother','Blurp','Dino-Rhino','Magikoopa','Pokey','Montey Mole','Ninji','Muncher','Porcupuffer','Rex','Reznor','Spiny','Sumo Brother','Swooper','Big Boo','Thwimp','Urchin','Wiggler','Boomerang Boom','Boom-Boom','FireBro','Chain Chomp','Balloon Mario','Raccoon Mario','Shoe Mario','Hammer Mario','P-Wing',
'Fire Chomp','Ice Bro','Spike','Rocky Wrench','Wart','Behemot King','Snifit','Phanto','Pidgit','Blooper','Lakitu','Geno','Hoot','Tuxie','Dorrie','Koopa the quick','Mips','Toad','Ukkiki','Big Bully','Bully','Wing Mario','Vanish Mario','Metal Mario','Bunny Mario','Space Mario','Aqua MarioBubble Mario','Cappy','Cape Mario',
'Coud Mario','Rock Mario','Spin Drill','White Tanooki Mario','Statue Mario','Propeller Box','? Box','Gold Block','White Raccoon Mario','Magmaargh','Double Mario','Elder Princess Shroob','Fawful','Kylie Koopa','Princess Shroob','Professor E. Gadd','Elvin Gadd','Shroob','Stuffwell','Toadiko','Toadbert','Yoob','Toad Doctor',
'Blue Toad','Spin Drift','Motos','Piantas','Shadow Luigi','Pink-gold peach','Invincible Mario','Mini Mario','Mega Mario','Shell Mario','Cat Mario','Cosmic Mario','Fire Mario','Propeller Mario','Ice Mario','Gold Mario','Pinguin mario','Tanuki Mario','Toadsworth','Fludd','Petey Piranha','Shadow Mario','Klepto','Wriggler','Whomp King','Whomp','Money Bag','EyeRock','Amp',
'Shrooblet','Boom Guy','Koopeleon','Boo Guy','Elasto-Piranha','Spiny Shroopa','Lakitufo','Dr. Shroob','Pidgit','Coconutter','Galoomba','Gnarantula','RC Shroober','Shrooba Diver','Dark Boo','Snifaro','Elite Boom Guy','Thwack','Tanoomba','Red Coconutter','Gold Koopeleon','	Blazing Shroob',
'Aurora Block','Popple','Blue switch','Dr Snoozemore','Control Block','Empty Block','L Block','Laser Block','M Block','Pi\'illoper','Recovery Block','Save Album','Simu-Block','Small Shine Block',
'Ice Flower','Cannonball','Wiggly','Bros. Flower','Green Shell','Dreambunny','Mushroom','Super Mushroom','Mega Phil','Ultra Mushroom','Max Mushroom','Mole Hunt Host','Mushroom Drop','Super Drop',
'Ultra Drop','Private Goomp','1-up Mushroom','1-up Super','Corporal Paraplonk','Refreshing Herb','Green Pepper','Red Pepper','Antasma','Lil\' Massif','Bedsmith','Big Massif','Luiginoid','Blue Pepper','Dream stone\'s spirit',
'Price Dreambert','Time hole','Brickle','Trampoline','Treasure chest','Warp block','Eldream','Warp Pipe','Yellow switch','Hooski','Zeekeeper','Bros. Ball.','Starlow','Cush','Brock','Britta','Nommon','Mix Flower','Red Shell','Copy Flower','Seabury','Seabelle','Pocket Chomp','Smash Egg','Seadring','Shelltop',
'Thwack Totem','Guardian Shroob','Shroid','Love Bubble','Skellokey','Handfake','Fly Guy','Piranha Planet','Wonder Thwack','Tashrooba','Snoozorb','','Soul Bubble','Shroob Rex','Shroobsworth','Intern Shroob','Ghoul Guy','Lethal Bob-omb','Baby Bowser','Exor','Junior Shrooboid','Hammer Bros','Swiggler','Sunnycide','Shrooboid Brat','Mrs. Thwomp','Commander Shroob','Support Shroobs','Elder Shrooboid','Shrowser','Baby Mario','Baby Luigi','Dream Luigi','4-Bros. Random Block','Adult Shine Block','Broggy',
'Nebula' ,'Drax','Hugo de Jonge','thierry baudet','Jesse Klaver','Djoopie','MisterPringleMan','Agent Carter','Misterio','Captain Marvel','Odin','Stan Lee','Fitz', 'Hawk Eye','Skye','Black Panther','Jemma Simmons', 'Mario', 'Quick silver','Wolverine', 'Deadpool','Flash','SuperMan','Batman','Mantis',
'mandy','madelief','anne nieuwenhuis','stan','nathalie','djurre','rick','annieltje','sanne','elize','elise','luna','lianne','julia','ingrid','tiff','sven','lennert','johnny','kimberly','daniel','jamy','lynn','mitch','roos','lotte','matthew','emilia','mia','anna','lisanne','renske','ferris',
'vivienne','frankaaaa','elvirus','nathan','simon','bo','jasmine','mart','gilli djojo','king papi','iris','melis','jelte','boris johnson','naomi','merlijn','tineke','mr.muffinnn','timo','niels','duncan','morris','donnie','manouk','jelle','corne','elke','mariska','melissa','luca','maddo','luuk',
'randerkip','marten','tim','sam','samuel','eva','fernndo','kirsten','david','yarilin','fatma','matthijs','tino','coen','annefleurr','noa','adrienne','niels','kim','jasper','stevey','guusje','lone','xander','jordy','jochem','julia','sem','toine','mark','laurens','barbara','floor','ruben','aqua',
'finn','frank','poerd','luna','ezraki','esther','alicia','andres','fenne','babette','dante','jonne','leon','kevin','rio','langefries','danique','virtualpeko','yassin','liz','sweetie','sb','raoul','thijs','arianne','henk','henk de steen','henkie spenkie','yeetus']
colorblindNames = ['thomas', 'george', 'colorblind guy','thierry baudet']
cardTypes, cardTypesNames, cardColors, yellowGreenColorblindCardColorsNames, blueRedColorblindCardColorsNames, colorblindCardColorsNames, cardColorsNames, specials, specialsNames = pluginLoad(cardTypes, cardTypesNames, cardColors, yellowGreenColorblindCardColorsNames, blueRedColorblindCardColorsNames, colorblindCardColorsNames, cardColorsNames, specials, specialsNames)
#creating players
playerList = list()
playerListEndOfGame = list()
for i in range(setting[4]):
    if setting[6] == True:
        while True:
            playerName = input(f"hello player number {len(playerList)+1}, what is your name?\n>>>")
            if playerName != "":
                playerList.append(player(1, playerName, [], 0, [], len(playerList)))
                playerListEndOfGame.append(player(1, playerName, [], 0, [], len(playerList)))
                if playerList[len(playerList)-1].name.lower() in colorblindNames:
                    playerList[len(playerList)-1].effect = 1
                break
    else:
        playerList.append(player(1, computerNameList[random.randint(0, len(computerNameList)-1)], [], 0, [], len(playerList)))
        playerListEndOfGame.append(player(1, playerList[len(playerList)-1].name, [], 0, [], len(playerList)+1))
        if playerList[len(playerList)-1].name.lower() in colorblindNames and setting[8] == True:
            randomNumber = random.randint(0,100)
            if randomNumber > 85:#the colorblind effect
                playerList[len(playerList)-1].effect = 3
            elif randomNumber > 44:
                playerList[len(playerList)-1].effect = 2
            else:
                playerList[len(playerList)-1].effect = 1

    randomNumber = random.randint(0,100)
    if randomNumber < 8  and setting[8] == True:#the colorblind effect
        randomNumber = random.randint(0,100)
        if randomNumber > 85:
            playerList[len(playerList)-1].effect = 3
        elif randomNumber > 44:
            playerList[len(playerList)-1].effect = 2
        else:
            playerList[len(playerList)-1].effect = 1

for i in range(setting[5]):
    if setting[1] != "Exercise":
        playerList.append(player(0, computerNameList[random.randint(0, len(computerNameList)-1)], [], 0, [], len(playerList)))
        playerListEndOfGame.append(player(0, playerList[len(playerList)-1].name, [], 0, [], len(playerList)+1))
        if playerList[len(playerList)-1].name.lower() in colorblindNames.lower() and setting[8] == True:
            randomNumber = random.randint(0,100)#the colorblind effect
            if randomNumber > 85:
                playerList[len(playerList)-1].effect = 3
            elif randomNumber > 44:
                playerList[len(playerList)-1].effect = 2
            else:
                playerList[len(playerList)-1].effect = 1
    else:
        playerList.append(player(0, computerNameList[random.randint(0, len(computerNameList)-1)], [], 0, [], len(playerList)))
        playerListEndOfGame.append(player(0, playerList[len(playerList)-1].name, [], 0, [], len(playerList)+1))

    if random.randint(0,100) > 8 and setting[8] == True:#the colorblind effect
        randomNumber = random.randint(0,100)
        if randomNumber > 85:
            playerList[len(playerList)-1].effect = 3
        elif randomNumber > 44:
            playerList[len(playerList)-1].effect = 2
        else:
            playerList[len(playerList)-1].effect = 1

try:
    #creating a game
    cardDeck = setupCardPile(cardColors, cardTypes, specials, setting)
    playedPlusCards = list()
    playedCardsPile = [cardDeck[0]]#start card
    cardDeck.pop(0)#remove start card from cards list
    playerDirection = 1
    playerList, cardDeck = givePeoplePlayingCards(playerList, cardDeck, setting)
    activePlayer = random.randint(0, len(playerList)-1)

    #the infinite loop which is called a game
    answer = 0
    turn = 0
    win = [False]
    #things for statitics
    orderOfWinners = list()
    amountOfPlayers = len(playerList)
    wins = list()
    mostPlayedColor = list()
    mostPlusCards = list()
    mostSkipCards = list()
    mostReverseCards = list()
    mostTimesGrabbedFromPile = list()
    mostTimesBullied = list()
    mostTimesGrabbedACardInsteadOfPlaying = list()
    startTime = str(datetime.now())
    for x in range(len(cardColors)):
        mostPlayedColor.append(0)
    for x in range(len(playerList)):
        mostPlusCards.append(0)
        mostSkipCards.append(0)
        mostReverseCards.append(0)
    

    extra = []
    showStats = False

    while win[0] == False:
        turn += 1
        activePlayer += playerDirection#for the next turn, also controls skips and reverse
        while activePlayer < 0 or activePlayer >= len(playerList):
            if activePlayer > len(playerList)-1:
                activePlayer -= len(playerList)
            elif activePlayer < 0:
                activePlayer += len(playerList)
        if playerDirection > 0:
            playerDirection = 1
        else:
            playerDirection = -1
        if playerList[activePlayer].type == 1:
            cards, playedCards, playerList, settings, playerDirection, win, playedPlusCards, extra = playerTurn(playerList[activePlayer], cardDeck, playedCardsPile, playerList, setting, playerDirection, activePlayer, win, playedPlusCards, turn)
        else:
            cards, playedCards, playerList, settings, playerDirection, win, playedPlusCards = aiTurn(playerList[activePlayer], cardDeck, playedCardsPile, playerList, setting, playerDirection, activePlayer, win, playedPlusCards, turn)
        if extra != []:
            cardTypes,cardTypesNames,cardColors,yellowGreenColorblindCardColorsNames,blueRedColorblindCardColorsNames,colorblindCardColorsNames,cardColorsNames,specials,specialsNames,mostPlayedColor, mostPlusCards, mostSkipCards, mostReverseCards, mostTimesGrabbedFromPile, mostTimesBullied, mostTimesGrabbedACardInsteadOfPlaying, orderOfWinners, wins, playerListEndOfGame, historyPlayersThatPlayedACard, historyOfCards = extra
            extra = []
        if playedCards[len(playedCards)-1].split(".")[1] == "12" and historyOfCards[len(historyOfCards)-1] != "nothing, he grabbed a card" and historyOfCards[len(historyOfCards)-1] != "nothing, he disconnected":#check for reverse card
            playerDirection = playerDirection * -1
            mostReverseCards[playerList[activePlayer].number] += 1
        elif playedCards[len(playedCards)-1].split(".")[1] == "10" and historyOfCards[len(historyOfCards)-1] != "nothing, he grabbed a card" and historyOfCards[len(historyOfCards)-1] != "nothing, he disconnected":#check for skip card
            playerDirection = playerDirection * 2
            mostSkipCards[playerList[activePlayer].number] += 1
        elif checkForPlus(playedCards[len(playedCards)-1]) == True:
            mostPlusCards[playerList[activePlayer].number] += 1

    


        if win[0] != False:
            print(f"player {playerList[activePlayer].number + 1}, {playerList[activePlayer].name} has 0 cards left, Congrats!!")
            loop7 = True
            wins.append([turn, f"{playerList[activePlayer].number}, {playerList[activePlayer].name}"])
            if len(playerList) > 2 and answer == 0:
                while loop7 == True:
                    answer = input("do you want to continue with the other people? Y/N")
                    if answer.lower() == "y":
                        orderOfWinners.append(f"{playerList[activePlayer].number}, {playerList[activePlayer].name}")
                        playerList.pop(activePlayer)
                        win[0] = False
                        loop7 = False
                    if answer.lower() == "n":
                        win[0] = True
                        loop7 = False
                        showStats = True
            elif len(playerList) > 2:
                orderOfWinners.append(f"{playerList[activePlayer].number}, {playerList[activePlayer].name}")
                playerList.pop(activePlayer)
                win[0] = False
            elif answer != 0:
                print("\n------Results-----\n")
                for i in range(len(orderOfWinners)):
                    try:
                        print(f'player {orderOfWinners[i]} has finished at place nr {i+1}')
                    except Exception as e:
                        print(e)
                averageTurnsToWin = 0
                for z in range(len(wins)):
                    try:
                        averageTurnsToWin += wins[z][0]
                    except Exception as e:
                        print(e)
                mostTimesGrabbedFromPile, mostTimesBullied, mostTimesGrabbedACardInsteadOfPlaying = classDataToLists(mostTimesGrabbedFromPile, mostTimesBullied, mostTimesGrabbedACardInsteadOfPlaying)
                print(f"\n------Results-----\n\n\n-----Stats-----\nIt took {wins[0][0]} turns for the first player ({wins[0][1]}) to finish\nIt took {turn} turns for the last player ({wins[len(wins)-1][1]}) to finish")
                statsCalculationForMultipleFinishers(mostPlusCards, "plus cards")
                statsCalculationForMultipleFinishers(mostSkipCards, "skip cards")
                statsCalculationForMultipleFinishers(mostReverseCards, "reverse cards")
                statsCalculationForMultipleFinishers(mostTimesBullied, "times being bullied")
                statsCalculationForMultipleFinishers(mostTimesGrabbedACardInsteadOfPlaying, "times grabbing a card instead of playing a card")
                statsCalculationForMultipleFinishers(mostTimesGrabbedFromPile, "cards grabbed from the card pile")
                try:
                    averageTurnsToWin = round(averageTurnsToWin / len(wins))
                    print(f"The average turns needed to win: {averageTurnsToWin}")
                except Exception as e:
                    print(e)
                print(f"The game started at {startTime}, it finished at {datetime.now()}")
                print("-----Stats-----")
    if showStats == True:
        mostTimesGrabbedFromPile, mostTimesBullied, mostTimesGrabbedACardInsteadOfPlaying = classDataToLists(mostTimesGrabbedFromPile, mostTimesBullied, mostTimesGrabbedACardInsteadOfPlaying)
        print(f'\n-----Stats-----\nIt took {wins[0][0]} turns to finish')
        statsCalculationForMultipleFinishers(mostPlusCards, "plus cards")
        statsCalculationForMultipleFinishers(mostSkipCards, "skip cards")
        statsCalculationForMultipleFinishers(mostReverseCards, "reverse cards")
        statsCalculationForMultipleFinishers(mostTimesBullied, "times being bullied")
        statsCalculationForMultipleFinishers(mostTimesGrabbedACardInsteadOfPlaying, "times grabbing a card instead of playing a card")
        statsCalculationForMultipleFinishers(mostTimesGrabbedFromPile, "cards grabbed from the card pile")
        print(f"The game started at {startTime}, it finished at {datetime.now()}")
        print("-----Stats-----")

    input("\nPress Enter To Close..")
except Exception as e:
    print(f"seed: {setting[0]}")
    input(e)

print()
kaas = input()