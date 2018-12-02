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


