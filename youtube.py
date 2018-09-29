import playlist as pl
import songs as sg

def file_ch(service,playlist_id,songs):
    """ 
    A multitude of songs in a file is added to the playlist represented by the 
    playlist id if it is not already present.
    """
    
    print("Do you want to add %d songs to your playlist? Y/N" % len(songs))
    choice =  input().lower().strip()

    if choice != 'y':
        exit(0)
    
    # Retrieves Ids of already existing songs in the playlist
    playlist_songs_id = pl.playlist_list(service,playlist_id)

    for ind,song in enumerate(songs):
        song_id = sg.video_id(service,song.lower())
        
        if song_id not in playlist_songs_id:
            pl.playlistItem_insert(service,playlist_id,song_id)
            playlist_songs_id.append(song_id)
            print("Adding song %d %s" % (ind+1,song))
        else:
            print("Skipping song %d %s" % (ind+1,song) )
        
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

def youtube_add(service,name,choice):
    
    """
    Adds songs to youtube playlist
    """

    playlist = input("Playlist Name > ").strip().lower().title()
    playlist_id = pl.extract_playlist_id(service,playlist)

    if choice == 'f':
        file_ch(service,playlist_id,name)
    else:
        single(service,playlist_id,name)        

