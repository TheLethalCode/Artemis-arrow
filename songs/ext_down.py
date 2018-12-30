import youtube_dl
import os
import requests as rq
from dotenv import load_dotenv


def youtbe_dl_down(url,song):

    """
    Downloads the song using youtbedl.
    Used as a last resort
    """

    SONG_DIR = os.path.join(os.path.dirname(__file__),'Songs')
    FILE =  os.path.join(SONG_DIR,song.title())+'.mp3'

    options = {'format': 'bestaudio/best',
               'postprocessors': [{'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                     'preferredquality': '192',
                                }],
                'outtmpl': FILE,    
                'noplaylist' : True,   
            }
    
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([url])

    return FILE


def video_id(songname):

    SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
    API_KEY = os.getenv("API_KEY")

    """
    Searches for the song and returns the VideoID
    """

    if "song" in songname.lower():
        SongName = songname.lower()
    else:
        SongName = songname.lower() + " song"

    payload = {
        "part" : "snippet,id",
        "q" : SongName,
        "type" : "video",
        "maxResults" : "10",
        "key" : API_KEY
    }

    results = rq.get(SEARCH_URL,payload)
    songs = [{ "title" : result["snippet"]["title"],
                "id" : result["id"]["videoId"]
            } for result in results.json()["items"] ]

    return songs
    # print(songs)


if __name__ == '__main__':
    load_dotenv()
    print(video_id("end game"))