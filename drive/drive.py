import os
import flask
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage 
from apiclient import errors
from apiclient.http import MediaFileUpload



@app.route('/')
def index():
	credentials = get_credentials()
	if credentials == False:
		return flask.redirect(flask.url_for('oauth2callback'))
	elif credentials.access_token_expired:
		return flask.redirect(flask.url_for('oauth2callback'))
	else:
		return


@app.route('/oauth2callback')
def oauth2callback():
	flow = client.flow_from_clientsecrets('client_id.json',
			scope='https://www.googleapis.com/auth/drive',
			redirect_uri=flask.url_for('oauth2callback', _external=True)) # access drive api using developer credentials
	flow.params['include_granted_scopes'] = 'true'
	if 'code' not in flask.request.args:
		auth_uri = flow.step1_get_authorize_url()
		return flask.redirect(auth_uri)
	else:
		auth_code = flask.request.args.get('code')
		credentials = flow.step2_exchange(auth_code)
		open('credentials.json','w').write(credentials.to_json()) # write access token to credentials.json locally 
		return flask.redirect(flask.url_for('index'))



def get_credentials():
	credential_path = 'credentials.json'

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		print("Credentials not found.")
		return False
	else:
		print("Credentials fetched successfully.")
		return credentials



def insert_file(service, title, description, parent_id, mime_type, filename):
  """Insert new file.

  Args:
    service: Drive API service instance.
    title: Title of the file to insert, including the extension.
    description: Description of the file to insert.
    parent_id: Parent folder's ID.
    mime_type: MIME type of the file to insert.
    filename: Filename of the file to insert.
  Returns:
    Inserted file metadata if successful, None otherwise.
  """
  media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
  body = {
    'title': title,
    'description': description,
    'mimeType': mime_type
  }
  # Set the parent folder.
  if parent_id:
    body['parents'] = [{'id': parent_id}]

  try:
    file = service.files().insert(
        body=body,
        media_body=media_body).execute()

    # The following line prints the file id
    print 'File ID: %s' % file['id']

    return file
  except errors.HttpError, error:
    print 'An error occurred: %s' % error
    return None




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
    	if os.path.exists('client_id.json') == False:
		print('Client secrets file (client_id.json) not found in the app path.')
		exit()
	
	    
	
