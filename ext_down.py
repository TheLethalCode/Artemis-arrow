from __future__ import unicode_literals
import youtube_dl
import os
import songs as sg
import authentication as at

def youtbe_dl_down(url,song,dir):
    """
    Downloads the song using youtbedl.
    Used as a last resort
    """

    # Sets destination and audio format
    options = {'format': 'bestaudio/best',
               'postprocessors': [{'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                     'preferredquality': '192',
                                }],
                'outtmpl': os.path.join(dir,song.title())+'.mp3',    
                'noplaylist' : True,   
            }
    
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    service = at.get_normal_service_y()
    song="faded"
    id = sg.video_id(service,song)
    dir = '.'
    youtbe_dl_down(id,song,dir)