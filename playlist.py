import authentication as at

def build_resource(properties):
    """
    This builds the body listed by the properties which can further be
    used to update the body of a playlist, playlistitem, etc.
    """  
    resource = {}
    for p in properties:
        prop_array = p.split('.')
        ref = resource
        for pa in range(0, len(prop_array)):
            is_array = False
            key = prop_array[pa]
            if key[-2:] == '[]':
                key = key[0:len(key)-2:]
                is_array = True
            if pa == (len(prop_array) - 1):
                if properties[p]:
                    if is_array:
                        ref[key] = properties[p].split(',')
                    else:
                     ref[key] = properties[p]
            elif key not in ref:
                ref[key] = {}
                ref = ref[key]
            else:
                ref = ref[key]
    return resource

def playlistItem_delete(service,did):
    """
    Deletes an item in the playlist represented by the playlistid
    """
    service.playlistItems().delete(id=did).execute()

def playlistItem_insert(service,playlistId,videoId,kind="youtube#video"):
    """
    Inserts a particular video(videoId) into a playlist (playlistId)
    """
    properties={}
    properties["snippet.playlistId"], properties["snippet.resourceId.kind"] = playlistId, kind
    properties["snippet.resourceId.videoId"] = videoId
    resource = build_resource(properties)
    service.playlistItems().insert(body=resource,part="snippet").execute()

def create_playlist(service,Name):
    """
    Creates a new playlist by the given name and returns its ID
    """
    newplaylist = {}
    newplaylist["snippet.title"], newplaylist["status.privacyStatus"] = Name, "private"
    resource = build_resource(newplaylist)
    return service.playlists().insert(body=resource,part="snippet,status").execute()["id"]

def delete_playlist(service,did):
    """
    Deletes a playlist by the represented id
    """
    service.playlists().delete(id=did).execute()

def extract_playlist_id(service,playlistName,no=0):
    
    """
    Finds the ID of the playlist of the given name. If it is not present,
    it creates a new one of the same
    """

    PlayID = None

    responses = service.playlists().list(part="snippet",mine=True,maxResults=50).execute()
    playlists = responses["items"]
    while True:
        for playlist in playlists:
            if playlist["snippet"]["title"].lower().title() == playlistName:
                PlayID = playlist["id"]
                break
        if PlayID == None and ("nextPageToken" in responses):
            responses = service.playlists().list(part="snippet",
                                                mine=True,
                                                maxResults=50,
                                                pageToken=responses["nextPageToken"]).execute()
            playlists = responses["items"]
        else:
            break
            
    if PlayID == None and not no:
        ans = input("\nNo playlist found with the given name. Do you want to create a new one? y/n ").strip().lower()
        if ans == 'y':
            PlayID = create_playlist(service,playlistName)
            print("\nCreated new playlist")
        else:
            exit(0)

    return PlayID

def playlist_list(service,playlist_id):

    """
    Returns the VideoID of all songs in the playlist
    """

    responses =  service.playlistItems().list(part="snippet",playlistId=playlist_id,maxResults=50).execute()
    song_ids=[]
    while True:
        temp_id = [songs["snippet"]["resourceId"]["videoId"] for songs in responses["items"]]
        song_ids= song_ids + temp_id
        if "nextPageToken" in responses:
            responses=service.playlistItems().list(part="snippet",
                                                    playlistId=playlist_id,
                                                    maxResults=50,
                                                    pageToken=responses["nextPageToken"]).execute()
        else:
            break
    return song_ids

if __name__ == '__main__':

    service =  at.get_authenticated_service_y()
    id = extract_playlist_id(service,"Mine",1)
    delete_playlist(service,id)