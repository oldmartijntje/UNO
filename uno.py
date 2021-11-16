import os
import pathlib
import random

#get the programs path
ownPath = pathlib.Path().resolve()
def createConfig(ownPath):
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
        settings.write("#if you leave empty lines, or with other characters(unless the line starts with #, then it is okay), the program will choose by itself")
        settings.write("\n#\n#\n#BE AWARE THAT \"True\" AND \"False\" NEED TO HAVE THE FIRST LETTER CAPITALIZED\n#\n#")
        settings.write("\n#if you want to use a seed, put it here, else, make it False\nFalse")
        settings.write("\n#choose a gamemode, these are the gamemodes:\n#Easy\n#Normal\n#Impossible\n#Exercise\nExercise")
    settings.close()

def readConfig():
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
            if settingsSplitted[x][0] != "#" and settingsSplitted[x][1] != "#":
                settingsWithoutComments.append(settingsSplitted[x])
        except:
            input(f"There is a problem with \"{ownPath}/Config.ini\" Go fix it, or Delete it\nPress Enter to close")
            exit()
    return settingsWithoutComments

def rawSettingsToSettings(rawSettings):
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
    return settings

def stringToSeed(string):
    seedList = []
    for x in string:
        seedList.append(ord(x))#change every character into its ASCII value
    seedString = ''.join([str(elem) for elem in seedList])#add list together into string
    seed = int(seedString)
    return seed

createConfig(ownPath)
setting = rawSettingsToSettings(readConfig())
if setting[0] != False: random.seed(setting[0])#set seed if seed in config

cardTypes = ["0", '1', '2', '3', '4', '5', '6', '7', '8', '9', 'skip', 'draw two', 'reverse']
cardColors = ["red", 'blue', 'green', 'yellow']