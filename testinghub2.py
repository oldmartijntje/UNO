# Load the dictionary back from the pickle file.
import pickle

returned = pickle.load( open( "save.p", "rb" ) )
favorite_color,colorblindNames,computerNameList,specialsNames,specials,cardColorsNames,colorblindCardColorsNames,cardColors, cardTypesNames = returned
print(returned)
print(favorite_color)
# favorite_color is now { "lion": "yellow", "kitty": "red" }