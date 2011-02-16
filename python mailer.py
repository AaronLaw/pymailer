# -*- coding: utf8 -*-

#############################################################
# Program: 	python mailer.py
#	This script opens a mailing list (a file supplied) in command argv and mails it to each receiver in a given time interval (to prevent spam jam).
# Author: 	Aaron Law
# Date:		2011-01-22
# Version 0: 	initial to test python features.
# Version 1.0: 	add class SmartMessage, MailServer, which are wrapper class for python's built-in function of mailing, in SendMail.py
#		fix encoding problem in SendMail.py. Now can send Chinese character
##############################################################
import sys, time # taking argv and sleeper
import smtplib # for SMTP mailing features
 
counter = 0

###### Variable Definition ######
intervalPerAction = 0.5 # in second
intervalPerBunch = 10*60 # min = time*60sec

#@see help(smtplib)
smtpAddr = 'smtp.google.com' #@see REFERENCE section
port = '25'
username = 'aaronishere@gmail.com'
password = '06936841'
fromAddr = 'aaronishere@test.com'
toAddr = 'aaronishere@gmail.com'
overSSL = True
#################################

###### REFERENCE ######
#SMTP address for common email provider:
#gmail: 	smtp.gmail.com:465 (over SSL)
#yahoo mail:
#mail.com:	
#inbox.com:	
#################################	

#TODO: http://www.wrox.com ISBN is 978-0-470-41463-7
# http://www.wrox.com/dynamic/books/download.aspx 

from SendMail import SmartMessage
msg = SmartMessage("Me <aaronishere@gmail.com>", 
		"You <aaronishere@gmail.com>",
		"Your picture","Here's that picture I took of you.")
MailServer(smtpAddr, username, password, port).sendMessage(msg)

##### MAIN ######
try: 
	#while counter <= len(sys.argv[1]):
	for chars in (sys.argv[1]): #loop through each character in the cmd argv given
		#msg.encode("utf8")
		#msg = '', counter
		print 'This is the 我們',counter ,'count.'
		counter= counter+1
		time.sleep(intervalPerAction)
except Exception as error: 
	print error
	print ('There was no such file.', error)
