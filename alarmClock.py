# -*- coding: utf-8 -*-

import os
import sys
import time
import urllib2
from mpd import MPDClient
from xml.etree import ElementTree as tree

#---------------------
# Global variables:
#---------------------

global_debug = False

tracklist = "spotify:track:1DzQvaFztN7CnbqcXOO5k0"
lightTiming = [
    (6,100),
    (4,255)
    ]



#---------------------
# Classes:
#---------------------

#a artificall intelligence
class ai:

	def __init__(self, name):
		self.name     = name
		self.voice    = "Fred"
	
	
	def say(self, text):
		print self.name + ': ' + text
		os.system('say "' + str(text) + '" -v "' + str(self.voice) + '"')


	def parse(self, phrase):
		phrase  = phrase.lower().split(' ')
		command = phrase[0]
		args    = phrase[1:]
		
		if command == "lamps":
			self.lamps(args)
		elif command == "quit" or command == "exit" or command == "bye":
			self.shutdown()
		elif command == "alarm":
			self.set_alarm(args)
		elif command == "hi" or command == "hello":
			self.say("Hello!")
		elif command == "status":
			self.say("I am up and running, no known problems.")
		else:
			self.say("Unknown command.")
		
	
	def set_alarm(self, args):
		try:
			alarmtime = args[0]
			t      = alarmtime.split(':')
			hour   = int(t[0])
			minute = int(t[1])
		except:
			self.say("Please enter a time for the alarm")
			return
			
		self.say("I have set an alarm for " + alarmtime + ". Good night!")
				
		#alarm waiting time
		while True:
			now = list(time.localtime())
			h   = now[3]
			m   = now[4]

			# break on esc
			#if sys.stdin.read(1) is "t":
			#    break
			#if sys.stdin.read(1) != None:
			#    self.say("Aborting the alarm")
			#    return

			if hour == h and minute == m:
				break
			else:
				time.sleep(20)
		
		#alarm execution
		client = MPDClient()
		client.connect("localhost", 6600)
		client.setvol(100)
		client.clear()
		client.add(tracklist)
		client.play()
		client.disconnect()
		
		for tup in lightTiming:
		    time.sleep(tup[0])
            	    self.lamps([tup[1]])
        
		raw_input("press 'enter' to end the alarm.")
		client = MPDClient()
		client.connect("localhost", 6600)
		client.stop()
		client.disconnect()
		
	def shutdown(self):
		self.say("Good bye!\n\n")
		sys.exit(1)
	
		
	def lamps(self, args):
		
		if args == []:
			self.say("Please specify what you want me to do.")
			return
		
		if args[0] == 'on':
			level = 255
			os.system("tdtool -n 2")
		elif args[0] == 'off':
			level = 0
			os.system("tdtool -f 2")
		else:
			level = args[0]
			os.system("tdtool -v " + str(level) + " -d 2")		
		
		
#---------------------
# Main:
#---------------------

def main():
	
	#Ui	
	print "\n~ ~ Simple room control application. By Viktor Lyresten ~ ~"	
		
	#create ai
	bot = ai("Room Intelligence")
	bot.say("Hello")
	
	#main run
	while True:
		phrase = raw_input(">> ")
		bot.parse(phrase)
	

#only runt main on direct run.
if __name__ == '__main__':
	main()