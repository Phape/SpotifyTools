import spotipy

class SpotifyApi:
    def __init__(self):
        super().__init__()

    def get_current_track(self, spotify):
        return spotify.currently_playing()

    def get_current_artists(self, spotify):
        current_track = self.get_current_track(spotify)
        if not current_track:
            return "Seems like nothing is currently playing."

        artist_ids = []
        for artist in current_track['item']['artists']:
            artist_ids.append(artist['id'])
            current_artists = spotify.artists(artist_ids)
        return current_artists