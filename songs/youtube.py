import playlist as pl
import songs as sg
       
def single(service,playlist_id,song):
    
    """ 
    A single song is added to the playlist represented by the playlist id if it is not already present
    """

    song_id = sg.video_id(service,song)

    playlist_songs_id = pl.playlist_list(service,playlist_id)

    if song_id not in playlist_songs_id:
        pl.playlistItem_insert(service,playlist_id,song_id)
        print("Adding Song .....")
    
    else:
        print("Skipping song, song already in playlist")


