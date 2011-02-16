#############################################################
# Program: 	pythor mailer.py
#	This script opens a mailing list (a file supplied) in command argv and mails it to each receiver in a given time interval (to prevent spam jam).
# Author: Aaron Law
# Date:	2011-01-22
# Version 0: initial to test python features.
#
##############################################################
import sys, time
counter = 0
#while counter <= len(sys.argv[1]):
for chars in (sys.argv[1]): #loop through each character in the cmd argv given
	#msg.encode("utf8")
	#msg = '', counter
	print 'This is the ',counter ,'count.'
	counter= counter+1
	time.sleep(0.5)
