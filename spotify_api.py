import spotipy

class SpotifyApi:
    def __init__(self):
        super().__init__()

    def get_current_track(self, spotify):
        current_track = spotify.currently_playing()
        return spotify.currently_playing()

    def get_current_artists(self, spotify, current_track):
        """Gets the Spotify IDs of the artists of the current song.

        Args:
            spotify: the spotify object from spotipy
            current_track (dict): a track retrieved from the Spotify API (via spotipy)

        Returns:
            dict: The Spotify IDs of the current artists
        """
        artist_ids = []
        for artist in current_track['item']['artists']:
            artist_ids.append(artist['id'])

        if artist_ids == [None]:    #Happens when listenig to local music
            return []
        else:
            current_artists = spotify.artists(artist_ids)
            return current_artists