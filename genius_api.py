import requests
import json
from bs4 import BeautifulSoup
import settings

# heavily inspired by https://dev.to/willamesoares/how-to-integrate-spotify-and-genius-api-to-easily-crawl-song-lyrics-with-python-4o62
# thanks to https://github.com/willamesoares


class GeniusApi:

    def request_song_info(self, song_title, artist_name):
        base_url = 'https://api.genius.com'
        headers = {'Authorization': 'Bearer ' + settings.GENIUS_ACCESS_TOKEN}
        search_url = base_url + '/search'
        data = {'q': song_title + ' ' + artist_name}
        response = requests.get(search_url, data=data, headers=headers)
        # f = open("response.json", "w")
        # f.write(json.dumps(response.json()))

        return response

    def get_remote_song_url(self, song_title, artist_name):
        # Search for matches in the request response
        response = self.request_song_info(song_title, artist_name)
        json = response.json()
        remote_song_info = None

        for hit in json['response']['hits']:
            if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                remote_song_info = hit
                break

        # Extract lyrics from URL if the song was found
        if remote_song_info:
            song_url = remote_song_info['result']['url']

        return song_url

    def get_song_lyrics_from_url(self, url):
        page = requests.get(url)
        html = BeautifulSoup(page.text, 'html.parser')
        lyrics = html.find('div', class_='lyrics').get_text()

        return lyrics

    def get_lyrics_from_artist_and_title(self, song_title, artist_name):
        url = self.get_remote_song_url(song_title, artist_name)
        lyrics = self.get_song_lyrics_from_url(url)

        return lyrics


if __name__ == "__main__":
    genius_api = GeniusApi()
    lyrics = genius_api.get_lyrics_from_artist_and_title(
        song_title="Hotline Bling", artist_name="Drake")
    print(lyrics)
