#The MIT License (MIT)
#
#Copyright (c) 2013 David Ryack
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
#the Software, and to permit persons to whom the Software is furnished to do so,
#subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
#FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
#IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



# Hamurabi in Python

import random
import os
import sys


#since all player input in the game should either be a \r or a positive number
#this function wraps raw_input and only returns a value if the input
#meets the above criteria.
#otherwise it will print a brief message and call itself again
def get_input(prompt):
	input = raw_input(prompt)
	if ((input.isdigit() == True) and (int(input) >= 0)) or (input == ""):
		return input
	else:
		print "Try again Hamurabi!"
		return get_input(prompt)

class CityState():
	def __init__(self, turns):
		self.turns_tp = turns
		self.year = 0
		self.population = 100
		self.starved = 0
		self.migrated = 0
		self.bushels = 2800
		self.acres = 1000
		self.byield = 3
		self.pests = 200
		self.tradeval =  0
		self.avg_starved = 0
		self.totaldied = 0
		self.fed = 100
		self.planted = 0
		self.died = 0
		self.print_year_end()
		
	def check_for_plague(self):
		if (self.year > 0) and (random.randint(0,15) == 0):  #check for plague
			print "A horrible plague has struck!  Many have died!"
			self.died = self.population/(random.randint(0,4)+2) #calculate losses
			self.population -= self.died
			self.totaldied += self.died
	
	def print_year_end(self):
		if self.year > 0:
			self.do_numbers()
		
		#set this year's tradevalue
		self.tradeval = 17+random.randint(0, 10)
		print "\nMy lord in the year " + str(self.year) + " I beg to report to you that"
		print str(self.starved) + " people starved, and " + str(self.migrated) + " came to the city."
		self.check_for_plague()
		print "Population is now " + str(self.population) + "."
		print "The city now owns " + str(self.acres) + " acres of land."
		print "You have harvested " + str(self.byield) + " bushels per acre."
		print "Rats ate " + str(self.pests) + " bushels of grain."
		print "We now have " + str(self.bushels) + " in store."
		print "Land is trading at " + str(self.tradeval) + " bushels per acre.\n"
		self.year += 1
	
	def get_acres(self, *test):
		
		if test:
			inp = test
		else:
			inp = get_input('How many acres do you wish to buy? => ')
			
		if (inp == "") or (int(inp) == 0):	#player doesn't want to buy
		
			if test:
				inp = test
			else:
				inp = get_input('How many acres do you wish to sell => ')
		
			if (inp == "") or (int(inp) == 0):
				return True	#neither buying nor selling
			else:
				if int(inp) > self.acres:
					print "Think again Hamurabi, you only have " + str(self.acres) + " acres to sell!"
					return False  #tried to sell more than currently owned
				else:
					self.acres -= int(inp)       #reduce acres by number sold
					self.bushels += int(inp)*self.tradeval    #increase bushels based on number acres sold
					return True
		else:
			if int(inp)*self.tradeval > self.bushels:
				print "Think again Hamurabi, you only have " + str(bushels) + " bushels to use for purchase!"
				return False	#tried to buy more than can be afforded
			else:
				self.acres += int(inp)       #increase acres by num purchased
				self.bushels -= int(inp)*self.tradeval    #reduce bushels based on purchased acres
				return True
		
		
	def feed_people(self):
				
		print "This year you will require " + str(self.population*20) + " bushels to avoid starving anyone."
		inp = get_input('How many bushels do you wish to release to your people? => ')
		if inp == "":
			return False #player didn't enter anything
		else:
			if int(inp) > self.bushels:
				print "Think again Hamurabi, you only have " + str(self.bushels) + " available!"
				return False
			else:
				self.bushels -= int(inp)
				self.fed = int(inp)/20
				return True
			
	def plant_fields(self):
		inp = get_input('How many fields will you plant => ')
		if inp == "":
			return False	#player didn't enter anything
		else:
			if int(inp) > self.bushels:
				print "Think again Hamurabi, you only have " + str(self.bushels) + " bushels available!"
				return False
			elif int(inp) > self.population * 10: # people can only plant 10 acres each
				print "Think again Hamurabi, you only have " + str(self.population) + " people to plant the fields!"
				return False
			elif int(inp) > self.acres:
				print "Think again Hamurabi, you only have " + str(self.acres) + " acres to plant!"
				return False
			else:
				self.bushels -= int(inp)
				self.planted = int(inp)
				return True
			
	def check_for_overthrow(self):
		if self.starved > int(0.45 * self.population):
			print "\nYou starved starved " + str(self.starved) + " out of a population of only " + str(self.population) + ","
			print "this has caused you to be deposed by force!\n"
			self.totaldied += self.starved
			self.print_end_reign()
			sys.exit(0)   #end game due to starvation
					
	def do_numbers(self):
		self.byield = random.randint(1, 10)	#set bushel yield per acre for the year
		
		self.starved = self.population - self.fed
		if self.starved < 0:
			self.starved = 0
		self.avg_starved += int((float(self.starved)/float(self.population))*100)
		self.births = int(self.population / random.randint(2, 10))	
		self.population += self.births
		self.check_for_overthrow()
		self.avg_starved += int((float(self.starved)/float(self.population))*100)
		self.population -= self.starved #children can die
		self.migrated =  int(0.1 * random.randint(1, self.population))
		self.population += self.migrated #but immigrants don't
		
		self.pests = int(self.bushels / random.randint(1, 5)+2)
		self.bushels += self.planted * self.byield
		self.bushels -= self.pests
		if self.bushels < 0:
			self.bushels = 0
		
		self.totaldied += self.starved
		
	def print_end_reign(self):
		print "In your " + str(self.year) + " year term of office " + str(int(self.avg_starved/self.year)) + " percent of"
		print "population starved per year on average.  A total"
		print "of " + str(self.totaldied) + " people died during your term."
		print "The city began with 10 acres per person and ended with"
		print str(self.acres/self.population) + " acres per person."
		
		if int(self.avg_starved / self.year) > 33:
			print "Due to this extreme mismanagement you have not only"
			print "been impeached and thrown out of office, but you have"
			print "also been declared 'National Fink'!!\n"
		
		elif int(self.avg_starved / self.year) > 10:
			print "Your heavy handed performance smacks of Nero and Ivan IV."
			print "The people remaining find you an unpleasant ruler, and"
			print "frankly, hate your guts!\n"
		else:
			print "Your performance could have been somewhat better, but"
			print "really wasn't too bad at all."
			print str(random.randint(1, self.population)) + " people would dearly like to see you assassinated,"
			print "but we all have our trivial problems.\n"
			
		print "<<-----------<END>----------->>"
	

def main():
	os.system('clear')	#clear screen
	
	gameturns = get_input('How many years would you like to play? => ')
	if (gameturns == '') or (int(gameturns) <= 0):
		gameturns = 10
	sumer = CityState(int(gameturns))
	
	while int(gameturns) > 0:
		
		tmp = False
		while tmp == False:
			tmp = sumer.get_acres()
	
		tmp = False
		while tmp == False:
			tmp = sumer.feed_people()
		
		tmp = False
		while tmp == False:
			tmp = sumer.plant_fields()
			
		gameturns = int(gameturns) - 1
		sumer.print_year_end()
		
	sumer.print_end_reign()

if __name__ == "__main__":
    main()