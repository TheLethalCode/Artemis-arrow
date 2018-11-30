def video_id(service,songname,no=0):
    """
    Searches for the song and returns the VideoID
    """

    if "song" in songname.lower():
        SongName = songname.lower()
    else:
        SongName = songname.lower() + " song"
    song = service.search().list(part="snippet,id",q=SongName,type="video").execute()["items"][no]
    return song["id"]["videoId"]

def song_extract(filename):
    """
    Reads a file of songs and returns a list of song names
    """
    try:
        s_f =  open(filename,'r',encoding='utf-8')
    except:
        print("Cannot open file.")
        exit(0)
    
    songs = []
    while True:
        song = s_f.readline()
        if not song:
            break
        songs.append(song.strip())
    s_f.close()
    return songs