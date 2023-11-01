from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

mailid=0

uri = f"mongodb+srv://{os.getenv('user')}:{os.getenv('pass')}@{os.getenv('url')}/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

collection = client['myGenrAI']['Users'] #'''fixed, no flask job here'''

def signup_func(f_name,l_name,mail,pasw):
    if collection.find_one({'mail':mail}):
        return False
    encpass = ''
    for char in pasw:
        encpass+=chr(ord(char)*10+5)
    collection.insert_one({
        'f_name':f_name,
        'l_name':l_name,
        'mail':mail,
        'pasw':encpass,
        'genre_dict':
            {
    'blues': 0, 'classical': 0, 'country': 0, 'disco': 0, 'hiphop': 0,
    'jazz': 0, 'metal': 0, 'pop': 0, 'reggae': 0, 'rock': 0
            }
    })
    return True

def decrypt(encpass):
    dec=''
    for char in encpass:
        dec+=chr((ord(char)-5)//10)
    return dec


def login(mail, pasw):
    global mailid
    mailid = mail
    if (doc:=collection.find_one({'mail':mail})) and (pasw == decrypt(doc['pasw'])):
        return 'Valid'
    if doc:
        return 'Incorrect password. Retry.'
    return "Account doesn't exist. Please sign up."

'''
Example of the attribute
genre_dict = {
    'blues': 3 # most
    'jazz': 1
    'hiphop': 2
    'rock': 0 # try new
}
'''

def update_preferences(genre): # Call this everytime the classification is done, the arguments are fed from website
    doc = collection.find_one({'mail': mailid})
    old_genre_dict = doc['genre_dict']
    old_genre_dict[genre]+=1
    collection.update_one({'mail': mailid}, {'$set': {'genre_dict': old_genre_dict}})


def new_ones():
    l = []
    doc = collection.find_one({'mail': mailid})
    old_genre_dict = doc['genre_dict']
    i = 3
    while i:
        i-=1
        key = min(old_genre_dict, key=old_genre_dict.get)
        del old_genre_dict[key]
        l.append(key)
    return l
