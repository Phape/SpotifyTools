import os
from flask import Flask, session, request, redirect, render_template, url_for
from flask_session import Session
from flask_assets import Environment, Bundle
from functools import wraps
import spotipy
import settings
import dicts
import uuid
import time
from spotify_api import SpotifyApi

app = Flask(__name__)
app.config.from_object(settings)

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('css/main.scss', filters='pyscss', output='css/main.css')
assets.register('scss_all', scss)

Session(app)


def sign_in_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'uuid' not in session:
            session['NEXT_URL'] = request.url
            return render_template('sign_in.html')
        else:
            return f(*args, **kwargs)
    return wrap


@app.route('/sign-in', methods=['GET'])
def sign_in():
    if 'uuid' not in session:
        session['uuid'] = uuid.uuid4()

    if 'token_info' not in session:
        cache_path = os.path.join(
            settings.cache_path, str(session.get('uuid')))
        session['AUTH_MANAGER'] = spotipy.oauth2.SpotifyOAuth(username=session.get(
            'uuid'), cache_path=cache_path, scope=settings.scopes)
        auth_url = session.get('AUTH_MANAGER').get_authorize_url()
        return redirect(auth_url)


@app.route('/authorize', methods=['GET'])
def authorize():
    if request.args.get('code'):
        session['token_info'] = session.get('AUTH_MANAGER').get_access_token(
            code=request.args['code'], as_dict=False)

        spotify = spotipy.Spotify(
            auth_manager=session.get('AUTH_MANAGER'))

        session['SPOTIFY_API'] = SpotifyApi(spotify)

        if session.get('NEXT_URL'):
            return redirect(session.get('NEXT_URL'))
        return redirect(url_for('index'))

    else:
        f"Didn't get a token from Spotify."


@app.route('/sign-out', methods=['GET'])
def sign_out():
    cache_file = os.path.join(settings.cache_path, str(session.get('uuid')))
    if(os.path.exists(cache_file)):
        os.remove(cache_file)
    session.clear()
    return redirect(url_for('index'))


@app.route('/', methods=['GET'])
@sign_in_required
def index():
    spotify_me = session.get('SPOTIFY_API').get_spotify_me()
    return render_template('index.html', spotify_me=spotify_me)


@app.route('/toggle-auto-refresh', methods=['GET'])
def toggle_auto_refresh():
    session['NEXT_URL'] = request.url

    if not session.get('REFRESH_AFTER_SECONDS'):
        session['REFRESH_AFTER_SECONDS'] = settings.refresh_after_seconds
    else:
        session.pop('REFRESH_AFTER_SECONDS')
    return redirect(request.args.get('next', default='/'))


# @app.route('/playlists', methods=['GET'])
# def playlists():
#      # Check if user is signed in
#     if not session.get('uuid'):
#         session['NEXT_URL'] = request.url
#         return render_template('sign_in.html')

#     return session.get('SPOTIFY').current_user_playlists() #session spotify is depricated


@app.route('/current-genres', methods=['GET'])
@sign_in_required
def current_genres():
    current_track_name = session.get('SPOTIFY_API').get_current_track_name()
    current_artists = session.get('SPOTIFY_API').get_current_artists()
    refresh_after_seconds = session.get('REFRESH_AFTER_SECONDS')

    return render_template('current_genres.html', current_track_name=current_track_name, current_artists=current_artists, refresh_after_seconds=refresh_after_seconds)


@app.route('/top-artists', methods=['GET'])
@sign_in_required
def top_artists():
    time_range = request.args.get('time_range', default='short_term')
    offset = request.args.get('offset', default=0)
    top_artists = session.get('SPOTIFY_API').get_top_artists(
        limit=50, time_range=time_range, offset=offset)
    genre_rank = session.get(
        'SPOTIFY_API').get_genre_rank_by_top_artists(top_artists)

    time_range_text = dicts.time_ranges[time_range]
    return render_template('top_artists.html', top_artists=top_artists, genre_rank=genre_rank, chosen_time_range=time_range_text)


@app.route('/top-tracks', methods=['GET'])
@sign_in_required
def top_tracks():
    time_range = request.args.get('time_range', default='short_term')
    offset = request.args.get('offset', default=0)
    top_tracks = session.get('SPOTIFY_API').get_top_tracks(
        limit=50, time_range=time_range, offset=offset)

    time_range_text = dicts.time_ranges[time_range]
    return render_template('top_tracks.html', top_tracks=top_tracks, chosen_time_range=time_range_text)


@app.route('/current-features', methods=['GET'])
@sign_in_required
def current_features():
    current_track_name = session.get('SPOTIFY_API').get_current_track_name()
    current_track_features_human_readable = session.get(
        'SPOTIFY_API').get_current_track_features_human_readable()

    refresh_after_seconds = session.get('REFRESH_AFTER_SECONDS')
    return render_template('current_features.html', current_track_name=current_track_name, current_track_features_human_readable=current_track_features_human_readable, refresh_after_seconds=refresh_after_seconds)


@app.route('/recently-played', methods=['GET'])
@sign_in_required
def recently_played():
    recently_played = session.get('SPOTIFY_API').get_recently_played()
    return render_template('recently_played.html', recently_played=recently_played)


@app.before_request
def make_session_permanent():
    session.permanent = settings.session_permanent
    app.permanent_session_lifetime = settings.permanent_session_lifetime


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


# Initialize Cache
if not os.path.exists(settings.cache_path):
    os.makedirs(settings.cache_path)

current_time = time.time()

for f in os.listdir(settings.cache_path):
    f = os.path.join(settings.cache_path, f)
    creation_time = os.path.getctime(f)
    # remove cache that is older than x days
    if (current_time - creation_time) // (24 * 3600) >= 1:
        os.remove(f)


if __name__ == "__main__":
    app.run()
