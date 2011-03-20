# -*- coding: utf8 -*-

#############################################################
# Program: 	python mailer.py
#		This script opens a mailing list (a file supplied) in command argv and mails it to every receiver in a given time interval (to prevent spam jam).
# Author: 	Aaron Law
# Date:		2011-01-22
# Last update:	2011-01-24
#
# Original Problem: 	[Write down to clear my mind...]
#		I need to send out mail to many people at work. This is a mass email for ads. I can do it with a free gmail/yahoo email account with my bare hands, but...
#		1. Gmail blocks me when I send a bunch of mail once a time.
#		2. I can send mail in a small bunch onec a time, but I don't have much spare time...
#		I need a auto-robot to help me send mail. The robot should send to a receiver once a time to prevent Gmail/Yahoo/Mail.com's spam jam.
#		-> Problem: [No much spare time, don't want to sit in front of computer to send mail and wait and wait, being lazy and free my hands to do other things, Gmail doesn't allow me to send mail in a large bunch, I want others to do the job for me]
#
# Solution:	I should have a robot to do AUTOMATION for me, reading email address from a list and sending mail to them without spam jam. That's great if it sends mail to one person once a time.
#		 -> Robot as a smtp client, for automating mass email-marketing (auto-robot for MUA)
#
# Problem when I code:
#		[To clear my mind...had I done what I need to solve originally? or coding abuse when I still code for it?
#		 -> Had I coded what I need to code or Had I trapped into coding abuse?
#		 -> Had I finished the program even though it is imperfact, or should I write more features to the program?
#		 -> When should I quit the coding task and start to use it at work?
#		 -> Had I get things done ever the program is imperfact?
#		 -> Can I use this program at work NOW?]
#
#############################################################
# Version 0: 	initial to test python features.
# Version 1.0: 	add class SmartMessage, MailServer, which are wrapper class for python's built-in function of mailing, in SendMail.py
#		fix encoding problem in SendMail.py. Now can send Chinese character
# Version 1.0.1:Pratical test.
#		1. Setting of Gmail's SMTP server is tested (smtp.gmail.com:465 over SSL). Classes SmartMessage & MailServer are not in use temply due to Gmail's SSL problem.
#		2. Test for sending out email to a receiver in a giver time interval automatically (e.g. send out a mail every 5 seconds)
# Version 1.0.2: Able to send out HTML message now
# Version 1.0.3: Re-enable the use of SmartMessage, MailServer for abstraction
# Version 1.1.0: About mailing list
#		1. Able to read email addresses from a text-based mailing list
#		2. Send to receivers on mailing list one after one
# Version 1.1.1: Code clean up, and make reading mailinglist file a function for handling file error
# Version 1.2.0: Grouping mailing process by function for abstraction (v1.1.1 is the last one with on use of function)
#		1. sendMassMail()...done
#		2. sendMail()...done
#		3. sendRepeatMail...leave for TODO
# Version 1.2.1: Bug fix: A bug is found since V1.1.0 (changes from V1.0.3 to V1.1.0: I give a list of addresses from a internal list in V1.0.3...and I give a list of addresses to 'toAddr' from a file in V1.1.0)
#		The bug is: Mail is send as plain text rather than html mail even though content-type is set to 'text/html'. It is caused by the ending return char ('\n') at the end of the email address. 
#			(I find that bug in the code 'for toSingleAddr in mailList:' in sendMassMail().
#			I find the difference between reading addresses from an internal list and from a file by  doing "print toSingleAddr":
#				 1. from an internal addresses list -> results in "aaronishere@gmail.com"
#				 2. Reading addresses from a file -> results in "aaronishere@gmail.com\n". And the ending '\n' leads to the bug)
#	
#TODO:	1. [x] Fix encoding problem (unicode support)
#	2. [x] Do pratical test with Gmail (Can I use Gmail to send out email?)
#	3. [x] Repeat mailing (Can I send out a mail to a person, 180 times in a 5 sec interval?)
#	4. [x] Change of program behavior: Send out email from an internal email-address-list (more than 1 receiver) in a single loop, one receiver each time
#	5. [x] Able to send out text/html message rather than text/plain only
#	6. [x] Read email addresses from a text-based mailing list
#		6.1 [x] Make it robust to handle dead/invaild email address (no program crash)
#	7. [] Message template: Able to read external file as the content (html) of the message body
#	8. [] Warp up: Tidy up code section to let others use my program...easily (May be warp up with function)
#	9. [] Write hints for usage
# 	10. [] Have I separate data and logic?
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

intervalPerAction =  2 # in second
intervalPerBunch = 10*60 # min = time*60sec
#################################

###### REFERENCE ######
#SMTP address for common email provider:
#gmail: 	smtp.gmail.com:465 (over SSL)
#yahoo mail:	smtp.mail.yahoo.com:465
#hotmail:	
#mail.com:	
#inbox.com:	
#################################	

