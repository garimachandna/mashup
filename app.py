import sys
import streamlit as st
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re
import os


# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
 
# Define a function for
# for validating an Email
def check(email):
 
    # pass the regular expression
    # and the string into the fullmatch() method
    if(not re.fullmatch(regex, email)):
        st.error("Invalid Email Address")
        sys.exit()

def sendmail(mail, result):
        
    fromaddr = "chandnagarima4@gmail.com"
    toaddr = mail
    
    # instance of MIMEMultipart
    msg = MIMEMultipart()
    
    # storing the senders email address  
    msg['From'] = fromaddr
    
    # storing the receivers email address 
    msg['To'] = toaddr
    
    # storing the subject 
    msg['Subject'] = "Attachment: Merged audio file of your mashup experiment"
    
    # string to store the body of the mail
    body = "Hello, The result of your mashup is attached herewith.\nThank You\nRegards,\nGarima Chandna\n102017070"
    
    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    
    # open the file to be sent 
    filename = result
    attachment = open(result, "rb")
    
    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')
    
    # To change the payload into encoded form
    p.set_payload((attachment).read())
    
    # encode into base64
    encoders.encode_base64(p)
    
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    
    # attach the instance 'p' to instance 'msg'
    msg.attach(p)
    
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()
    s.ehlo()
    # Authentication
    s.login("chandnagarima4@gmail.com", "crpmaxwjiiwqdkqt")

    # message to be sent
    message = msg.as_string()

    # sending the mail
    s.sendmail("chandnagarima4@gmail.com", mail,  message)

    # terminating the session
    s.quit()
   # st.info( 'The result has been mailed to you :)')





st.title('Mashup')

with st.form(key= 'mashup form'):
    singer= st.text_input('Singer Name')
    noofvideos= st.text_input('Number of videos')
    duration= st.text_input('Duration of each video')
    mailid= st.text_input('Email id')

    button= st.form_submit_button('Submit')
    if button:
        print(singer, noofvideos, duration, mailid)
        if not (( singer.startswith("'") and singer.endswith("'") ) or ( singer.startswith('"') and singer.endswith('"') )):
            st.error('singer name must be enclosed in single/double quotes')
            sys.exit() 
        if(int(noofvideos) <10) :
            st.error('No of videos should be greater than or equal to 10')
            sys.exit() 

        if(int(duration) <20) :
            st.error('Duration of each audio should be greater than or equal to 20')
            sys.exit() 

        check(mailid)    

        
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '10207070.py')

        
        subprocess.call(f'python3 {filename} {singer} {noofvideos} {duration} "m.mp3"')
        sendmail(mail= mailid, result= 'm.mp3')
        st.success('Mail sent successfully')

