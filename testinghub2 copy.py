import pickle

class Laptop:
	
	def __init__(self, name, processor, hdd, ram, cost):
		self.name = name
		self.processor = processor
		self.hdd = hdd
		self.ram = ram
		self.cost = cost
		
	def details(self):
		print('The details of the laptop are:')
		print('Name         :', self.name)
		print('Processor    :', self.processor)
		print('HDD Capacity :', self.hdd)
		print('RAM          :', self.ram)
		print('Cost($)      :', self.cost)

#read the pickle file
picklefile = open('laptop1', 'rb')
#unpickle the dataframe
laptop1 = pickle.load(picklefile)
#close file
picklefile.close()

#print the dataframe
print(type(laptop1))
laptop1.details()