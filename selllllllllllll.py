import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from collections import OrderedDict
import numpy as np
from dotenv import load_dotenv
import base64
import json
load_dotenv()
import os
firebase_credentials_path_64 = os.getenv('FIREBASE_CREDENTIALS_PATH')
firebase_credentials_path=json.loads(base64.b64decode(firebase_credentials_path_64))
cred = credentials.Certificate(firebase_credentials_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://amgaaa-999fd-default-rtdb.asia-southeast1.firebasedatabase.app/contestant'})
ref=db.reference(path='contestant')
data=ref.get()
player_names = [entry.get('name') for entry in data]
rating=[entry.get('elo') for entry in data]
print(player_names)
def name_details(a,b):
    query=ref.order_by_child('name').equal_to(a)
    query1=ref.order_by_child('name').equal_to(b)
    for i in query.get().values():
        print(type(i))
    for j in query1.get().values():
        print(type(i))
    query_elo=i['elo']
    query1_elo=j['elo']
    query_img=i['image_path']
    query1_img=j['image_path']
    return query_elo,query1_elo,query_img,query1_img
def update_rating(id,new_rating):
    celeb=db.reference(path=f'contestant/{id}')
    celeb.update({
        "elo":new_rating
    })
