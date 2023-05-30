

from notion_client import Client
import datetime as dt
import requests, json
import oauth2

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.constants as NoteStoreConstants
from evernote.edam.notestore.ttypes import RelatedQuery, NoteFilter, NotesMetadataResultSpec
import evernote.edam.type.ttypes as Types
import os
from evernote.api.client import EvernoteClient
import os.path

#date = datetime.datetime.utcnow()
#utc_time = calendar.timegm(date.utctimetuple())
#print(utc_time)

notion = Client(auth="secret_Bic72FOFxzDyq62v2AYX4FiQAaT68hDRkR1VAxkqsWB")

headers = {
    "Authorization": "Bearer " + "secret_Bic72FOFxzDyq62v2AYX4FiQAaT68hDRkR1VAxkqsWB",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


#list_users_response = notion.users.list()
dev_token = "S=s1:U=96f72:E=18fa0bcec98:C=188490bc098:P=1cd:A=en-devtoken:V=2:H=752388ce896d31879e1ca90806abe9af"
everNote = EvernoteClient(token=dev_token)

userStore = everNote.get_user_store()
noteStore = everNote.get_note_store()


user = userStore.getUser()
#print(user)
#version_ok = userStore.checkVersion("Evernote EDAMTest (Python)", UserStoreConstants.EDAM_VERSION_MAJOR, UserStoreConstants.EDAM_VERSION_MINOR )


notebooks = noteStore.listNotebooks()
infoToInclude = NotesMetadataResultSpec(includeTitle=True, 
                                        includeContentLength=True, 
                                        includeCreated=None, 
                                        includeUpdated=None, 
                                        includeDeleted=None, 
                                        includeUpdateSequenceNum=None, 
                                        includeNotebookGuid=True, 
                                        includeTagGuids=None, 
                                        includeAttributes=True, 
                                        includeLargestResourceMime=True, 
                                        includeLargestResourceSize=None
                                        )
noteFilter = NoteFilter(order=None, ascending=None, words=None, notebookGuid="b68bbebd-9122-4b0e-9d29-e09fe192df8c", tagGuids=None, timeZone=None, inactive=None, emphasized=None)
notesMetadataList = noteStore.findNotesMetadata(dev_token, noteFilter, 0, 99999, infoToInclude)
print("Found ", len(notebooks), " notebooks:")
for notebook in notebooks:
    print("  * ", notebook.guid)
    
notesList = []    
resourceList = []    
"""
print()
print(notesMetadataList)
print("-------")
print(notesMetadataList.notes)
print("-------")
print(notesMetadataList.notes[0])
print("-------")
print(notesMetadataList.notes[0].guid)
print("-------")
"""

"""
spec = NoteResultSpec(includeContent=False,
        includeResourcesData=True,
        includeResourcesRecognition=False,
        includeResourcesAlternateData=False,
        includeSharedNotes=False,
        includeNoteAppDataValues=False,
        includeResourceAppDataValues=False,
        includeAccountLimits=False
        )
"""
for i in range(0, notesMetadataList.totalNotes):
    #notesList.append(notesMetadataList.notes[i].guid)
    """
    notesList.append(
        noteStore.getNote(
            notesMetadataList.notes[i].guid, 
            withContent=True, 
            withResourcesData=True, 
            withResourcesRecognition=False, 
            withResourcesAlternateData=False
            )
        )
    """
    notesList.append(
        noteStore.getNote(
            notesMetadataList.notes[i].guid, 
            True, 
            False, 
            False, 
            False
            )
        )
    resourceList.append(
        noteStore.getNote(
            notesMetadataList.notes[i].guid, 
            False, 
            True, 
            False, 
            False
            )
        )
    
for i in range(0, len(notesList)):
    #print(notesList[i])
    #f = open("newFile.jpg", "x")
    #f.close()
    #print("----------")
    try:
        print(str(notesList[i].resources[0].attributes.fileName))
        #f = open(str(notesList[i].resources[0].attributes.fileName), "w")
        print("|")

        save_path = "C:/Users/Ziddane/git/EverNotion/Files"

        completeName = os.path.join(save_path, str(notesList[i].resources[0].attributes.fileName))         
                
        file = open(completeName, "wb")
   
        # Write bytes to file
        file.write(resourceList[i].resources[0].data.body)
        file.close()
        #img = Image
        print("|")
        #f.close()
    except TypeError as e:
        print("no data in note: " + str(i+1))
    print("----------")
    print("----------")

    #print(notesMetadataList.notes[i].resources)

#print("Is my Evernote API version up to date? ", str(version_ok))

# -*- coding: utf-8 -*-
"""
Created on Sun May 28 01:27:36 2023

@author: Ziddane
"""


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from Google import Create_Service
import googledrive
import googleapiclient


from googleapiclient.discovery import build
from google.oauth2 import service_account

import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
  
  
  
# Define the SCOPES. If modifying it,
# delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/drive']
  
  

# Create a function getFileList with 
# parameter N which is the length of 
# the list of files.
def getFileList():
  
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None
  
    # The file token.pickle stores the 
    # user's access and refresh tokens. It is
    # created automatically when the authorization 
    # flow completes for the first time.
  
    # Check if file token.pickle exists
    if os.path.exists('token.pickle'):
  
        # Read the token from the file and 
        # store it in the variable creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
  
    # If no valid credentials are available, 
    # request the user to log in.
    if not creds or not creds.valid:
  
        # If token is expired, it will be refreshed,
        # else, we will request a new one.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
  
        # Save the access token in token.pickle 
        # file for future usage
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
  
    # Connect to the API service
    service = build('drive', 'v3', credentials=creds)
  
    # request a list of first N files or 
    # folders with name and id from the API.
    resource = service.files()
    result = resource.list(q="'1ikRaDORo-QyyfFE6J8Fj0_z6SGVnz8_E' in parents", fields="files(id, name)").execute()
  
    # return the result dictionary containing 
    # the information about the files
    return result
  
  
    
#CREATE
gauth = GoogleAuth()           
drive = GoogleDrive(gauth) 

path = "C:/Users/Ziddane/git/EverNotion/Files"
dir_list = os.listdir(path)
upload_file_list = dir_list

for upload_file in upload_file_list:
	gfile = drive.CreateFile({'parents': [{'id': '1ikRaDORo-QyyfFE6J8Fj0_z6SGVnz8_E'}]}) #CREATES FILE
	# Read file and set it as the content of this instance.
	gfile.SetContentFile(os.path.join(path, upload_file))
	gfile.Upload() # Upload the file.


#"""
CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
#CREATE


# Get list of first 5 files or 
# folders from our Google Drive Storage
result_dict = getFileList()
  
  
  
# Extract the list from the dictionary
file_list = result_dict.get('files')
  
  
  
# Print every file's name
for file in file_list:
    print(file['id'])




# Load credentials from the JSON file you downloaded


for file in file_list:
    # Update Sharing Setting
    file_id = file['id']
    
    request_body = {
        'role': 'reader',
        'type': 'anyone'
    }
    
    file_name = file['name']
    
    response_permission = service.permissions().create(
        fileId=file_id,
        body=request_body
    ).execute()
    
    #print(response_permission)
    
    
    # Print Sharing URL
    response_share_link = service.files().get(
        fileId=file_id,
        fields='webViewLink'
    ).execute()
    
    print(response_share_link.get('webViewLink'))
    
    # Remove Sharing Permission
    service.permissions().delete(
        fileId=file_id,
        permissionId='anyoneWithLink'
    ).execute()


    url = "https://api.notion.com/v1/pages"
    
    payload = {
        "parent": {
            "type": "database_id",
            "database_id": "156e3e8693964e94b43dc067ba410d61"
        },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": file_name[38: -4]
                        }
                    }
                ]
            }
     
    
        }, 
        "children": [
            {
                "object": "block",
                "heading_2": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Google Drive link to content"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "paragraph": {
                    "rich_text": [
                        {
                            "text": {
                                "content": response_share_link.get('webViewLink'),
                                "link": {
                                    "url": response_share_link.get('webViewLink')
                                }
                            },
                            "href": response_share_link.get('webViewLink')
                        }
                    ],
                    "color": "default"
                }
            }
        ]
        
    }
    
    headers = {
        "Authorization": "Bearer " + "secret_Bic72FOFxzDyq62v2AYX4FiQAaT68hDRkR1VAxkqsWB",
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json"
    }
    
    
    response = requests.post(url, json=payload, headers=headers)
    #print(response.text)