##################################################################
####################### Name: Jin-Seo Bae ########################
####################### Uniqname: jinbae  ########################
##################################################################

from bs4 import BeautifulSoup
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import csv
import sqlite3

CLIENT_ID = "15f49feff96d484488c85b03315cdd41"
SECRET_CLIENT_ID = "a55595dd478d4c72b004b9f5c3a81b9e"

#Getting Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=SECRET_CLIENT_ID)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

######CACHE#####
CACHE_FILE_NAME = 'cache.json'
CACHE_DICT = {}

def load_cache(): 
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

def save_cache(cache): 
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()

def make_url_request_using_cache(url, cache):
    if (url in cache.keys()): 
        print("Using cache")
        return cache[url]     
    else:
        print("Fetching")
        response = requests.get(url) 
        cache[url] = response.text 
        save_cache(cache)          
        return cache[url]          

CACHE_DICT = load_cache()

######SCRAPE TOP 100 SONGS FROM BILLBOARD WEBSITE#####
title_list = []
artist_list = []
ranking_list = []
number_of_hits = []

url = "https://www.billboard.com/charts/hot-100"

html = make_url_request_using_cache(url, CACHE_DICT)
soup = BeautifulSoup(html, 'html.parser')

titles_of_songs = soup.find_all('span',class_="chart-element__information__song text--truncate color--primary")
artists_names = soup.find_all('span',class_="chart-element__information__artist text--truncate color--secondary")
ranking = soup.find_all('span',class_="chart-element__rank__number")

for title in titles_of_songs:
    name = title.text
    title_list.append(name)

for name in artists_names:
    artist = name.text
    artist_list.append(artist)

for i in ranking:
    rank = i.text
    ranking_list.append(rank)

for x in range(0,100):
    total_list={}
    total_list['track_name']= title_list[x]
    total_list['artist_name'] = artist_list[x]
    total_list['rank'] = x + 1
    number_of_hits.append(total_list)

#####GETING TOP SONGS FROM SPOTIFY BY USING ITS API AND SAVE IT AS CSV FILE#####
def get_spotify_csv():
    artistName = []
    trackTitle = []
    ID = []
    popularity = []
    for i in range(0, 10):
        for name in artist_list:
            track_results = sp.search(name) #connecting with spotify API
            for i, t in enumerate(track_results['tracks']['items']):
                artistName.append(t['artists'][0]['name'])
                trackTitle.append(t['name'])
                ID.append(t['id'])
                popularity.append(t['popularity'])

    spotifyDB = pd.DataFrame({'artist_name':artistName,'track_name':trackTitle,'track_id':ID,'popularity':popularity})
    spotifyDB.to_csv('top_spotify.csv') 

#get_spotify_csv()
#If I uncomment above code, then it will get current top spotify songs using Spotify API
#It took forever so I decided to download just once and use this file to complete this project.
#If you want to try to download the file, you can download it by uncommenting "get_spotify_csv()".



#####DATABASE FOR BOTH SPOTIFY AND BILLBOARD####
def create_SpotifyTracks():

    conn= sqlite3.connect("song_track.sqlite")
    cur = conn.cursor()

    create_tracks = '''
        CREATE TABLE "SpotifyTracks" (
            "track_name" TEXT,
            "artist_name" TEXT,
            "track_id" TEXT PRIMARY KEY NOT NULL,
            "popularity" INTEGER
        )
    '''
    
    cur.execute(create_tracks)

    spotifyDB = pd.read_csv('top_spotify.csv', index_col=0)
    spotifyDB.drop_duplicates(subset=['track_name'],inplace=True)

    drop_tracks_sql = 'DROP TABLE IF EXISTS "SpotifyTracks"'
    cur.execute(drop_tracks_sql)

    spotifyDB.to_sql('SpotifyTracks', conn, if_exists='append', index=False) #Change csv file to database
    conn.commit()
    conn.close()

create_SpotifyTracks()

def create_BillboardTracks():
    conn = sqlite3.connect("song_track.sqlite")
    cur = conn.cursor()
    drop_BillboardTracks_sql = 'DROP TABLE IF EXISTS "BillboardTracks"'
    
    create_BillboardTracks_sql = '''
        CREATE TABLE IF NOT EXISTS "BillboardTracks" (
            "Track_Name" TEXT NOT NULL, 
            "Artist_Name" TEXT NOT NULL,
            "Rank" INTEGER PRIMARY KEY NOT NULL
        )
    '''
    cur.execute(drop_BillboardTracks_sql)
    cur.execute(create_BillboardTracks_sql)
    conn.commit()
    conn.close()

create_BillboardTracks()  


def load_BillboardTracks():
    conn = sqlite3.connect("song_track.sqlite")
    cur = conn.cursor()

    insert_hits_sql = '''
        INSERT INTO BillboardTracks
        VALUES (?, ?, ?)
    '''
    
    for number in number_of_hits: #using previously created list by scraping billboard website
        cur.execute(insert_hits_sql,
        [
            number['track_name'],
            number['artist_name'],
            number['rank'],
        ]
        )
    conn.commit()
    conn.close()

load_BillboardTracks() 