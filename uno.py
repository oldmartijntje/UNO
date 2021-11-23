import os
import pathlib
import random
import time

#settings: seed0, difficulty1, normal cards2, special cards3, player amount4, starting cards5

class player(): #player and computer
    def __init__(self, playerOrComputer, userName, cardsDeck, statusEffects, memory, playerNumber) -> None:
        self.name = userName
        self.cards = cardsDeck
        self.effect = statusEffects
        self.memory = memory
        self.type = playerOrComputer
        self.number = playerNumber


def pleaseFixTheConfigFile(exception = ""):#tells u there is a problem with your config
    input(f"There is a problem with \"{ownPath}/Config.ini\" Go fix it, or Delete it\nPress Enter to close")
    print(exception)
    exit()

#get the programs path
ownPath = pathlib.Path().resolve()

def cardIdToName(ID):#input the card id: 1.6 and turns it into blue 6
    card = ""
    splitted = ID.split(".")
    splitted[0] = int(splitted[0])
    splitted[1] = int(splitted[1])
    if splitted[0] == 4:
        card = f"{specialsNames[splitted[1]]}"
    else:
        card = f'{cardColorsNames[splitted[0]]} {cardTypesNames[splitted[1]]}'
    return card

def clear_console(): # clear the console
    try:
        os.system('cls')
    except:
        try:
            os.system('clear')
        except:
            e = 0

def takeCardFromDeck(amount, card, played):#grab the amount of cards and add it to your deck
    gift = list()
    for x in range(amount):
        if len(card) > 1:
            gift.append(card[0])
            print(f"you have grabbed a {cardIdToName(card[0])}")
            card.pop(0)
        else:#add the played pile to the new cards
            placeholderList = list()
            for y in range(1, len(played)):
                placeholderList.append(played[y])
            random.shuffle(placeholderList)
            card.append(placeholderList)

            gift.append(card[0])
            print(f"you have grabbed a {cardIdToName(card[0])}")
            card.pop(0)
            
    return gift, card, played

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
    "\n#choose the amount of starting cards (might break if no cards are left) (7 by default)\n7")
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
            settings[0] = False
        else:
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
        if settings[4] > 9*settings[2] or settings[4] < 1:
            settings[4] = 1

        settings.append(int(rawSettings[5])) #set amount of computer players
        if settings[5] + settings[4] > 9*settings[2] or settings[4] + settings[4] < 2:
            settings[5] = 3

        print(rawSettings)

        settings.append(rawSettings[6])
        if rawSettings[6] == "False":#check if they want names
            settings[6] = False
        else:
            settings[6] = True

        settings.append(int(rawSettings[7])) #set amount of starting cards


        return settings
    except Exception as e:
        print(settings)
        pleaseFixTheConfigFile(e)

def chooseCard(player, cards, playedCards, playerList, settings, playingDirection, activePlayer, win):
    lastPlayedCard = cardIdToName(playedCards[len(playedCards)-1])
    print(f"The last player played {lastPlayedCard}")
    cardsInDeckString = ""
    for x in range(len(player.cards)):#show all your cards
        cardsInDeckString += "| " + f"{x+1}."+cardIdToName(player.cards[x])+" | "
    print(f"what card do you want to play? (say 0 to grab a card from the pile)\n{cardsInDeckString}")
    loop = True
    while loop == True:
        try:
            numberCard = int(input())
            if numberCard > -1 and numberCard <= len(player.cards):#if he chose an existing card
                if numberCard == 0:
                    if (playedCards[len(playedCards)-1].split(".")[0] == "4" and playedCards[len(playedCards)-1].split(".")[1] == "1") or (playedCards[len(playedCards)-1].split(".")[1] == "11" and playedCards[len(playedCards)-1].split(".")[0] != "4"):
                        win.append("+")
                    cardsForPlayer, cards, playedCards = (takeCardFromDeck(1, cards, playedCards))#grab a card
                    for x in range(len(cardsForPlayer)):
                        player.cards.append(cardsForPlayer[x])
                    loop = False
                else: #play the card
                    numberCard -= 1
                    splittedCard = player.cards[numberCard].split(".")
                    splittedLastCard = playedCards[len(playedCards)-1].split(".")
                    if splittedCard[0] != "4" and splittedLastCard[0] != "4": #check for wild or +4 card
                        if splittedCard[0] == splittedLastCard[0] or splittedCard[1] == splittedLastCard[1]:
                            playedCards.append(player.cards[numberCard])
                            if player.cards[numberCard].split(".")[1] == "12":#check for reverse card
                                playingDirection = playingDirection * -1
                            elif player.cards[numberCard].split(".")[1] == "10":#check for skip card
                                playingDirection = playingDirection * 2
                            player.cards.pop(numberCard)
                            loop = False
                            if len(player.cards) == 0:#check if someone has won
                                win[0] = True
                        
                        else:#it is not a available card
                            print("you can't play that card right now")
                    else:# play the wild or +4 card
                        playedCards.append(player.cards[numberCard])
                        player.cards.pop(numberCard)
                        loop = False
            else:
                print("you don't have a card in that slot")
        except Exception as e:
            print(e)
            print("try inputting a number")
    return player, playedCards, playingDirection, win

