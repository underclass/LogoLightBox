#!/usr/bin/env python

import time
import os
import motephat

motephat.configure_channel(1, 16, False)
motephat.configure_channel(2, 16, False)

motephat.set_clear_on_exit(True)

facebookUrl = os.environ.get('facebook')
instagramUrl = os.environ.get('instagram')

def getFacebookLikes():
	likes = os.popen("curl -s %s | grep 'total_likes:' | grep -o '[0-9|,]\+' | tr -d ','" % facebookUrl).read()

	return likes

#making changes here

def getInstagramFollowers():
	followers = os.popen("curl -s %s | grep -o 'meta content=\"[[:digit:]]\{1,\} Followers' | grep -o '[0-9|,]'" % instagramUrl).read()

	#'meta content=\"[[:digit:]]\{1,\} Followers' | grep -o '[0-9|,]\+'

	return followers.replace(',','')

def setMoteColor(r, g, b):
	# http://forums.pimoroni.com/t/mote-phat-not-all-leds-are-lighting-on-first-show/3740/3
	# Workaround: multiple motephat.show()
	motephat.set_all(r, g, b, 1.0)
	motephat.show()
	motephat.show()

# defines the blink
def setMoteBlink(r, g, b):
	for x in range(4):
		setMoteColor(r, g, b)
		time.sleep(0.25)

		setMoteColor(255, 255, 255)
		time.sleep(0.25)

def main():
	previousFacebookLikes = 0
	previousInstagramFollowers = 0

	while(1):
		currentFacebookLikes = getFacebookLikes().strip()

		if(currentFacebookLikes > previousFacebookLikes):
			setMoteBlink(0,0,255)
			print "Facebook: " + currentFacebookLikes
			previousFacebookLikes = currentFacebookLikes

		currentInstagramFollowers = getInstagramFollowers().strip()

		if(currentInstagramFollowers > previousInstagramFollowers):
			setMoteBlink(255, 8, 127)
			print "Instagram: " + currentInstagramFollowers
			previousInstagramFollowers = currentInstagramFollowers

		setMoteColor(255, 255, 255)

		time.sleep(60)

main()
