#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import sys
from socket import *
from optparse import OptionParser

## Create variables
repeat = None
group = None
brightness = None

## Define options
opts = OptionParser()
usage = "usage: %prog [options] [inputs]"
opts = OptionParser(usage=usage)
opts.add_option("-i", "--ip", action="store", dest="ip", default="127.0.0.1", help="Wifi Bridge IP [default: %default]")
opts.add_option("-p", "--port", action="store", type="int", dest="port", default="8899", help="Wifi Bridge port [default: %default]")
opts.add_option("-g", "--group", action="store", dest="group", help="Light group: 0 (for all), 1, 2, 3 or 4")
opts.add_option("-c", "--command", action="store", dest="command", help="Commmand such as a color (white, red, etc...) or special mode (on, off, disco, slower, faster)")
opts.add_option("-b", "--brightness", action="store", dest="brightness", help="Brightness level (integer number: minimum 0 to maximum 25)")
options, arguments = opts.parse_args()

## Set socket parameters
addr = (options.ip,options.port)

## Commands & Groups
alloff = '\x41\x00\x55'     #Group ALL OFF
allon = '\x42\x00\x55'      #Group ALL ON
slower = '\x43\x00\x55' 	#Disco speed SLOWER
faster = '\x44\x00\x55'  	#Disco speed FASTER
oneon = '\x45\x00\x55'      #Group 1 ON
oneoff = '\x46\x00\x55'     #Group 1 OFF
twoon = '\x47\x00\x55'      #Group 2 ON
twooff = '\x48\x00\x55'     #Group 2 OFF
threeon = '\x49\x00\x55'    #Group 3 ON
threeoff = '\x4A\x00\x55'   #Group 3 OFF
fouron = '\x4B\x00\x55'     #Group 4 ON
fouroff = '\x4C\x00\x55'    #Group 4 OFF
disco = '\x4D\x00\x55'  	#Next "Disco mode"
allwhite = '\xC2\x00\x55'   #Groupe ALL WHITE
onewhite = '\xC5\x00\x55'   #Groupe 1 WHITE
twowhite = '\xC7\x00\x55'   #Groupe 2 WHITE
threewhite = '\xC9\x00\x55' #Groupe 3 WHITE
fourwhite = '\xCB\x00\x55'  #Groupe 4 WHITE

## Colors
blue = '\x40\x00\x55'
aqua = '\x40\x20\x55'
cyan = '\x40\x40\x55'
mint = '\x40\x50\x55'
green = '\x40\x60\x55'
lime = '\x40\x7E\x55'
yellow = '\x40\x90\x55'
orange = '\x40\xA0\x55'
red = '\x40\xAE\x55'
pink = '\x40\xC0\x55'
fuchsia = '\x40\xD0\x55'
purple = '\x40\xF0\x55'

## Brightness levels (not reliable)
bright0 = '\x4E\x02\x55'	#Min brightness
bright1 = '\x4E\x03\x55'
bright2 = '\x4E\x04\x55'
bright3 = '\x4E\x05\x55'
bright4 = '\x4E\x06\x55'
bright5 = '\x4E\x07\x55'
bright6 = '\x4E\x08\x55'
bright7 = '\x4E\x09\x55'
bright8 = '\x4E\x0A\x55'
bright9 = '\x4E\x0B\x55'
bright10 = '\x4E\x0C\x55'
bright11 = '\x4E\x0D\x55'
bright12 = '\x4E\x0E\x55'
bright13 = '\x4E\x0F\x55'
bright14 = '\x4E\x10\x55'
bright15 = '\x4E\x11\x55'
bright16 = '\x4E\x12\x55'
bright17 = '\x4E\x13\x55'
bright18 = '\x4E\x14\x55'
bright19 = '\x4E\x15\x55'
bright20 = '\x4E\x16\x55'
bright21 = '\x4E\x17\x55'
bright22 = '\x4E\x18\x55'
bright23 = '\x4E\x19\x55'
bright24 = '\x4E\x1A\x55'
bright25 = '\x4E\x1B\x55'	#Max brightness

## Get group
if options.group == "0" or options.group == "all":
    group = allon
elif options.group == "1":
	group = oneon
elif options.group == "2":
	group = twoon
elif options.group == "3":
	group = threeon
elif options.group == "4":
	group = fouron
else:
	if options.group is not None:
		sys.exit("ERROR! Invalid group: " + options.group)
	else:
		sys.exit("ERROR! group not specified")

## Get command
if options.command is None:				# Exception: no command provided (brightness only?)
	command = None
elif options.command == "on":			# Exception: on (equal group)
	command = None
elif options.command == "white":		# Exception: white light (change with group)
	command = "white"
elif options.command == "off":			# Exception: off (change with group)
    if options.group == "0" or options.group == "all":
        command = alloff
    elif options.group == "1":
        command = oneoff
    elif options.group == "2":
        command = twooff
    elif options.group == "3":
        command = threeoff
    elif options.group == "4":
        command = fouroff
elif options.command == "fade_rainbow":
	command = red
	repeat = 1
elif options.command == "fade_white":
	command = "white"
	repeat = 2
elif options.command == "fade_rgbw":
	command = red
	repeat = 3
elif options.command == "blink_rainbow":
	command = red
	repeat = 4
elif options.command == "blink_random":
	command = red
	repeat = 5
elif options.command == "blink_red":
	command = red
	repeat = 6
elif options.command == "blink_green":
	command = green
	repeat = 7
elif options.command == "blink_blue":
	command = blue
	repeat = 8
elif options.command == "fade_blink_all":
	command = red
	repeat = 9
else:									# No exception: get command name and load corresponding message
	try:
		command = eval(options.command)
	except:
		sys.exit("ERROR! Invalid command: " + options.command)

if command == "white":		# Exception: white light (change with group)
    if options.group == "0" or options.group == "all":
        command = allwhite
    elif options.group == "1":
        command = onewhite
    elif options.group == "2":
        command = twowhite
    elif options.group == "3":
        command = threewhite
    elif options.group == "4":
        command = fourwhite

## Get brightness
if options.brightness is not None:
	try:
		if 0 <= int(options.brightness) <=25:
			brightness = eval("bright" + options.brightness)
		else:
			sys.exit("ERROR! Brightness setting out of range: " + options.brightness)
	except:
		sys.exit("ERROR! Brightness setting should be an integer number between 0 and 25: " + options.brightness)

## Create socket
UDPSock = socket(AF_INET,SOCK_DGRAM)

## Send messages
if group is not None:
    if not options.command == "off":
        UDPSock.sendto(group,addr)			# Send group
        time.sleep(0.1)
if command is not None:
	UDPSock.sendto(command,addr)		# Send command
	time.sleep(0.1)
if repeat is not None:
	for x in range (0, repeat):
		UDPSock.sendto(disco,addr)		# Send command
		time.sleep(0.10)
if brightness is not None:
    UDPSock.sendto(brightness,addr)		# Send brightness
    time.sleep(0.1)

## Close socket and exit
UDPSock.close()
sys.exit(0)
