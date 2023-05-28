# -*- coding: utf-8 -*-
"""
Created on Wed May 17 09:22:50 2023

@author: Owner
"""
from PIL import Image

from notion_client import Client
import datetime as dt
import requests, json
import oauth2

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.constants as NoteStoreConstants
from evernote.edam.notestore.ttypes import RelatedQuery, NoteFilter, NotesMetadataResultSpec
import requests
import evernote.edam.type.ttypes as Types
import os
from evernote.api.client import EvernoteClient
#date = datetime.datetime.utcnow()
#utc_time = calendar.timegm(date.utctimetuple())
#print(utc_time)

notion = Client(auth="secret_Bic72FOFxzDyq62v2AYX4FiQAaT68hDRkR1VAxkqsWB")
#list_users_response = notion.users.list()
dev_token = "S=s1:U=96f72:E=18fa0bcec98:C=188490bc098:P=1cd:A=en-devtoken:V=2:H=752388ce896d31879e1ca90806abe9af"
everNote = EvernoteClient(token=dev_token)

userStore = everNote.get_user_store()
noteStore = everNote.get_note_store()


user = userStore.getUser()
print(user)
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
    print(notesList[i])
    f = open("test.txt", "w")

    print("----------")
    try:
        print(str(notesList[i].resources[0].attributes.fileName))
        f = open(str(notesList[i].resources[0].attributes.fileName), "w")
        print("|")
        #img = PIL.Image.frombytes("RGBA", (notesList[i].resources[0].width, notesList[i].resources[0].height), resourceList[i])
        img = Image
        print("|")
        f.close()
    except TypeError as e:
        print("no data in note: " + str(i+1))
    print("----------")
    print("----------")

    #print(notesMetadataList.notes[i].resources)

#print("Is my Evernote API version up to date? ", str(version_ok))
