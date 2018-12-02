import authentication as at 

def folder_id(service,name):

    ID = None

    results = service.files().list(pageSize=1000, 
                            fields="nextPageToken, files(id, name, mimeType, \
                            ownedByMe, parents, size)"
                            ).execute()

    while True:

        for files in results.get('files',[]):
            if files['ownedByMe'] and files["mimeType"] == "application/vnd.google-apps.folder":
                if files['name'].lower() == name.lower():
                    ID = files['id']
                    break

        if results.get('nextPageToken') and not ID:
                results = service.files().list(pageSize=1000, pageToken=results['nextPageToken'], \
                fields="nextPageToken, files(id, name, mimeType, ownedByMe, parents, size)").execute()
        else:
            break

    return ID

if __name__ == '__main__':
    drive = at.get_authenticated_service_d()
    print(folder_id(drive,"music"))