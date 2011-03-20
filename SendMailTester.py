# -*- coding: utf8 -*-

from SendMail import SmartMessage
msg = SmartMessage("Me <me@example.com>", "You <you@example.com>", "Your picture","Here's that picture I took of you.")
print (str(msg))


from SendMail import MailServer
msg1 = SmartMessage("aaronishere@gmail.com", "Aaron <aaronishere@gmail.com>, Hello <hello@abc.com>", 'This is subject', 'Content goes here.')
print(str(msg1))
MailServer('smtp.gmail.com', 'aaronishere@gmail.com','06936841', '465').sendMessage(msg1)
