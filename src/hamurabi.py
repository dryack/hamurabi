#The MIT License (MIT)
#
#Copyright (c) 2013-2018 David Ryack
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


# Hamurabi in Python

import random
import os
import sys
import inspect


#since all player input in the game should either be a \r or a positive number
#this function wraps raw_input and only returns a value if the input
#meets the above criteria.
#otherwise it will print a brief message and call itself again
def get_input(prompt):
        input = raw_input(prompt)
        if ((input.isdigit() is True) and (int(input) >= 0)) or (input == ""):
                return input
        else:
                print "Try again Hamurabi!"
                return get_input(prompt)


def test_get_input(prompt):
        print prompt
        # checkInpFrame is in place to keep line length under control,
        # otherwise it isn't really needed.
        checkInpFrame = '["                        inp = get_input(\'How man\
        y acres do you wish to sell => \')\n"]'
        # peeking at sumer method which has called this func
        frame_c = inspect.stack()[1][3]

        # peeking at source code context -
        # in order to use prompt for selling acres
        frame_s = inspect.stack()[1][4]

        if frame_c == 'main':
            return str(100)     # request 100 turn game
        else:
            # peeking at variables within sumer
            frame_v = inspect.stack()[2][0]
            bush = frame_v.f_locals['sumer'].bushels
            pop = frame_v.f_locals['sumer'].population
            acre = frame_v.f_locals['sumer'].acres

            if frame_c == 'get_acres':
                #check and see if we're selling
                if frame_s == checkInpFrame:
                    if bush <= (pop * 11) + acre:
                        return str(acre / 7)
                    elif bush <= (pop * 8) + acre:
                        return str(acre / 5)
                    elif (acre / pop) > 15:
                        return str(acre / 10)
                    else:
                        return str(1)
                else:       # we're buying
                    if bush >= (pop * 30) + acre:
                        #return str(random.randint(50, 200))
                        return str(0)
                    elif bush >= (pop * 20) + acre:
                        #return str(random.randint(25,50))
                        return str(0)
                    elif bush >= (pop * 15) + acre:
                        if (acre / pop) < 8:
                            #return str(random.randint(1, 25))
                            return str(0)
                        else:
                            return str(0)
                    else:
                        return str(0)
            elif frame_c == 'feed_people':
                max_feed = bush - acre      # set aside bushels for planting
                if bush >= acre:
                    #if bumper crop, feed almost everyone
                    if max_feed >= 40 * pop:
                        return str(18 * pop)
                    elif max_feed >= (15 * pop):
                        return str(13 * pop)
                    else:
                        return str(max_feed)

                else:
                    return str(max_feed + (bush / random.randint(5, 15)))

            elif frame_c == 'plant_fields':
                max_plant = 10 * pop
                if bush >= max_plant and bush >= acre:
                    if acre > max_plant:
                        return str(max_plant)
                    else:
                        return str(acre)
                elif bush >= max_plant and bush <= acre:
                    return str(max_plant)
                elif bush <= max_plant and bush >= acre:
                    return str(acre)
                else:
                    return str(bush)

            else:
                print "REACHED UNEXPECTED STACK FRAME: %s" % frame_c


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
                self.tradeval = 0
                self.avg_starved = 0
                self.totaldied = 0
                self.fed = 100
                self.planted = 0
                self.died = 0
                self.print_year_end()

        def check_for_plague(self):
                #check for plague
                if (self.year > 0) and (random.randint(0, 15) == 0):
                        print "A horrible plague has struck!  Many have died!"
                        #calculate losses
                        self.died = self.population/(random.randint(0, 4)+2)
                        self.population -= self.died
                        self.totaldied += self.died

        def print_year_end(self):
                if self.year > 0:
                        self.do_numbers()

                #set this year's tradevalue
                self.tradeval = 17+random.randint(0, 10)
                print "\nMy lord in the year " + str(self.year) + \
                    " I beg to report to you that"
                print str(self.starved) + " people starved, and " + \
                    str(self.migrated) + " came to the city."
                self.check_for_plague()
                print "Population is now " + str(self.population) + "."
                print "The city now owns " + str(self.acres) + \
                    " acres of land."
                print "You have harvested " + str(self.byield) + \
                    " bushels per acre."
                print "Rats ate " + str(self.pests) + " bushels of grain."
                print "We now have " + str(self.bushels) + " in store."
                print "Land is trading at " + str(self.tradeval) + \
                    " bushels per acre.\n"
                self.year += 1

        def get_acres(self):
                #comment out for regular play, test_get_input sets a
                #very rudimentary AI to play the game
                get_input = test_get_input

                inp = get_input('How many acres do you wish to buy => ')
                #player doesn't want to buy
                if (inp == "") or (int(inp) == 0):
                        inp = get_input(
                            'How many acres do you wish to sell => ')
                        if (inp == "") or (int(inp) == 0):
                                return True     # neither buying nor selling
                        else:
                                if int(inp) > self.acres:
                                        print "Think again Hamurabi, you only \
                                            have " + str(self.acres) + \
                                            " acres to sell!"
                                        #tried to sell more than
                                        #currently owned
                                        return False
                                else:
                                        #reduce acres by number sold
                                        self.acres -= int(inp)
                                        #increase bushels based on num acres
                                        #sold
                                        self.bushels += int(inp)*self.tradeval
                                        return True
                else:
                        if int(inp)*self.tradeval > self.bushels:
                                print "Think again Hamurabi, you only have " \
                                    + str(self.bushels) + \
                                    " bushels to use for purchase!"
                                #tried to buy more than can be afforded
                                return False
                        else:
                                #increase acres by num purchased
                                self.acres += int(inp)
                                #reduce bushels based on purchased acres
                                self.bushels -= int(inp)*self.tradeval
                                return True

        def feed_people(self):
                #comment out for regular play, test_get_input sets a
                #very rudimentary AI to play the game
                get_input = test_get_input

                print "This year you will require " + str(self.population*20) \
                    + " bushels to avoid starving anyone."
                inp = get_input(
                    'How many bushels do you wish to release to your people? \
                    => ')
                if inp == "":
                        return False    # player didn't enter anything
                else:
                        if int(inp) > self.bushels:
                                print "Think again Hamurabi, you only have " \
                                    + str(self.bushels) + " available!"
                                return False
                        else:
                                self.bushels -= int(inp)
                                self.fed = int(inp)/20
                                return True

        def plant_fields(self):
                #comment out for regular play, test_get_input sets a
                #very rudimentary AI to play the game
                get_input = test_get_input

                inp = get_input('How many fields will you plant => ')
                if inp == "":
                        return False    # player didn't enter anything
                else:
                        if int(inp) > self.bushels:
                                print "Think again Hamurabi, you only have " \
                                    + str(self.bushels) + \
                                    " bushels available!"
                                return False
                        #people can only plant 10 acres each
                        elif int(inp) > self.population * 10:
                                print "Think again Hamurabi, you only have " \
                                    + str(self.population) + \
                                    " people to plant the fields!"
                                return False
                        elif int(inp) > self.acres:
                                print "Think again Hamurabi, you only have " \
                                    + str(self.acres) + " acres to plant!"
                                return False
                        else:
                                self.bushels -= int(inp)
                                self.planted = int(inp)
                                return True

        def check_for_overthrow(self):
                if self.starved > int(0.45 * self.population):
                        print "\nYou starved starved " + str(self.starved) + \
                            " out of a population of only " + \
                            str(self.population) + ","
                        print "this has caused you to be deposed by force!\n"
                        self.totaldied += self.starved
                        self.print_end_reign()
                        sys.exit(0)   # end game due to starvation

        def do_numbers(self):
                #set bushel yield per acre for the year
                self.byield = random.randint(1, 10)

                self.starved = self.population - self.fed
                if self.starved < 0:
                        self.starved = 0
                self.avg_starved += int(
                    (float(self.starved)/float(self.population))*100)
                self.births = int(self.population / random.randint(2, 10))
                self.population += self.births
                self.check_for_overthrow()
                self.avg_starved += int(
                    (float(self.starved)/float(self.population))*100)
                self.population -= self.starved     # children can die
                self.migrated = int(0.1 * random.randint(1, self.population))
                self.population += self.migrated    # but immigrants don't

                self.pests = int(self.bushels / random.randint(1, 5)+2)
                self.bushels += self.planted * self.byield
                self.bushels -= self.pests
                if self.bushels < 0:
                        self.bushels = 0

                self.totaldied += self.starved

        def print_end_reign(self):
                print "In your " + str(self.year) + " year term of office " \
                    + str(int(self.avg_starved/self.year)) + " percent of"
                print "population starved per year on average.  A total"
                print "of " + str(self.totaldied) + \
                    " people died during your term."
                print "The city began with 10 acres per person and ended with"
                print str(self.acres/self.population) + " acres per person."

                if int(self.avg_starved / self.year) > 33:
                        print "Due to this extreme mismanagement you \
                            have not only"
                        print "been impeached and thrown out of office, \
                            but you have"
                        print "also been declared 'National Fink'!!\n"

                elif int(self.avg_starved / self.year) > 10:
                        print "Your heavy handed performance smacks \
                            of Nero and Ivan IV."
                        print "The people remaining find you an \
                            unpleasant ruler, and"
                        print "frankly, hate your guts!\n"
                else:
                        print "Your performance could have been somewhat \
                            better, but"
                        print "really wasn't too bad at all."
                        print str(random.randint(1, self.population)) + \
                            " people would dearly like to see you \
                            assassinated,"
                        print "but we all have our trivial problems.\n"

                print "<<-----------<END>----------->>"


def main():
        os.system('clear')      # clear screen

        #comment out for regular play, test_get_input sets a
        #very rudimentary AI to play the game
        get_input = test_get_input

        gameturns = get_input('How many years would you like to play? => ')
        if (gameturns == '') or (int(gameturns) <= 0):
                gameturns = 10
        sumer = CityState(int(gameturns))

        while int(gameturns) > 0:

                tmp = False
                while tmp is False:
                        tmp = sumer.get_acres()

                tmp = False
                while tmp is False:
                        tmp = sumer.feed_people()

                tmp = False
                while tmp is False:
                        tmp = sumer.plant_fields()

                gameturns = int(gameturns) - 1
                sumer.print_year_end()

        sumer.print_end_reign()

if __name__ == "__main__":
        main()