#TODO: http://www.wrox.com ISBN is 978-0-470-41463-7
# http://www.wrox.com/dynamic/books/download.aspx
# Google: use python to send email 
# Google: use python to send email header
# Google: use php to send email -> cation on the setting of 'header'
# http://docs.python.org/library/smtplib.htm

from SendMail import SmartMessage, MailServer

### Setup text mail here (by smtplib simply)
#msg = "Subject: Hello, a test from aaron's self made program\n\n"
#msg = msg + "This is the body of the message\n\n<a href='http://www.google.com>A URL</a> port 465 by SMTP_SSL interval test"

### Setup text or HTML mail here (by class SmartMessage)
subject = "hello, this is a content-type test from aaron"
content = "Dear all, <br />I am writing a mailing program and doing a test. please DO REPLY me if you got this email.(just press the REPLY BUTTON to let me see the actual mail)<br /><br />This is the body of the message<br /><a href='http://www.google.com'>A URL</a> port 465 by SMTP_SSL interval test. Content-type = text/html"
content = content + '<p>@Version 1.2.0</p>'

##### FUNCTION ######
def readTxt(fname):
	# I don't handle exception here (Cannot open a mailing list is not critical of the process of automation of mail-sending)
	try:
		file = open(fname, 'r')	
		print ('Loading of', fname , 'is success.')
		return file
	except (IOError, IndexError) as error:
		print ('An error occur:', error)
		print ('Oh! Program is going to terminate')		
		sys.exit()

### sendMail() sends one mail from a list (one mail to a bunch of people each time)
### It accepts a bunch of address in a list (e.g. ['1@test.com', '2@test.com'])
def sendMail(subject, content, fromAddr, toAddrList, smtpAddr, username, password, port, sleep):
	isSuccess = False	
	try:
		msg = SmartMessage(fromAddr, toAddrList, subject, content)
		msg.set_type('text/html')
		MailServer(smtpAddr, username, password, port).sendMessage(msg)

		time.sleep(sleep)
		isSuccess = True	
	except (Exception) as error: 
		#print (error)
		print ('There is an error occured during sending mail.', error)
		### put invalid mail addresses in a list to show later
		#invalidAddr.append(toSingleAddr)
	return isSuccess # return True when mail send successfully

### sendMassMail() does sending mail to a receiver once a time
def sendMassMail(subject, content, fromAddr, mailList, smtpAddr, username, password, port, sleep=5):
	count = 0
	totalOfAddr = 0
	print 'I am in mass mail mode. I am goint to send mail in every '+ str(sleep) + ' second.'
	for toSingleAddr in mailList:

		print 'Processing ' + toSingleAddr + '...'
		toAddr = toSingleAddr.rstrip("\r\n")  # work around: the ending '\n' char in an address leads to a bug. That bug is 'text\html' doesn't work and leads to the outing mail being plain text
					# Reference: Google: python remove \n
 		isSuccess = sendMail(subject, content, fromAddr, toAddr, smtpAddr, username, password, port, sleep)
		if isSuccess is True:
			count = count + 1 # count is up only when mail out was success (@see isSuccess in sendMail())
			print 'Mail #',count,' is sent to ' + toSingleAddr + '.'
		else:
			print 'Mail #',count,' is not sent to ' + toSingleAddr +'.'

		totalOfAddr = totalOfAddr + 1 # totalOfAddr is up whenever mail out was success or not

	print('There are ', count, ' out of', totalOfAddr, 'mail sent successfully.')

### mailList is a list of receivers
def sendRepeatMail(subject, content, fromAddr, toAddrList, smtpAddr, username, password, port, sleep=5, repeat=1):
	print 'I am in repeat mail mode. I am goint to send mail in every '+ str(sleep) + ' second.'
	for i in repeat:
		print 'Repeat mail round #', i
		print 'Processing... ' + toSingleAddr,
		sendMail(subject, content, fromAddr, toAddrList, smtpAddr, username, password, port, sleep)

##### MAIN ######
count = 0
totalOfAddr = 0 # number of email recever
invalidAddr = []

mailingList = readTxt(sys.argv[1])
#print( type(mailingList))
#totalOfAddr = len(mailingList.readlines())
print('Mail is begin to send...' )
#sendMail(subject, content, fromAddr, ['hh@gg.com', '22@33.com'], smtpAddr, username, password, port, intervalPerAction)
#sendMassMail(subject, content, fromAddr, ['hh@test.com', '22@test.com'], smtpAddr, username, password, port, intervalPerAction)
sendMassMail(subject, content, fromAddr, mailingList, smtpAddr, username, password, port, intervalPerAction)


print invalidAddr
