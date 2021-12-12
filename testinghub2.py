# Load the dictionary back from the pickle file.
import pickle

favorite_color = pickle.load( open( "save.p", "rb" ) )
print(favorite_color)
# favorite_color is now { "lion": "yellow", "kitty": "red" }