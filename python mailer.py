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
# Version 1.0.2: Able to send out HTML message now
# Version 1.0.3: Re-enable the use of SmartMessage, MailServer for abstraction

#TODO:	1. [x] Fix encoding problem (unicode support)
#	2. [x] Do pratical test with Gmail (Can I use Gmail to send out email?)
#	3. [x] Repeat mailing (Can I send out a mail to a person, 180 times in a 5 sec interval?)
#	4. [] Change of program behavior: Send out email from an internal email-address-list (more than 1 receiver) in a single loop, one receiver each time
#	5. [x] Able to send out text/html message rather than text/plain only
#	6. [] Read email addresses from a text-based mailing list
#	7. [] Message template: Able to read external file as the content (html) of the message body
#	8. [] Warp up: Tidy up code section to let others use my program...easily (May be warp up with function)
##############################################################
import sys, time # taking argv and sleeper
import smtplib # for SMTP mailing features

###### Variable Definition ######

#@see help(smtplib)
smtpAddr = 'smtp.gmail.com' #@see REFERENCE section
port = '465'
username = 'aaronishere@gmail.com'
password = '06936841'
fromAddr = 'test@test.com'
toAddr = ['gethighprofit@gmail.com','Aaron <aaronishere@gmail.com>']#, 'aaronlaw@gmail.com',  'herbalifeaaron@yahoo.com.hk', 'Kaiser KS <wwwkaiserkscom@gmail.com>', 'luk Benny <lukkaihang@hotmail.com>']
isOverSSL = True

intervalPerAction = 5 # in second
intervalPerBunch = 10*60 # min = time*60sec
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

### for used by smtplib simply
#msg = "Subject: Hello, a test from aaron's self made program\n\n"
#msg = msg + "This is the body of the message\n 我們BBC’s Top 100 Best Novels BBC：有史以来最伟大的100部小说.有效的學習方法.\n<a href='http://www.google.com>A URL</a> port 465 by SMTP_SSL interval test"

### for used by class SmartMessage
subject = "hello, this is a content-type test from aaron"
content = "Dear all, <br />I am writing a mailing program and doing a test. please DO REPLY me if you got this email.(just press the REPLY BUTTON to let me see the actual mail)<br /><br />This is the body of the message\n 我們BBC’s Top 100 Best Novels BBC：有史以来最伟大的100部小说.有效的學習方法.\n<a href='http://www.google.com'>A URL</a> port 465 by SMTP_SSL interval test. Content-type = text/html<br />by python mailer v1.0.3"
msg = SmartMessage(fromAddr, toAddr, subject, content)
# change the content-type to enable HTML
msg.set_type('text/html')
#print msg.get_content_type()
#msg = str(msg) # make SmartMessage object to string if not use MailServer to send mail

### use python built-in smtplib to connect to server
#if isOverSSL is True: # server connected over SSL
#	server = smtplib.SMTP_SSL(smtpAddr, port)
#else:
#	server = smtplib.SMTP(smtpAddr, port)
#server.login(username, password)
#server.sendmail(fromAddr, toAddr, msg)

### use custom class MailServer to connect to server
#MailServer(smtpAddr, username, password, port).sendMessage(msg)

##### MAIN ######
try: 
	#while counter <= len(sys.argv[1]):
	for count in range(int(sys.argv[1])): #loop through the range in the cmd argv given
		msgCount = "\n\nThis is the "+ str(count) +" out of "+ str(sys.argv[1]) +" mail, with a time interval = " + str(intervalPerAction) + "seconds."
		
		MailServer(smtpAddr, username, password, port).sendMessage(msg)
		time.sleep(intervalPerAction)
		print 'Mail #',count ,'is sent.'
except Exception as error: 
	print error
	print ('There was no such file.', error)
