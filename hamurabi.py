# Hamurabi in Python

import random

population = 95
starved = 0
migrated = 5
bushels = 2800
acres = 1000
byield = 3
pests = 200
tradeval = 17+random.randint(0, 10) #randomly set between 17 and 27 at the beginning of each game
avgstarved = 0
totaldied = 0 #incremented by all deaths due to any cause
fed = 0
planted = 0

class Exitloop(Exception): pass  #for immediate breaking from nested loops

##################################################################################################################
#####	For later consideration... improving flexibility 
###################################################################################################################
#def rats(x): # takes bushels
#	return x/(random.randomint(0, 5)+2)

#def births(x): #takes population

#def buyAcres(x): #takes amount player is attempting to purchase
#	if (x*tradeval) > bushels:
#		short = abs((bushels-(x*tradeval)))
#		print "My lord, you are short " + short + " bushels for purchasing that land!"
#		return FALSE
#	else:
#		acres += x
#		return TRUE
###################################################################################################################

for year in [1,2,3,4,5,6,7,8,9,10]:
	died = 0 #no one has died so far this year
	print "\nMy lord in the year " + str(year) + " I beg to report to you that"
	print str(starved) + " people starved, and " + str(migrated) + " came to the city."
	if (year != 1) and (random.randint(0,15) == 0):  #check for plague
		print "A horrible plague has struck!  Many have died!"
		died = population/(random.randint(0,4)+2) #calculate losses
		population -= died
		totaldied += died

	print "Population is now " + str(population) + "."
	print "The city now owns " + str(acres) + " acres of land."
	print "You have harvested " + str(byield) + " bushels per acre."
	print "Rats ate " + str(pests) + " bushels of grain."
	print "We now have " + str(bushels) + " in store."
	print "Land is trading at " + str(tradeval) + " bushels per acre.\n"
	
	try:	#really just using the try block to allow breaking from nested loops
		while 1:
			inp = raw_input('How many acres do you wish to buy? => ')
			if (inp == "") or (int(inp) == 0):  #player doesn't want to buy
				while 1:
					inp = raw_input('How many acres do you wish to sell => ')
					if (inp == "") or (int(inp) == 0):
						raise Exitloop
					elif int(inp) < 0:  #player is crazy... placeholding for more interesting behavior
						print"\nHamurabi, you have gone mad!"
						raise Exitloop
					else:
						if int(inp) > acres:
							print "Think again Hamurabi, you only have " + str(acres) + " acres to sell!"
							continue  #tried to sell more than currently owned
						else:
							acres -= int(inp)	#reduce acres by number sold
							bushels += int(inp)*tradeval	#increase bushels based on number acres sold
							raise Exitloop
			elif int(inp) < 0:
                                print "\nHamurabi, you have gone mad!"	#player is crazy... placeholding for more interesting behavior
                                raise Exitloop

			else:
				if int(inp)*tradeval > bushels:
					print "Think again Hamurabi, you only have " + str(bushels) + " bushels to use for purchase!"
					continue	#tried to buy more than can be afforded
				else:
					acres += int(inp)	#increase acres by num purchased
					bushels -= int(inp)*tradeval	#reduce bushels based on purchased acres
					raise Exitloop
	except Exitloop:
		pass
	try:
		while 1:
			print "This year you will require " + str(population*20) + " bushels to avoid starving anyone."
			inp = raw_input('How many bushels do you wish to release to your people? => ')
			if inp == "":
				continue #player didn't enter anything
			elif int(inp) < 0:
				print "Hamurabi, you have gone mad!"
				raise Exitloop
			else:
				if int(inp) > bushels:
					print "Think again Hamurabi, you only have " + str(bushels) + " available!"
					continue
				else:
					bushels -= int(inp)
					fed = int(inp)/20
					raise Exitloop
	except Exitloop:
		pass
	try:
		while 1:
			inp = raw_input('How many fields will you plant => ')
			if inp == "":
				continue #player didn't enter anything
			elif int(inp) < 0:
				print "Hamurabi, you have gone mad!"
				raise Exitloop
			else:
				if int(inp) > bushels:
					print "Think again Hamurabi, you only have " + str(bushels) + " available!"
					continue
				elif int(inp) > population * 10: # people can only plant 10 acres each
					print "Think again Hamurabi, you only have " + str(population) + " to plant the fields!"
					continue
				else:
					bushels -= int(inp)
					planted = int(inp)
					raise Exitloop
	except Exitloop:
		pass
	
	starved = abs(fed - int(population))
	if starved < 0:
		starved = 0
	#print str(population) + '\n'
	births = int(population / 2)
	population += births
	population -= starved #children can die
#	x = int(population)
#	print str(population) + '\n'
	migrated =  int(0.1 * random.randint(1, population))
	population += migrated #but immigrants don't
	byield = random.randint(1, 10)
	pests = int(bushels / random.randint(0, 5))+2
	bushels += planted * byield
	bushels -= pests
	print "\n\n"