def stringToSeed(string): #turns everything into ther ASCII value
    seedList = []
    for x in string:
        seedList.append(ord(x))#change every character into its ASCII value
    seedString = ''.join([str(elem) for elem in seedList])#add list together into string
    seed = int(seedString)
    return seed

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

def playerTurn(player, cards, playedCards, playerList, settings, playingDirection, activePlayer, win):
    if playingDirection > 0:
        playingDirection = 1
    else:
        playingDirection = -1
    stackedPlusCards = 0

    lastPlayedCard = cardIdToName(playedCards[len(playedCards)-1])
    if settings[4] > 1: #only if it's not singleplayer
        clear_console()
        input(f"it's player number {player.number+1}, {player.name} their turn\nPress the enter button to play\n")
    lastPlayedCardID = playedCards[len(playedCards)-1]
    if len(win) != 1:
        while len(win) != 1:
            win.pop(1)
    else:
        if lastPlayedCardID.split(".")[0] == '4' and lastPlayedCardID.split(".")[1] == '1':#check if it is a +4 card
            stackedPlusCards += 4
            print(f"The last player played {lastPlayedCard}")
        elif lastPlayedCardID.split(".")[1] == '11':#check if it is a +2 card
            stackedPlusCards += 2
            print(f"The last player played {lastPlayedCard}")
    if stackedPlusCards > 0:#if it was a + card, check how many of them are stacked
        check = 1
        for x in range(2, len(playedCards)):
            if check == 1:
                if playedCards[len(playedCards)- x].split(".")[0] == '4' and playedCards[len(playedCards)-x].split(".")[1] == '1':#check if it is a +4 card
                    stackedPlusCards += 4
                elif playedCards[len(playedCards)-x].split(".")[1] == '11':#check if it is a +2 card
                    stackedPlusCards += 2
                else:
                    check = 0
    yourAmountPlusCards = [0, 0]
    if stackedPlusCards > 0:
        for x in range(len(player.cards)): #check if you have any + card to counter
            if player.cards[x].split(".")[0] == '4' and player.cards[x].split(".")[1] == '1':
                yourAmountPlusCards[1] += 1
            elif player.cards[x].split(".")[1] == '11':
                yourAmountPlusCards[0] += 1
        if yourAmountPlusCards[0] + yourAmountPlusCards[1] == 0: #if you have no cards to counter the + card, automatically get the cards
            cardsForPlayer, cards, playedCards = (takeCardFromDeck(stackedPlusCards, cards, playedCards))
            for x in range(len(cardsForPlayer)):
                player.cards.append(cardsForPlayer[x])
            player, playedCards, playingDirection, win = chooseCard(player, cards, playedCards, playerList, settings, playingDirection, activePlayer)
        else:
            cardsInDeckString = ""
            for x in range(len(player.cards)):#show all your cards
                cardsInDeckString += "| " + f"{x+1}."+cardIdToName(player.cards[x])+" | "
            print(f"what card do you want to play? (say 0 to grab the cards from the pile)\n{cardsInDeckString}")
            loop = True
            while loop == True:
                try:
                    numberCard = int(input())
                    if numberCard > -1 and numberCard <= len(player.cards ):#check if it's a card you have
                        if numberCard == 0:
                            if (playedCards[len(playedCards)-1].split(".")[0] == "4" and playedCards[len(playedCards)-1].split(".")[1] == "1") or (playedCards[len(playedCards)-1].split(".")[1] == "11" and playedCards[len(playedCards)-1].split(".")[0] != "4"):
                                win.append("+")
                            cardsForPlayer, cards, playedCards = (takeCardFromDeck(stackedPlusCards + 1, cards, playedCards))
                            for x in range(len(cardsForPlayer)):
                                player.cards.append(cardsForPlayer[x])
                            loop = False
                        else:
                            numberCard -= 1
                            if player.cards[numberCard].split(".")[0] == '4' and player.cards[numberCard].split(".")[1] == '1':#check if it is a +4 card
                                playedCards.append(player.cards[numberCard])
                                player.cards.pop(numberCard)
                                loop = False
                            elif player.cards[numberCard].split(".")[1] == '11':#check if it is a +2 card
                                playedCards.append(player.cards[numberCard])
                                player.cards.pop(numberCard)
                                loop = False
                            else:
                                print("\nthe last player played a + card so we will grab your cards first, then you can choose which one to play\n")#get cards
                                time.sleep(3)
                                cardsForPlayer, cards, playedCards = (takeCardFromDeck(stackedPlusCards, cards, playedCards))
                                for x in range(len(cardsForPlayer)):
                                    player.cards.append(cardsForPlayer[x])
                                player, playedCards, playingDirection, win = chooseCard(player, cards, playedCards, playerList, settings, playingDirection, activePlayer)
                                loop = False
                    else:
                        print("that is not a card you have")
                except Exception as e:
                    print("try a number")
                    print(e)
    else:
        player, playedCards, playingDirection, win = chooseCard(player, cards, playedCards, playerList, settings, playingDirection, activePlayer, win)
    input(f"that was your turn {player.name}\npress enter so the next player can play\n")
    return cards, playedCards, playerList, settings, playingDirection, activePlayer, win
                
                           

