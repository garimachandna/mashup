import os
import glob
import sys
from youtubesearchpython import *
import youtube as yt
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
            yt.single_video(links[c], 'videos/')
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




def main():
    n = len(sys.argv)
    print(n)
    if(n!=5):
        print("Incorrect number of arguments\n")
        return


    singer= sys.argv[1]
    noofvideos= int(sys.argv[2])
    duration= int(sys.argv[3])
    outputfile= sys.argv[4]

    print(singer , noofvideos, duration, outputfile)
    
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
    mergeaudios(outputfile)


if __name__ == "__main__":
    main()