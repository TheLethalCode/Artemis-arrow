import songs as sg
import requests as rq
import authentication as at
import os
import time
import ext_down as ed

def find_files(dir_name):
    """
    Finds all mp3 files present in the directory
    """
    songs=[]
    directory = os.fsencode(dir_name)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".mp3"): 
            songs.append(filename.split('.')[-2].lower())
    return songs

def generate_body(page):
    """
    Generates the data for POST request
    """
    body={}
    body["type"]="youtube"
    ini = page.find("_id:")
    fin = page.find("mp3",ini)
    id, vid,ext = page[ini:fin-1].split(',')
    body["_id"],body["v_id"] = id.strip().split(':')[-1].strip()[1:-1] , vid.strip().split(':')[-1].strip()[1:-1]
    body["mp3_type"]=256
    return body

def generate_link(page):
    """
    Generates the link to the audio file
    """
    ind=page.find("http")
    fin=page.find('"',ind)
    return page[ind:fin]

def download_song(service,song,id,dir_name):
    """
    Downloads the song and stores it in a file
    """

    # URL's
    URL_Page = "https://y2mate.com/mp3/ajax"
    URL_Conv = "https://y2mate.com/mp3Convert"
    url = "https://www.youtube.com/watch?v=" + id
    
    # Takes care of generation of the query body
    while True :
        try:
            res = rq.post(URL_Page,{"url":url,"ajax":1})
            body=generate_body(res.json()["result"])
            print("Generated body")
            break

        except (KeyboardInterrupt,ValueError):
            raise

        except:
            # When the conversion takes time
            time.sleep(0.5)
            pass
    
    # Generates download link
    while True :
        try:         
            ans = rq.post(URL_Conv,body)
            wle = ans.json()["result"]

            # When the song not available in that format
            if wle[2] == 't':
                raise KeyError
            
            LINK = generate_link(wle)
            resp = rq.get(LINK,stream=True)
            
            # When conversion not possible
            if resp.headers['Content-Type'] != 'audio/mpeg':
                raise KeyError

            print("Generated Link")
            break
        
        except KeyError:
            # If 128 format not available, it looks for alternative
            if body["mp3_type"]==128:
                raise ValueError            
            else:
                body["mp3_type"]=128

        except KeyboardInterrupt:
            raise
        
        # except ValueError:
        #     print("Server throttling connection")
        #     time.sleep(1)
        #     pass

    # Size of the file
    size=int(resp.headers["Content-Length"])
    down_size = 0 

    fil = open(os.path.join(dir_name,song.title()+".mp3"),"wb")
    print("STARTING DOWNLOAD")
    for data in resp.iter_content(chunk_size=100000):
        if data:
            fil.write(data)
            down_size+=100000
            percent = min((down_size*100)/size,100)
            print("DOWNLOADED %.1f/100" % percent,end='\r')

def download_songs(service,songs,choice):
    """
    Downloads a group or a single song and stores it in the 
    specified directory if it is not already present
    """

    # Takes the name of the directory
    dir_name = input("Enter the path to the directory where you want to store the songs:-\
    \n('.' for the current directory)\n").strip()
    if not os.path.exists(dir_name):
        ex_songid = []
        cho = input("The requested directory does not exist. Do you want to create one? Y/N").strip().lower()
        if cho=='y':
            os.makedirs(dir_name)
        else:
            exit(0)
    
    else:
        # Retrieves the ids of already existing songs
        ex_songs = find_files(dir_name)
        print("Retrieving the ids of %d songs already in the directory...." % len(ex_songs),end='\r')
        while True:
            ex_songid = []
            try:
                for song in ex_songs:
                    ex_songid.append(sg.video_id(service,song))
                break
            except KeyboardInterrupt:
                raise
            except:
                pass
        print("Retrieved and ids generated succesfully"," "*10,"\n")
    
    done = 0
    fl=0
    while True:
        try:
            temp = done

            # Takes care of a file of songs
            if choice=='f':
                for ind,song in enumerate(songs[temp:]):
                    id = sg.video_id(service,song,fl)
                    if id not in ex_songid:
                        print("Downloading song %d ......" % (ind+1+temp))
                        download_song(service,song,id,dir_name)
                        print("Downloaded song %d    \n" % (ind+1+temp))

                    else:
                        print("Skipping song %d, song already present" % (ind+1+temp))
                    done+=1
                    fl=0
            
            # Takes care of a single song        
            else:
                if done:
                    break
                id = sg.video_id(service,songs)
                song = songs
                if id not in ex_songid:
                    print("Downloading song ......")
                    download_song(service,songs,id,dir_name)
                    print("\nDownloaded song     \n")
                else:
                    print("Skipping song, song already present")
            break
        
        except KeyboardInterrupt:
            raise
        
        except ValueError:      #Control comes here when the song conversion is not available
            
            # Uses youtube_dl to download
            if fl == 1:
                print("Unexpected error...Using external agent.")
                ed.youtbe_dl_down(id,song,dir_name)
                print("Downloaded song %d    \n" % (ind+1+temp))
                fl=0
                done=done+1

            # Trying the next suggestion in the youtube search query
            else:
                print("Cannot download audio...Trying alternative")
                fl=1

if __name__ == '__main__':
    service = at.get_authenticated_service()
    songs = sg.song_extract("Songs.txt")
    download_songs(service,songs,'f')