# Import smtplib for the actual sending function
import smtplib
import csv

# Import the email modules we'll need
from email.mime.text import MIMEText


# Create a text/plain message


rejected = False

recips = list()

recip_file = ''


if rejected:
    with open('../reject_letter.txt') as fp:
        msg = MIMEText(fp.read())
    msg['Subject'] = 'Thank You'
    recip_file = '../rejected.txt'


else:
    with open('../accept_letter.txt') as fp:
     msg = MIMEText(fp.read())
    msg['Subject'] = 'Congratulations'
    recip_file = '../accepted.txt'


with open(recip_file) as f:
    bcc = f.read().splitlines()




toaddr = 'hackatbrownDave@gmail.com'
toaddrs = [toaddr] + bcc

msg['From'] = 'hackatbrownDave@gmail.com'
msg['To'] = toaddr


print msg.as_string()

username = 'hackatbrownDave@gmail.com'
password = 'hackatbrown'


server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(username, toaddrs, msg.as_string())
server.quit()


# Send the message via our own SMTP server, but don't include the
# envelope header.
#s = smtplib.SMTP('localhost')
#server.sendmail(me, [you], msg.as_string())
