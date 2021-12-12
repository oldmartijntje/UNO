# Save a dictionary into a pickle file.
import pickle

cardTypesNames = ["zero", 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'skip', 'draw two', 'reverse']
cardColors = [0, 1, 2, 3, 4]#all colors, special, red, blue, green, yellow
colorblindCardColorsNames = ["a color", 'a color', 'a color', 'a color', 'black']
cardColorsNames = ["red", 'blue', 'green', 'yellow', 'black']
specials = [0, 1]#the special cards, wild, draw 4
specialsNames = ["wild", 'draw four']
computerNameList = ['thomas', 'thom', 'muik', 'coen', 'staninna', 'stijn', 'florida man', 'mandrex', 'bob', 'grian', 'mumbo jumbo', 'scar', '[CLASSEFIED]', 'george',
'lianne', 'tommy', 'tiffany', 'katie', 'jase', 'lennert', 'mellodie', 'mark rutte', 'Master of scares', 'Null', 'Herobrine', 'None', 'Undefined', 'liam', 'anne', 'colorblind guy', 
'Ms.Kittens', 'attack helicopter', 'mr Blue Sky','joe', 'kaas', 'peter quill','Nat','Loki','Nick Fury','Vision', 'Eather', 'Mind Stone', 'Power Stone','Tesseract','Wanda', 'Soul Stone', 'Time Stone',
'Dr Strange','Coulson', 'Banner','Peter Parker','Tony Stark', 'Scott Lang','pjotter', 'Thanos', 'Thor', 'GLaDOS', 'chell', 'Phileine', 'emiel', 'twan', 'david', 'joelia', 'sneal', 'pieter', 'merijn', 'marjin',
'oldmartijntje', 'martijn', 'mercury', 'lara', 'steve jobs', 'mark zuckerburg', 'elon musk', 'sinterklaas', 'bart', 'ewood', 'mathijs', 'joris', 'zwarte piet','Gamora','Why Is Gamora?','I Am Groot','Rocket Raccoon','KORG',
'Nebula' ,'Drax','Hugo de Jonge','thierry baudet','Jesse Klaver','Agent Carter','Misterio','Captain Marvel','Odin','Stan Lee','Fits', 'Hawk Eye','Sky','Black Panther','Jemma Simmons', '', 'Quick silver','Wolverine', 'Deadpool','Flash','SuperMan','Batman','Mantis']
colorblindNames = ['thomas', 'george', 'colorblind guy','thierry baudet']
favorite_color = { "lion": "yellow", "kitty": "red" }

allInAList = [favorite_color,colorblindNames,computerNameList,specialsNames,specials,cardColorsNames,colorblindCardColorsNames,cardColors, cardTypesNames]
pickle.dump( allInAList, open( "save.p", "wb" ) )
