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



import os
import glob
import sys
from youtubesearchpython import *
from pytube import YouTube 
import os
import moviepy.editor as mp
from moviepy.editor import concatenate_audioclips, AudioFileClip


def searchsongs(singer):

    customSearch = VideosSearch(singer)

    l = len(customSearch.result()['result'])
    print(l)
    links= []
    for i in range(l):
        links.append(customSearch.result()['result'][i]['link'])

    return links


def getsongs(links, n):
    print(n)
    c=0
    while c < min(n, len(links)):
        try:
            yt = YouTube(links[c]) 
            mp4files = yt.filter('mp4') 
        
            # get the video with the extension and
            # resolution passed in the get() function 
            d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution) 
            d_video.download('videos/')
            c=c+1
        except Exception as e:
            print(e)


def getaudio(y):
    # Python code to convert video to audio
    # Insert Local Video File Path
    for file in os.listdir('videos'):
        try:
            clip = mp.VideoFileClip(os.path.join('videos', file)).subclip(0,y)

            # Insert Local Audio File Path
            clip.audio.write_audiofile(os.path.join('audio', f"Audio {file}"), codec= 'libmp3lame')
        except Exception as e:
            print(e)
            continue


def mergeaudios(output_path):
    """Concatenates several audio files into one audio file using MoviePy
    and save it to `output_path`. Note that extension (mp3, etc.) must be added to `output_path`"""

    audio_clip_paths = glob.glob('audio/*')
    clips = [AudioFileClip(c) for c in audio_clip_paths]
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_path, codec= 'libmp3lame')



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

      #  filename = os.path.join("102017070.py")
        
       # subprocess.call(f'python3 {filename} {singer} {noofvideos} {duration} "m.mp3"')
        
        paths= ['videos/*', 'audio/*', 'merge/*']

        for path in paths:
            files = glob.glob(path)
            for f in files:
                try:
                    os.remove(f)
                except:
                    continue




        links= searchsongs(singer= singer)
        getsongs(links= links, n= noofvideos)
        getaudio(duration)
        mergeaudios('m.mp3')
        
        sendmail(mail= mailid, result= 'm.mp3')
        st.success('Mail sent successfully')
