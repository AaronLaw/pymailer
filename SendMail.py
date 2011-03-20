#############################################################
# Program: 	SendMail.py
#		This script warps Python's built-in mailing functions to a better & more user-friendly inrterface.
#		It contains 2 classes: SmartMessage & MailServer	
# Author: 	Aaron Law
# Date:		2011-01-22
# Original:	source code from Wrox.Beginning.Python.Using.Python.2.6.and.Python.3.1.Feb.2010 - Chapter 16: Network Programming
#		http://www.wrox.com ISBN is 978-0-470-41463-7
# 		http://www.wrox.com/dynamic/books/download.aspx 
#
# Version 1.0: 	Original code from James Payne: class SmartMessage, MailServer, which are wrapper class for python's built-in function of mailing, in SendMail.py
# Version 1.0.1: Change MailServer(SMTP) to MailServer(SMTP_SSL) for Gmail's connection (Gmail's connection is over SSL)
# Version 1.0.2: Exception in user login: Fixing try...except block to raise an SMTPAuthenticationError exception


#TODO:	1. [x] Use James Payne's code to make better handling of making mail

##############################################################
from email import encoders as Encoders
from email.message import Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
import mimetypes
class SmartMessage:
	"""A simplified interface to Python's library for creating email
	messages, with and without MIME attachments."""
	def __init__(self, fromAddr, toAddrs, subject, body):
		"""Start off on the assumption that the message will be a simple RFC
		2822 message with no MIME."""
		self.msg = Message()
		self.msg.set_payload(body)
		self['Subject'] = subject
		self.setFrom(fromAddr)
		self.setTo(toAddrs)
		self.hasAttachments = False
	def setFrom(self, fromAddr):
		"Sets the address of the sender of the message."
		if not fromAddr or not type(fromAddr)==type(''):
			raise Exception ('A message must have one and only one sender.')
		self['From'] = fromAddr
	def setTo(self, to):
		"Sets the address or addresses that will receive this message."
		if not to:
			raise Exception ('A message must have at least one recipient.')
		self.__addresses(to, 'To')
		#Also store the addresses as a list, for the benefit of future
		#code that will actually send this message.
		self.to = to
	def setCc(self, cc):
		"""Sets the address or addresses that should receive this message,
		even though it's not addressed directly to them ("carbon-copy")."""
		self.__addresses(cc, 'Cc')
	def addAttachment(self, attachment, filename, mimetype=None):
		"Attaches the given file to this message."
		#Figure out the major and minor MIME type of this attachment,
		#given its filename.
		if not mimetype:
			mimetype = mimetypes.guess_type(filename)[0]
		if not mimetype:
			raise Exception ("Couldn't determine MIME type for ", filename)
		if '/' in mimetype:
			major, minor = mimetype.split('/')
		else:
			major = mimetype
			minor = None
		#The message was constructed under the assumption that it was
		#a single-part message. Now that we know there's to be at
		#least one attachment, we need to change it into a multi-part
		#message, with the first part being the body of the message.
		if not self.hasAttachments:
			body = self.msg.get_payload()
			newMsg = MIMEMultipart()
			newMsg.attach(MIMEText(body))
			#Copy over the old headers to the new object.
			for header, value in self.msg.items():
				newMsg[header] = value
			self.msg = newMsg
			self.hasAttachments = True
		subMessage = MIMENonMultipart(major, minor, name=filename)
		subMessage.set_payload(attachment)
		#Encode text attachments as quoted-printable, and all other
		#types as base64.
		if major == 'text':
			encoder = Encoders.encode_quopri
		else:
			encoder = Encoders.encode_base64
		encoder(subMessage)
		#Link the MIME message part with its parent message.
		self.msg.attach(subMessage)
	def __addresses(self, addresses, key):
		"""Sets the given header to a string representation of the given
		list of addresses."""
		if hasattr(addresses, '__iter__'):
			addresses = ', '.join(addresses)
		self[key] = addresses
	#A few methods to let scripts treat this object more or less like
	#a Message or MultipartMessage, by delegating to the real Message
	#or MultipartMessage this object holds.
	def __getitem__(self, key):
		"Return a header of the underlying message."
		return self.msg[key]
	def __setitem__(self, key, value):
		"Set a header of the underlying message."
		self.msg[key] = value
	def __getattr__(self, key):
		return getattr(self.msg, key)
	def __str__(self):
		"Returns a string representation of this message."
		return self.msg.as_string()
# end of class SmartMessage

from smtplib import SMTP, SMTP_SSL
class MailServer(SMTP_SSL):
	"A more user-friendly interface to the default SMTP class."
	def __init__(self, server, serverUser=None, serverPassword=None, port=465):
		"Connect to the given SMTP server."
		SMTP_SSL.__init__(self, server, port)
		self.user = serverUser
		self.password = serverPassword
		#Uncomment this line to see the SMTP exchange in detail.
		#self.set_debuglevel(True)
	def sendMessage(self, message):
		"Sends the given message through the SMTP server."
		#Some SMTP servers require authentication.
		if self.user:
			#try:
			#	self.login(self.user, self.password)
			#except Exception as error:
			#	print (error)
			### use raise Exception instead
			if not self.login(self.user, self.password):
				raise Exception('username & password is NOT correct. Pls try again.')
		#The message contains a list of destination addresses that
		#might have names associated with them. For instance,
		#"J. Random Hacker <jhacker@example.com>". Some mail servers
		#will only accept bare e-mail addresses, so we need to create a
		#version of this list that doesn't have any names associated
		#with it.
		destinations = message.to
		if hasattr(destinations, '__iter__'):
			destinations = map(self.__cleanAddress, destinations)
		else:
			destinations = self.__cleanAddress(destinations)
		self.sendmail(message['From'], destinations, str(message))
	def __cleanAddress(self, address):
		"Transforms 'Name <e-mail@domain>' into 'e-mail@domain'."
		parts = address.split('<', 1)
		if len(parts) > 1:
			#This address is actually a real name plus an address:
			newAddress = parts[1]
			endAddress = newAddress.find('>')
			if endAddress != -1:
				address = newAddress[:endAddress]
		return address
# end of class MailServer