#config thingys
createConfig(ownPath)
setting = rawSettingsToSettings(readConfig())
if setting[0] != False: random.seed(setting[0])#set seed if seed in config


#basic settings
cardTypes = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12]#1 deck of color cards per color
#all types of cards with a color 0-9 numbers, 10 skip, 11 +2, 12 reverse
cardTypesNames = ["zero", 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'skip', 'draw two', 'reverse']
cardColors = [0, 1, 2, 3, 4]#all colors, special, red, blue, green, yellow
cardColorsNames = ["red", 'blue', 'green', 'yellow', 'black']
specials = [0, 1]#the special cards, wild, draw 4
specialsNames = ["wild", 'draw four']
computerNameList = ['thomas', 'muik', 'coen', 'staninna', 'stijn', 'florida man', 'mandrex', 'bob', 'grian', 'mumbo jumbo', 'scar', '[CLASSEFIED]', 'george',
'lianne', 'tommy', 'tiffany', 'katie', 'jase', 'lennert', 'mellodie', 'mark rutte', 'Master of scares', 'Null', 'Herobrine', 'None', 'Undefined', 'liam', 'anne', 'colorblind guy', 'sexy buurvrouw', 
'Ms.Kittens', 'attack helicopter', 'shell', 'twan', 'david', 'joelia', 'sneal', 'pieter', 'merijn', 'marjin', 'oldmartijntje', 'martijn', 'mercury', 'lara', 'steve jobs', 'mark zuckerburg', 'elon musk', 'sinterklaas', 'bart', 'ewood', 'mathijs', 'joris', 'zwarte piet']
colorblindNames = ['thomas', 'george', 'colorblind guy']

#creating players
playerList = list()
for i in range(setting[4]):
    if setting[6] == True:
        while True:
            playerName = input(f"hello player number {len(playerList)}, what is your name?\n>>>")
            if playerName != "":
                playerList.append(player(1, playerName, [], "", [], len(playerList)))
                if playerList[i].name.lower() in colorblindNames:
                    playerList[i].effect = "colorblind"
                break
    else:
        playerList.append(player(1, computerNameList[random.randint(0, len(computerNameList)-1)], [], "", [], len(playerList)))
        if playerList[i].name.lower() in colorblindNames:
            playerList[i].effect = "colorblind"
    

for i in range(setting[5]):
    if setting[1] != "Exercise":
        if random.randint(0, 100) == 5:
            playerList.append(player(0, computerNameList[random.randint(0, len(computerNameList)-1)], [], "colorblind", [], len(playerList)))
        else:
            playerList.append(player(0, computerNameList[random.randint(0, len(computerNameList)-1)], [], "", [], len(playerList)))
        if playerList[i].name.lower() in colorblindNames.lower():
            playerList[i].effect = "colorblind"
    else:
        playerList.append(player(0, computerNameList[random.randint(0, len(computerNameList)-1)], [], "", [], len(playerList)))

#creating a game
cardDeck = setupCardPile(cardColors, cardTypes, specials, setting)
playedCardsPile = [cardDeck[0]]#start card
cardDeck.pop(0)#remove start card from cards list
playerDirection = 1
playerList, cardDeck = givePeoplePlayingCards(playerList, cardDeck, setting)
activePlayer = random.randint(0, len(playerList)-1)

#the infinite loop which is called a game

win = [False]
while win[0] == False:
    activePlayer += playerDirection#for the next turn, also controls skips and reverse
    if activePlayer > len(playerList)-1:
        activePlayer -= len(playerList)
    elif activePlayer < 0:
        activePlayer += len(playerList)
    if playerList[activePlayer].type == 1:
        cards, playedCards, playerList, settings, playerDirection, activePlayer, win = playerTurn(playerList[activePlayer], cardDeck, playedCardsPile, playerList, setting, playerDirection, activePlayer, win)
    else:
        pass
