import requests
import json
import tqdm
import pandas as pd
from collections import Counter
from bs4 import BeautifulSoup

"""
The following code is inspired by the work of W. Soares:

https://dev.to/willamesoares/how-to-integrate-spotify-and-genius-api-to-easily-crawl-song-lyrics-with-python-4o62
"""


class GeniusParser():
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://api.genius.com'
        self.search_url = self.base_url + '/search'
        self.headers = {'Authorization': 'Bearer ' + self.token}

    def test_token(self):
        data = {'q': f'"Kaaris"'}
        test = requests.get(self.search_url, data=data,headers=self.headers).json()
        if 'error_description' in test:
            raise Exception(test['error_description'])
        else:
            print("Valid access token provided !")

    def get_artist_id(self, artist):
        data = {'q': f'"{artist}"'}
        find_id = requests.get(self.search_url, data=data,
                               headers=self.headers).json()
        list_artists_id = []
        for hit in find_id["response"]["hits"]:
            if hit["result"]["primary_artist"]["name"].lower() == artist.lower():
                list_artists_id.append(hit["result"]["primary_artist"]["id"])
        try:
            return Counter(list_artists_id).most_common(1)[0][0]
        except:
            raise Exception(f"Error 'id not found': {artist} !")

    def get_song_info(self, artist_name, song_title):
        data = {'q': song_title + ' ' + artist_name}
        response = requests.get(
            self.search_url, data=data, headers=self.headers)
        return response

    def scrap_song_url(self, url):
        page = requests.get(url)
        html = BeautifulSoup(page.text, 'html.parser')
        classes = [value for element in html.find_all(
            class_=True) for value in element["class"]]
        classes = [x for x in classes if 'lyrics' in x.lower()]

        lyrics = ''
        for class_ in classes:
            lyrics += html.find('div', class_=class_).get_text()
            return lyrics

    def get_lyrics(self, artist_name, song_title):
        response = self.get_song_info(artist_name, song_title)
        remote_song_info = response.json()['response']['hits']
        song_url = remote_song_info[0]['result']['url']
        for _ in range(100):
            song_lyrics = self.scrap_song_url(song_url)
            if '\n' in song_lyrics:
                return song_lyrics
        raise Warning(f"Error 'scrap_song_url': {song_url} !!")

    def get_artist_songs(self, id, params):
        search = self.base_url + f'/artists/{id}/songs'
        response = requests.get(
            search, params=params, headers=self.headers)
        response_json = json.loads(response.content.decode('utf-8'))
        artist_songs = [song['title'] for song in response_json['response']['songs']
                        if song['primary_artist']['id'] == id]
        return artist_songs

    def create_dict_artists(self, list_artists=['Booba']):
        self.list_artists = list_artists
        self.dict_artists = {
            artist: {
                "id": self.get_artist_id(artist),
                "list_songs": [],
                "lyrics": {}
            } for artist in list_artists
        }

        for artist in self.list_artists:
            if not self.dict_artists[artist]['id']:
                self.dict_artists.pop(artist)

    def search_for_songs(self, nb_page=10, per_page=1):
        for artist_name in tqdm.tqdm(self.dict_artists):
            list_songs = []
            for i in range(nb_page):
                params = {
                    'sort': 'popularity',
                    'per_page': per_page,
                    'page': i+1
                }
                list_songs += self.get_artist_songs(
                    self.dict_artists[artist_name]['id'], params)
            self.dict_artists[artist_name]['list_songs'] = list(
                pd.unique(list_songs))

    def search_for_lyrics(self, ):
        for artist_name in self.dict_artists:
            for song_title in tqdm.tqdm(self.dict_artists[artist_name]['list_songs']):
                self.dict_artists[artist_name]['lyrics'][song_title] = self.get_lyrics(artist_name, song_title)

    def export(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.dict_artists, f)