This is my first project with Python. It sends out bulk mail from any SMTP server, in a time interval. I create this project intend to free myself from setting in front of computer sending email as my daily work. 

I write it since 2011-01-20 during a 5 days holiday.

Usage
====
It runs on python 2.

Firstly you've to prepare the content of mail in the "Body" block, then

    python pymailer.py


PSEUDO CODE
====
* provide the info of email sender
* read the contact list
* read the template of email content
* construct an email
* connect to email server (SMTP, maybe over SSL)
* send out email to the receivers via the SMTP server
