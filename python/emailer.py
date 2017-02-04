# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText


# Create a text/plain message
msg = MIMEText('abc')


# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'The contents is here'
msg['From'] = 'hackatbrownDave@gmail.com'
msg['To'] = 'zfeinberg@gmail.com'

username = 'hackatbrownDave@gmail.com'
password = 'hackatbrown'

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(username, 'zfeinberg@gmail.com', msg.as_string())

# Send the message via our own SMTP server, but don't include the
# envelope header.
#s = smtplib.SMTP('localhost')
#server.sendmail(me, [you], msg.as_string())
server.quit()
