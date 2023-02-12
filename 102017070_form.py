import os
import glob
import sys
from youtubesearchpython import *
#import youtube as yt
import os
import moviepy.editor as mp
from moviepy.editor import concatenate_audioclips, AudioFileClip
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pytube import YouTube 

def sendmail(mail, result):
        
    fromaddr = "gchandna4@gmail.com"
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
    s.login("gchandna4@gmail.com", "btqrvroxddqbqggk")

    # message to be sent
    message = msg.as_string()

    # sending the mail
    s.sendmail("gchandna4@gmail.com", mail,  message)

    # terminating the session
    s.quit()
    print( '\n\n\nMail sent successfully')



def searchsongs(singer):

    customSearch = VideosSearch(singer)

    l = len(customSearch.result()['result'])
    links= []
    for i in range(l):
        links.append(customSearch.result()['result'][i]['link'])

    return links


def getsongs(links, n):
    c=0
    while c < min(n, len(links)):
        try:
            yt = YouTube(links[c]) 
            yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download('videos/')

            c=c+1
        except Exception as e:
           # print(e)
           continue


def getaudio(y):
    # Python code to convert video to audio
    # Insert Local Video File Path
    for file in os.listdir('videos'):
        try:
            clip = mp.VideoFileClip(os.path.join('videos', file)).subclip(0,y)

            # Insert Local Audio File Path
            clip.audio.write_audiofile(os.path.join('audio', f"Audio {file}"), codec= 'libmp3lame')
            print()
        except Exception as e:
          #  print(e)
            continue


def mergeaudios(output_path):
    """Concatenates several audio files into one audio file using MoviePy
    and save it to `output_path`. Note that extension (mp3, etc.) must be added to `output_path`"""

    audio_clip_paths = glob.glob('audio/*')
    clips = [AudioFileClip(c) for c in audio_clip_paths]
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_path, codec= 'libmp3lame')




def main():
    n = len(sys.argv)
    if(n!=5):
        print( "Incorrect number of arguments\n")
        return '', 0, 0


    singer= sys.argv[1]
    noofvideos= sys.argv[2]
    duration= sys.argv[3]
    mailid= sys.argv[4]
    
    paths= ['videos/*', 'audio/*', 'merge/*']

    for path in paths:
        files = glob.glob(path)
        for f in files:
            try:
                os.remove(f)
            except:
                continue



    links= searchsongs(singer= singer)
    getsongs(links= links, n= int(noofvideos))
    getaudio(int(duration))
    mergeaudios('m.mp3')
    sendmail(mail= mailid, result= 'm.mp3')

if __name__ == "__main__":
    x= main()
