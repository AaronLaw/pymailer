##### FUNCTION ######
### custom functions in mailer.py are moved to here since Version1.2.1.2_freeze
import sys, time # taking argv and sleeper
import smtplib # for SMTP mailing features
from SendMail import SmartMessage, MailServer

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
		msg.set_charset('UTF-8')
		#msg.add_header('Content-Transfer-Encoding', '8bit')
		#print msg.get_content_charset()		
		#print(msg)
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
	intervalPerBunch = sleep*60 # min = time*60sec
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
		# pause every 30 mail
		if totalOfAddr % 30 == 0:
			print('I am going to sleep ',intervalPerBunch, 'seconds.')
			time.sleep(intervalPerBunch)
	print('There are ', count, ' out of', totalOfAddr, 'mail sent successfully.')
	print('If you found a bug or an idea, pls report to aaronlaw@gmail.com. Thanks for using it, bye!' )

### mailList is a list of receivers
def sendRepeatMail(subject, content, fromAddr, toAddrList, smtpAddr, username, password, port, sleep=5, repeat=1):
	print 'I am in repeat mail mode. I am goint to send mail in every '+ str(sleep) + ' second.'
	for i in repeat:
		print 'Repeat mail round #', i
		print 'Processing... ' + toSingleAddr,
		sendMail(subject, content, fromAddr, toAddrList, smtpAddr, username, password, port, sleep)

