import authentication as at
import youtube as yt
import songs as sg

if __name__ == '__main__':
    
    service = at.get_authenticated_service()
    
    choice = input("\nDo you want to handle a file of songs or a single song? F/S ").strip().lower()

    if choice == 'f':
        song_file = input("File Name > ").strip()
        
        # Retrieves the names of the songs from the file
        songs = sg.song_extract(song_file)
        yt.youtube_add(service,songs,'f')

    else:
        song = input("Song Name > ").strip().lower()
        yt.youtube_add(service,song,'n')

    
    