import pathlib, ast, os

def pluginLoad(cardTypes, cardTypesNames, cardColors, yellowGreenColorblindCardColorsNames, blueRedColorblindCardColorsNames, colorblindCardColorsNames, cardColorsNames, specials, specialsNames):
    ownPath = pathlib.Path().resolve()
    if os.path.isfile(f"{ownPath}/plugin.txt"):
        pluginTXT = open(f"{ownPath}/plugin.ini", "r")
        reading = pluginTXT.read().split('\n')
        for x in range(len(reading)):
            try:
                reading[x] = ast.literal_eval(reading[x])
            except:
                reading[x] = reading[x].strip('][').split(', ')
        cardTypes, cardTypesNames, cardColors, yellowGreenColorblindCardColorsNames, blueRedColorblindCardColorsNames, colorblindCardColorsNames, cardColorsNames, specials, specialsNames = reading
    return cardTypes, cardTypesNames, cardColors, yellowGreenColorblindCardColorsNames, blueRedColorblindCardColorsNames, colorblindCardColorsNames, cardColorsNames, specials, specialsNames

