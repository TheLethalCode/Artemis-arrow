import authentication as at
import youtube as yt
import songs as sg
import download as dd
from sys import argv

if __name__ == '__main__':
    
    choice = input("Do you want to handle a file of songs or as single song? F/S ").strip().lower()
    choice_1 = input("\nWhich all operations do you want to perform? Enter space separated integers.\n\
                      1)Add songs to your youtube playlist\n\
                      2)Download the song\n\
                      3)Upload the songs to drive\n").split()
    
    if '1' in choice_1:
        youtube = at.get_authenticated_service_y()
    else:
        youtube = at.get_normal_service_y()

    if choice == 'f':
        song_file = input("File Name > ").strip()
        
        # Retrieves the names of the songs from the file
        songs = sg.song_extract(song_file)
        if '1' in choice_1:
            yt.youtube_add(youtube,songs,'f')
        if '2' in choice_1:
            dd.download_songs(youtube,songs,'f')    

    else:
        print("Enter 0 when done\n")
        while 1:
            song = input("Song Name > ").strip().lower()
            if song == '0':
                break
            if '1' in choice_1:
                yt.youtube_add(youtube,song,'s')
            if '2' in choice_1:
                dd.download_songs(youtube,song,'s')
        
    