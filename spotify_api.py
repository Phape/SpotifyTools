import spotipy

class SpotifyApi:
    def __init__(self):
        super().__init__()

    def get_current_track(self, spotify):
        current_track = spotify.currently_playing()
        if not current_track:
            raise NoCurrentTrackException()
        return spotify.currently_playing()

    def get_current_artists(self, spotify):
        try:
            current_track = self.get_current_track(spotify)
        except NoCurrentTrackException:
            return [] #Todo check how to properly handle this exception

        artist_ids = []
        for artist in current_track['item']['artists']:
            artist_ids.append(artist['id'])
            current_artists = spotify.artists(artist_ids)
        return current_artists

class NoCurrentTrackException(Exception):
    def __init__(self, message="No Current Track (check whether you are listening to music with your Spotify Account)"):
        self.message = message
        super().__init__(self.message)