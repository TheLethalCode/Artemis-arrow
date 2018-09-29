import authentication as at
import youtube as yt
import songs as sg
import download as dd
from sys import argv

if __name__ == '__main__':
    
    service = at.get_authenticated_service()
    
    choice = input("Do you want to handle a file of songs or as single song? F/S ").strip().lower()
    choice_1 = input("\nWhich all operations do you want to perform? Enter space separated integers.\n\
                      1)Add songs to your youtube playlist\n\
                      2)Download the song\n\
                      3)Upload the songs to drive\n").split()
    if choice == 'f':
        song_file = input("File Name > ").strip()
        
        # Retrieves the names of the songs from the file
        songs = sg.song_extract(song_file)
        if '1' in choice_1:
            yt.youtube_add(service,songs,'f')
        if '2' in choice_1:
            dd.download_songs(service,songs,'f')    

    else:
        print("Enter 0 when done\n")
        while 1:
            song = input("Song Name > ").strip().lower()
            if song == '0':
                break
            if '1' in choice_1:
                yt.youtube_add(service,song,'s')
            if '2' in choice_1:
                dd.download_songs(service,song,'s')
        
    