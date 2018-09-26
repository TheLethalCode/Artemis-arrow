import playlist as pl
import authentication as at
import songs as sg

def file_ch(service,playlist_id):
    """ 
    A multitude of songs in a file is added to the playlist represented by the 
    playlist id if it is not already present.
    """

    song_file = input("File Name > ").strip()
    songs = sg.song_extract(song_file)
    
    print("Do you want to add %d songs to your playlist? Y/N" % len(songs))
    choice =  input().lower().strip()

    if choice != 'y':
        exit(0)

    playlist_songs_id = pl.playlist_list(service,playlist_id)

    for ind,song in enumerate(songs):
        song_id = sg.video_id(service,song.lower())
        
        if song_id not in playlist_songs_id:
            pl.playlistItem_insert(service,playlist_id,song_id)
            playlist_songs_id.append(song_id)
            print("Adding song %d %s" % (ind+1,song))
        else:
            print("Skipping song %d %s" % (ind+1,song) )
        
def single(service,playlist_id):
    
    """ 
    A single song is added to the playlist represented by the playlist id if it is not already present
    """

    song = input("Song Name > ").strip().lower()
    song_id = sg.video_id(service,song)

    playlist_songs_id = pl.playlist_list(service,playlist_id)

    if song_id not in playlist_songs_id:
        pl.playlistItem_insert(service,playlist_id,song_id)



if __name__ == '__main__':
    
    service = at.get_authenticated_service()
    
    playlist = input("Playlist Name > ").strip().lower().capitalize()
    playlist_id = pl.extract_playlist_id(service,playlist)

    choice = input("\nA file of songs or a single song? F/S ").strip().lower()

    if choice == 'f':
        file_ch(service,playlist_id)
    else:
        single(service,playlist_id)

    