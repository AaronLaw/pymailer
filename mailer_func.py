##### FUNCTION ######
### custom functions in mailer.py are moved to here since Version1.2.1.2_freeze
### documentation and comment is writen in pymailer.py since this file is part of it
import sys, time # taking argv and sleeper
import smtplib # for SMTP mailing features
from SendMail import SmartMessage, MailServer
import random # simulate human action...pauseLikeAHuman()

def readTxt(fname):
	# I don't handle exception here (Cannot open a mailing list is not critical of the process of automation of mail-sending)
	try:
		file = open(fname, 'r')	
		print ('Loading of %s is success.' % (fname ))
		return file
	except (IOError, IndexError) as error:
		print ('An error occur:', error)
		print ('Oh! Program is going to terminate')		
		sys.exit()

#def shuffleList(file):

#def writeTxt(fname):

### simulate human's delay
def pauseInRandom(sleep):
	min = sleep / 2
	max = sleep * 2
	return random.randint(min, max)

def delayLikeAHuman(sleep):
	time.sleep(pauseInRandom(sleep))

### randomString() is put into the content of mail...to make every mail unique...to confuse gmail.
def randomString():
	return str(random.randint(777,7777))

### sendMail() sends one mail from a list (one mail to a bunch of people each time)
### It accepts a bunch of address in a list (e.g. ['1@test.com', '2@test.com'])
def sendMail(subject, content, fromAddr, toAddrList, smtpAddr, username, password, port):
	isSuccess = False	
	try:
		msg = SmartMessage(fromAddr, toAddrList, subject, content)
		msg.set_type('text/html')
		msg.set_charset('UTF-8')
		#msg.add_header('Content-Transfer-Encoding', '8bit')
		#print msg.get_content_charset()		
		#print(msg)
		MailServer(smtpAddr, username, password, port).sendMessage(msg)

		#time.sleep(sleep)
		isSuccess = True	
	except (Exception) as error: 
		#print (error)
		print ('There is an error occured during sending mail.', error)
		### put invalid mail addresses in a list to show later
		#invalidAddr.append(toSingleAddr)
	return isSuccess # return True when mail send successfully

### sendMassMail() does sending mail to a receiver once a time
### mailList is accept a file-handler or [1@test.com, 2@test.com]
def sendMassMail(subject, content, fromAddr, mailList, smtpAddr, username, password, port, sleep=5):
	count = 0
	totalOfAddr = 0
	#intervalPerBunch = pauseInRandom(sleep)*60 # min = time*60sec # move downward, not in here...see a bug?
	print 'I am in mass mail mode. I am goint to send mail in average every %2i second.' % (sleep)
	sendMail('Notice: '+subject+ 'is sent from '+ fromAddr, content, fromAddr, ['aaronishere@gmail.com', 'gethighprofit@gmail.com'], smtpAddr, username, password, port)
	for toSingleAddr in mailList:
		print 'Processing %s ...' % (toSingleAddr )
		toAddr = toSingleAddr.rstrip("\r\n")  # work around: the ending '\n' char in an address leads to a bug. That bug is 'text\html' doesn't work and leads to the outing mail being plain text
					# Reference: Google: python remove \n
 		isSuccess = sendMail(subject, content, fromAddr, toAddr, smtpAddr, username, password, port)
		delayLikeAHuman(sleep)
		if isSuccess is True:
			count = count + 1 # count is up only when mail out was success (@see isSuccess in sendMail())
			print 'Mail #%2i is sent to %s'% (count, toSingleAddr)
		else:
			print 'Mail is not sent to %s' % (toSingleAddr)

		totalOfAddr = totalOfAddr + 1 # totalOfAddr is up whenever mail out was success or not
		# pause every 30 mail
		if totalOfAddr % 30 == 0:
			intervalPerBunch = pauseInRandom(sleep)*60 # min = time*60sec 
			print('So tired...I have to take a rest for %2i minutes.' % (intervalPerBunch/60) )
			delayLikeAHuman(intervalPerBunch)
			print('OK, I feel better now.')
	print('There are %2i out of %2i mail sent successfully.' % (count, totalOfAddr) )
	print('If you found a bug or an idea, pls report to aaronlaw@gmail.com. Thanks for using it, bye!' )

### send mail to a list of receivers repeatly
### mailList is a list of receivers
def sendRepeatMail(subject, content, fromAddr, toAddrList, smtpAddr, username, password, port, sleep=5, repeat=1):
	print 'I am in repeat mail mode. I am goint to send mail in every %2i second.' % (sleep)
	for i in repeat:
		print 'Repeat mail round #%2i'% (i)
		print 'Processing... %s'% (toSingleAddr)
		sendMail(subject, content, fromAddr, toAddrList, smtpAddr, username, password, port)

