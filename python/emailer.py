# Import smtplib for the actual sending function
import smtplib
import csv
import sys
import os

# Import the email modules we'll need
from email.mime.text import MIMEText


# Create a text/plain message

rejected = (sys.argv[1] == "True")
company_name = sys.argv[2]
link = sys.argv[3] #https://www.youtube.com/watch?v=3KANI2dpXLw


recips = list()

recip_file = ''

if rejected:
    try:
        with open(os.path.join(os.getcwd(), 'static/assets/data/letters/reject_letter.txt'),"rb") as fp:
            print fp
            sys.stdout.flush()
            msg = MIMEText(fp.read())
    except IOError:
        print "io error"


    msg['Subject'] = 'Thank You'
    recip_file = os.path.join(os.getcwd(), 'reject_email.txt')
else:
    with open(os.path.join(os.getcwd(), 'static/assets/data/letters/accept_letter.txt'),"rb") as fp:
        msg = MIMEText(fp.read())
    msg['Subject'] = 'Congratulations'
    recip_file = os.path.join(os.getcwd(), 'accept_email.txt')



with open(recip_file) as f:
    bcc = f.read().splitlines()





toaddr = 'hackatbrownDave@gmail.com'
toaddrs = [toaddr] + bcc

msg['From'] = 'hackatbrownDave@gmail.com'
msg['To'] = toaddr

m = msg.as_string()
m = m.replace('<COMPANY NAME>', company_name)
m = m.replace('<LINK>', link)

print m

username = 'hackatbrownDave@gmail.com'
password = 'hackatbrown'


server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(username, toaddrs, m)
server.quit()

open(recip_file, 'w').close()


# Send the message via our own SMTP server, but don't include the
# envelope header.
#s = smtplib.SMTP('localhost')
#server.sendmail(me, [you], msg.as_string())
