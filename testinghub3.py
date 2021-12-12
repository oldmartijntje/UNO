import pickle
yeet = [True, False]
yeetus = yeet
yeetus[0] = False
print(yeet)
pickle.dump([yeet, yeetus],open( "test.e", "wb"))