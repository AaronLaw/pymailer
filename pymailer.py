# -*- coding: utf8 -*-

#############################################################
# Program: 	python mailer.py
#		This script opens a mailing list (a file supplied) in command argv and mails it to every receiver in a given time interval (to prevent spam jam).
# Author: 	Aaron Law
# Date:		2011-01-22
# Last update:	2011-02-06
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
# 2011-01-22:
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
#
# 2011-01-23: In production
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
# 2011-01-24:
# Version 1.2.1.1: Enhance mail's charset. msg.set_charset() is set to UTF8
#
# 2011-01-26:
# Version 1.2.1.2: Program is pause in a time period in mass mail mode. Variable intervalPerBunch is in use now
#
# 2011-02-06:
# Version 1.2.1.2_freeze:
#			Same as Version 1.2.1.2, excepts custom functions are moved to mailer_func.py 
#
#TODO:	1. [x] Fix encoding problem (unicode support)
#	2. [x] Do pratical test with Gmail (Can I use Gmail to send out email?)
#	3. [x] Repeat mailing (Can I send out a mail to a person, 180 times in a 5 sec interval?)
#	4. [x] Change of program behavior: Send out email from an internal email-address-list (more than 1 receiver) in a single loop, one receiver each time
#	5. [x] Able to send out text/html message rather than text/plain only
#	6. [x] Read email addresses from a text-based mailing list
#		6.1 [x] Make it robust to handle dead/invaild email address (no program crash)
#	7. [] Message template: Able to read external file as the content (html) of the message body
#	8. [x] Warp up: Tidy up code section to let others use my program...easily (May be warp up with function)
#	9. [] Write hints for usage
# 	10. [] Have I separate data and logic?
#	11. [] As a bots: Simulate human's behaviour to confuse mail providers
#	12..[] Multiple-user-account: randomly pick up a user account to send mail to prevent mail providers' daily-out limitation
##############################################################
import sys, time # taking argv and sleeper
import smtplib # for SMTP mailing features

###### Variable Definition ######

#@see help(smtplib)
smtpAddr = 'smtp.gmail.com' #@see REFERENCE section
port = '465'
username = 'aaronishere@gmail.com'
password = '69279308' #ZdC0oII0
fromAddr = 'test@test.com'
toAddr = ['gethighprofit@gmail.com','Aaron <aaronishere@gmail.com>']#, 'aaronlaw@gmail.com',  'herbalifeaaron@yahoo.com.hk', 'Kaiser KS <wwwkaiserkscom@gmail.com>', 'luk Benny <lukkaihang@hotmail.com>']
isOverSSL = True

intervalPerAction =  5 # in second
#intervalPerBunch = 2*60 # min = time*60sec
#################################

###### REFERENCE ######
#SMTP address for common email provider:
#gmail: 	smtp.gmail.com:465 (over SSL)
#yahoo mail:	smtp.mail.yahoo.com:465
#hotmail:	
#mail.com:	
#inbox.com:	
#gmx.com:	mail.gmx.com:465
#kaiserks.com:	mail.photo.kaiserks.com
#################################	

#TODO: http://www.wrox.com ISBN is 978-0-470-41463-7
# http://www.wrox.com/dynamic/books/download.aspx
# Google: use python to send email 
# Google: use python to send email header
# Google: use php to send email -> cation on the setting of 'header'
# http://docs.python.org/library/smtplib.htm
# Beginning Python - From Novice to Professinnas Secont Edition (2008) - Ch9:Generator

from SendMail import SmartMessage, MailServer

### Setup text mail here (by smtplib simply)
#msg = "Subject: Hello, a test from aaron's self made program\n\n"
#msg = msg + "This is the body of the message\n\n<a href='http://www.google.com>A URL</a> port 465 by SMTP_SSL interval test"

### Setup text or HTML mail here (by class SmartMessage)
subject = "想係屋企度工作? 你現在可以做的事…"
#content = "Dear all, <br />I am writing a mailing program and doing a test. please DO REPLY me if you got this email.(just press the REPLY BUTTON to let me see the actual mail)<br /><br />This is the body of the message<br /><a href='http://www.google.com'>A URL</a> port 465 by SMTP_SSL interval test. Content-type = text/html 個人訪問"
content = '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type">
  </head>
  <body bgcolor="#ffffff" text="#000000">
    <div class="moz-text-html" lang="x-western">
      <div class="moz-text-html" lang="x-western">
        <div class="moz-text-html" lang="x-unicode">
          <div class="moz-text-html" lang="x-unicode"> <font size="2"
              color="black" face="arial">
              <div>
                <div style="margin-bottom: 0cm;"><big><big>返工好無聊？但又唔知點樣可
                      以賺 取外 快？<br>
                    </big></big><br>
                  <font size="4">你在尋找的，不是一個受薪的工作，</font></div>
                <div style="margin-bottom: 0cm;"><font size="4">而是一個運用電腦
                    在家 工作 的生 意機 會</font></div>
                <div style="margin-bottom: 0cm;"><font size="4">你可藉此機會，選
                    擇……</font><font><font><font size="4">.</font></font></font></div>
                <div style="margin-bottom: 0cm;" align="JUSTIFY"><font><font><font
                        size="4"><b>1. </b></font></font></font><font
                    size="4"><b>時 間自由地兼職工作</b></font><font size="4">，或</font><font
                    size="4"> </font> </div>
                <div style="margin-bottom: 0cm;" align="JUSTIFY"><font><font><font
                        size="4"><b>2. </b></font></font></font><font
                    size="4"><b>全 程投入達至財務自由。</b></font></div>
                <div style="margin-bottom: 0cm;" align="JUSTIFY"><font
                    size="4">請 登入以下網站</font></div>
                <div style="margin-bottom: 0cm;" align="JUSTIFY"><br>
                </div>
                <div style="margin-bottom: 0cm;" align="JUSTIFY"><font
                    size="5" color="darkcyan"><a
                      href="http://www.gethighprofit.com/"
                      target="_blank">http://www.<span>gethighprofit</span>.com/</a></font><br>
                </div>
                <div style="margin-bottom: 0cm;" align="JUSTIFY"><br>
                </div>
                <div style="margin-bottom: 0cm;" align="JUSTIFY"><br>
                </div>
                <div style="margin-bottom: 0cm;" align="JUSTIFY"><font
                    size="4"><br>
                  </font></div>
                <div style="margin-bottom: 0cm;" align="JUSTIFY"><font><font><font
                        size="2">***</font></font></font><font size="2">如
                    閣 下不 想再 接受 本公司的電郵廣告，請回覆此電郵，<wbr>以便本公司取消閣下之電郵地址</font></div>
                <div style="margin-bottom: 0cm;" align="JUSTIFY"><font><font><font
                        style="font-size: 8pt;" size="1">All right
                        reserved for this Keep Fit Promotion. Please do
                        not delete or change the content.</font></font></font></div>
                <div style="margin-bottom: 0cm;" align="JUSTIFY"><font
                    style="font-size: 8pt;" size="1">此廣告宣傳是受香港版權約束，請勿隨意刪
                    除及 更改 內容</font><font><font><font style="font-size:
                        8pt;" size="1">***</font></font></font></div>
              </div>
            </font> </div>
        </div>
      </div>
    </div>
  </body>

</html>

'''
content = content + '<p>I am Hong Kong people@TST</p>'

##### FUNCTION ######
### @Version1.2.1.2_freeze: moved to mailer_func.py
from mailer_func import *

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
