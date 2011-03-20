# -*- coding: utf8 -*-

#############################################################
# Program: 	python mailer.py
#	This script opens a mailing list (a file supplied) in command argv and mails it to each receiver in a given time interval (to prevent spam jam).
# Author: 	Aaron Law
# Date:		2011-01-22
# Version 0: 	initial to test python features.
# Version 1.0: 	add class SmartMessage, MailServer, which are wrapper class for python's built-in function of mailing, in SendMail.py
#		fix encoding problem in SendMail.py. Now can send Chinese character
# Version 1.0.1:Pratical test.
#		1. Setting of Gmail's SMTP server is tested (smtp.gmail.com:465 over SSL). Classes SmartMessage & MailServer are not in use temply due to Gmail's SSL problem.
#		2. Test for sending out email to a receiver in a giver time interval automatically (e.g. send out a mail every 5 seconds)


#TODO:	1. [x] Fix encoding problem (unicode support)
#	2. [x] Do pratical test with Gmail (Can I use Gmail to send out email?)
#	3. [x] Repeat mailing (Can I send out a mail to a person, 180 times in a 5 sec interval?)
#	4. [] Change of program behavior: Send out email from an internal email-address-list (more than 1 receiver) in a single loop, one receiver each time
#	5. [] Able to send out text/html message rather than text/plain only
#	6. [] Read email addresses from a text-based mailing list
#	7. [] Message template: Able to read external file as the content (html) of the message body
##############################################################
import sys, time # taking argv and sleeper
import smtplib # for SMTP mailing features
 
counter = 0

###### Variable Definition ######
intervalPerAction = 10 # in second
intervalPerBunch = 10*60 # min = time*60sec

#@see help(smtplib)
smtpAddr = 'smtp.gmail.com' #@see REFERENCE section
port = '465'
username = 'aaronishere@gmail.com'
password = '06936841'
fromAddr = 'test@test.com'
toAddr = ['gethighprofit@gmail.com','Aaron <aaronishere@gmail.com>', 'aaronlaw@gmail.com',  'herbalifeaaron@yahoo.com.hk']
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

from SendMail import SmartMessage, MailServer
#msg = SmartMessage("Me <aaronishere@gmail.com>", 
#		"You <aaronishere@gmail.com>",
#		"Your picture","Here's that picture I took of you.")
#MailServer(smtpAddr, username, password, port).sendMessage(msg)

msg = "Subject: Hello, a test from aaron's self made program\n\n"
msg = msg + "This is the body of the message\n 我們BBC’s Top 100 Best Novels BBC：有史以来最伟大的100部小说.有效的學習方法.\n<a href='http://www.google.com>A URL</a> port 465 by SMTP_SSL interval test"

server = smtplib.SMTP_SSL(smtpAddr, port)
server.login(username, password)
server.sendmail(fromAddr, toAddr, msg)

##### MAIN ######
try: 
	#while counter <= len(sys.argv[1]):
	for count in range(int(sys.argv[1])): #loop through the range in the cmd argv given
		print 'Mail #',count ,'is sent.'
		msgCount = "\n\nThis is the "+ str(count) +" out of "+ str(sys.argv[1]) +" mail, with a time interval = " + str(intervalPerAction) + "seconds."
		#counter= counter+1
		server.sendmail(fromAddr, toAddr, msg+msgCount)
		time.sleep(intervalPerAction)
except Exception as error: 
	print error
	print ('There was no such file.', error)
