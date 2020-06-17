import os
from flask import Flask, session, request, redirect, render_template, url_for
from flask_session import Session
from flask_assets import Environment, Bundle
import spotipy
import settings
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
spotifyApi = SpotifyApi()


@app.route('/')
def index():
    if 'uuid' not in session:
        session['NEXT_URL'] = url_for('index')
        return render_template('sign_in.html')

    return render_template('index.html', spotify=session.get('SPOTIFY'))


@app.route('/sign_in')
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


@app.route('/authorize')
def authorize():
    if request.args.get("code"):
        session['token_info'] = session.get('AUTH_MANAGER').get_access_token(
            code=request.args['code'], as_dict=False)

        session['SPOTIFY'] = spotipy.Spotify(
            auth_manager=session.get('AUTH_MANAGER'))

        if session.get('NEXT_URL'):
            return redirect(session.get('NEXT_URL'))
        return redirect(url_for('index'))

    else:
        f"Didn't get a token from Spotify."


@app.route('/sign_out')
def sign_out():
    cache_file = os.path.join(settings.cache_path, str(session.get('uuid')))
    if(os.path.exists(cache_file)):
        os.remove(cache_file)
    session.clear()
    return redirect(url_for('index'))


@app.route('/playlists')
def playlists():
    if not session.get('token_info'):
        return redirect('/')

    return session.get('SPOTIFY').current_user_playlists()


@app.route('/current_genres', methods=['GET', 'POST'])
def current_genres():
    # Check if user is signed in
    if not session.get('uuid'):
        print("request url:", request.url)
        session['NEXT_URL'] = url_for('current_genres')
        return render_template('sign_in.html')

    # Handler for the toggle auto_refresh_button
    if request.method == 'POST':
        if request.form['auto_refresh_button']:
            if not session.get('IS_AUTOREFRESH') or session.get('IS_AUTOREFRESH') == False:
                session['IS_AUTOREFRESH'] = True
            else:
                session['IS_AUTOREFRESH'] = False

    last_current_track = session.get('CURRENT_TRACK')
    session['CURRENT_TRACK'] = spotifyApi.get_current_track(
        session.get('SPOTIFY'))

    if not session.get('CURRENT_TRACK'):
        current_track_name = "No Current Track, check whether you are listenig to Spotify with this account: " + \
            session.get('SPOTIFY').me()['display_name']
    else:
        if session.get('CURRENT_TRACK')['currently_playing_type'] != 'track':
            current_track_name = "You are not listening to a track. Make shure you don't listen to a podcast or something similar."
        else:
            current_track_name = session['CURRENT_TRACK']['item']['name']

    # Only get new artist info from Spotify if current_track has changed and if playback type is 'track'
    if session.get('CURRENT_TRACK') and session.get('CURRENT_TRACK')['currently_playing_type'] == 'track':
        if not last_current_track or session.get('CURRENT_TRACK')['item'] != last_current_track['item']:
            session['CURRENT_ARTISTS'] = spotifyApi.get_current_artists_ids(
                spotify=session.get('SPOTIFY'), current_track=session.get('CURRENT_TRACK'))
    else:
        session['CURRENT_ARTISTS'] = []

    if session.get('IS_AUTOREFRESH') == True:
        refresh_after_seconds = settings.refresh_after_seconds
    else:
        refresh_after_seconds = None

    return render_template('current_genres.html', current_track_name=current_track_name, current_artists=session.get('CURRENT_ARTISTS'), refresh_after_seconds=refresh_after_seconds)


@app.route('/top_artists')
def top_artists():
    time_range = request.args.get('time_range', default='medium_term')
    offset = request.args.get('offset', default=0)
    top_artists = spotifyApi.get_top_artists(session.get('SPOTIFY'), limit=50, time_range=time_range, offset=offset)
    genre_rank = spotifyApi.get_genre_rank_by_top_artists(top_artists)
    time_range_dict = {
        "short_term": "last 4 weeks",
        "medium_term": "last 6 months",
        "long_term": "total"
    }
    time_range_text = time_range_dict[time_range]
    return render_template('top_artists.html', top_artists=top_artists, genre_rank=genre_rank, chosen_time_range=time_range_text)


@app.route('/recently_played')
#not yet linked on the website
def recently_played():
    recently_played = session.get('SPOTIFY').current_user_recently_played() #move this to the spotifyApi class
    return recently_played


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
