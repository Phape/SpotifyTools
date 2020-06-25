import spotipy
from collections import Counter


class SpotifyApi:
    def __init__(self):
        super().__init__()

    def get_current_track(self, spotify):
        current_track = spotify.currently_playing()
        return spotify.currently_playing()

    def get_current_artists_ids(self, spotify, current_track):
        """Gets the artists of the current track.

        Args:
            spotify: the spotify object from spotipy
            current_track (dict): a track retrieved from the Spotify API (via spotipy)

        Returns:
            dict: The artists of the current track
        """
        artist_ids = []
        for artist in current_track['item']['artists']:
            artist_ids.append(artist['id'])

        if artist_ids == [None]:  # Happens when listenig to local music
            return []
        else:
            current_artists = spotify.artists(artist_ids)
            return current_artists

    def get_top_artists(self, spotify, limit=20, offset=0, time_range='medium_term'):
        # read more about time ranges on Spotify docs, currently:
        # long_term: years, medium_term: 6mo, short_term: 4w
        top_artists = spotify.current_user_top_artists(
            limit, offset, time_range)
        return top_artists

    def get_genre_rank_by_top_artists(self, top_artists):
        top_genres = []
        for artist in top_artists['items']:
            genres_of_artist = artist['genres']
            for genre in genres_of_artist:
                top_genres.append(genre)
        genre_rank = Counter(top_genres).most_common()
        return genre_rank

    def get_top_tracks(self, spotify, limit=20, offset=0, time_range='medium_term'):
        # read more about time ranges on Spotify docs, currently:
        # long_term: years, medium_term: 6mo, short_term: 4w
        top_tracks = spotify.current_user_top_tracks(
            limit, offset, time_range)
        return top_tracks
