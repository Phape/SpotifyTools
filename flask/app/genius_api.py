import requests
from bs4 import BeautifulSoup
import app.settings as settings

# heavily inspired by https://dev.to/willamesoares/how-to-integrate-spotify-and-genius-api-to-easily-crawl-song-lyrics-with-python-4o62
# thanks to https://github.com/willamesoares


class GeniusApi:

    def request_song_info(self, song_title, artist_name):
        base_url = "https://api.genius.com"
        headers = {"Authorization": "Bearer " + settings.GENIUS_ACCESS_TOKEN}
        search_url = base_url + "/search"
        data = {"q": song_title + " " + artist_name}
        response = requests.get(search_url, data=data, headers=headers)
        # f = open("response.json", "w")
        # f.write(json.dumps(response.json()))

        return response

    def get_remote_song_url(self, song_title, artist_name):
        # Search for matches in the request response
        response = self.request_song_info(song_title, artist_name)
        json = response.json()
        remote_song_info = None
        song_url = None

        for hit in json["response"]["hits"]:
            if artist_name.lower() in hit["result"]["primary_artist"]["name"].lower():
                remote_song_info = hit
                break

        # Extract lyrics from URL if the song was found
        if remote_song_info:
            song_url = remote_song_info["result"]["url"]

        return song_url

    def get_song_lyrics_from_url(self, url):
        page = requests.get(url)
        html = BeautifulSoup(page.text, "html.parser")
        html_lyrics = html.find("div", class_="lyrics")
        if html_lyrics is not None:
            lyrics = html_lyrics.get_text()
        else:
            lyrics = (
                "Could not obtain lyrics, please try again.\nAlternatively, you could see them here: "
                + url
            )

        return lyrics

    def get_lyrics_from_artist_and_title(self, song_title, artist_name):
        url = self.get_remote_song_url(song_title, artist_name)
        if url == None:
            lyrics = "No lyrics were found for this track"
        else:
            lyrics = self.get_song_lyrics_from_url(url)

        return lyrics


if __name__ == "__main__":
    genius_api = GeniusApi()
    lyrics = genius_api.get_lyrics_from_artist_and_title(
        song_title="Come With Me", artist_name="Nitro Fun"
    )
    print(lyrics)
