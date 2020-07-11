import spotipy
from collections import Counter
import dicts


class SpotifyApi:
    def __init__(self, spotify):
        super().__init__()
        self.spotify = spotify
        self.current_track = None
        self.current_artists = None
        self.current_track_features = None
        self.last_current_track = None
        self.last_artist_ids = None
        self.last_features_id = None
        self.spotify_me = self.spotify.me()

    def get_spotify_me(self):
        return self.spotify_me

    def get_current_track(self):
        self.last_current_track = self.current_track
        self.current_track = self.spotify.currently_playing()
        return self.current_track

    def get_current_track_name(self):
        self.get_current_track()
        if self.current_track == None:
            return "No Current Track, check whether you are listenig to Spotify with this account: " + self.spotify_me['display_name']
        elif self.current_track['currently_playing_type'] != 'track':
            return "You are not listening to a track. Make shure you don't listen to a podcast or something similar."
        else:
            return self.current_track['item']['name']

    def is_new_track_playing(self):
        if self.last_current_track != self.current_track:
            return True
        return False

    def get_current_artists(self):
        """Gets the artists of the current track.
        Only sends a request to Spotify if the artists for the current track were not already requested.

        Returns:
            dict: The artists of the current track
        """
        artist_ids = []
        if self.current_track == None or self.current_track['currently_playing_type'] != 'track':
            return []

        for artist in self.current_track['item']['artists']:
            artist_ids.append(artist['id'])

        if self.last_artist_ids != artist_ids:
            if artist_ids == [None]:  # Happens when listenig to local music
                return []
            else:
                self.current_artists = self.spotify.artists(artist_ids)
                self.last_artist_ids = artist_ids
        return self.current_artists

    def get_current_track_features(self):
        if self.current_track == None or self.current_track['currently_playing_type'] != 'track' or self.current_track['item']['id'] == None:
            return []
        track_id = self.current_track['item']['id']
        if self.last_features_id != track_id:
            self.current_track_features = self.spotify.audio_features(track_id)
            self.last_features_id = track_id
        return self.current_track_features

    def get_current_track_features_human_readable(self):
        features = self.get_current_track_features()[0] if self.get_current_track_features() != [] else []

        percentage_values = {'danceability', 'energy', 'speechiness',
                             'acousticness', 'instrumentalness', 'liveness', 'valence'}

        not_displayed_features = {'type', 'id', 'track_href', 'analysis_url'}

        result = []
        for feature in features:
            if feature in not_displayed_features:
                features.pop(feature)
                break

            result_entry = {}
            result_entry['name'] = feature
            result_entry['icon'] = '/static/images/feature_icons/{}.svg'.format(
                feature)

            value = features[feature]
            if feature == 'key':
                value = dicts.musical_keys[value]
            elif feature == "mode":
                value = dicts.musical_modes[value]
            elif feature in percentage_values:
                value = value * 100

            if type(value) is float:
                value = round(value, 2)
            result_entry['value'] = value

            result.append(result_entry)

        return result

    def get_top_artists(self, limit=20, offset=0, time_range='medium_term'):
        # read more about time ranges on Spotify docs, currently:
        # long_term: years, medium_term: 6mo, short_term: 4w
        top_artists = self.spotify.current_user_top_artists(
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

    def get_top_tracks(self, limit=20, offset=0, time_range='medium_term'):
        # read more about time ranges on Spotify docs, currently:
        # long_term: years, medium_term: 6mo, short_term: 4w
        top_tracks = self.spotify.current_user_top_tracks(
            limit, offset, time_range)
        return top_tracks

    def get_recently_played(self):
        recently_played = self.spotify.current_user_recently_played()
        return recently_played
