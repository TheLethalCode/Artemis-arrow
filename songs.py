def video_id(service,songname):
    """
    Searches for the song and returns the VideoID
    """
    if "song" in songname:
        SongName = songname
    else:
        SongName = songname + " song"
    song = service.search().list(part="snippet,id",q=SongName,type="video").execute()["items"][0]
    return song["id"]["videoId"]

def song_extract(filename):
    """
    Reads a file of songs and returns a list of song names
    """
    s_f =  open(filename,'r',encoding='utf-8')
    songs = []
    while True:
        song = s_f.readline()
        if not song:
            break
        songs.append(song.strip())
    s_f.close()
    return songs