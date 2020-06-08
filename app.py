import os
from flask import Flask, session, request, redirect, render_template
from flask_session import Session
import spotipy
import settings
import uuid
import time
from spotify_api import NoCurrentTrackException, SpotifyApi

app = Flask(__name__)
app.config.from_object(settings)

Session(app)
spotifyApi = SpotifyApi()


@app.route('/')
def index():
    if 'uuid' not in session:
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
            'uuid'), cache_path=cache_path, scope='user-read-currently-playing')
        auth_url = session.get('AUTH_MANAGER').get_authorize_url()
        return redirect(auth_url)

    return redirect('/')


@app.route('/authorize')
def authorize():
    if request.args.get("code"):
        session['token_info'] = session.get('AUTH_MANAGER').get_access_token(
            code=request.args['code'], as_dict=False)

        session['SPOTIFY'] = spotipy.Spotify(
            auth_manager=session.get('AUTH_MANAGER'))
        return redirect('/')


@app.route('/sign_out')
def sign_out():
    cache_file = os.path.join(settings.cache_path, str(session.get('uuid')))
    if(os.path.exists(cache_file)):
        os.remove(cache_file)
    session.clear()
    return redirect('/')


@app.route('/playlists')
def playlists():
    if not session.get('token_info'):
        return redirect('/')

    return session.get('SPOTIFY').current_user_playlists()


@app.route('/current_genres', methods=['GET', 'POST'])
def current_genres():
    # Handler for the toggle auto_refresh_button
    if request.method == 'POST':
        if request.form['auto_refresh_button']:
            if 'REFRESH_AFTER_SECONDS' in session:
                session['REFRESH_AFTER_SECONDS'] = None
            else:
                session['REFRESH_AFTER_SECONDS'] = settings.refresh_after_seconds

    last_current_track = session.get('CURRENT_TRACK')
    try:
        session['CURRENT_TRACK'] = spotifyApi.get_current_track(
            session.get('SPOTIFY'))
    except NoCurrentTrackException:
        session['CURRENT_TRACK'] = "No Current Track, check whether you are listenig to Spotify with this account: " + \
            session.get('SPOTIFY').me()['display_name']

    # Only get new artist info from Spotify if current_track has changed
    if not last_current_track or session.get('CURRENT_TRACK')['item'] != last_current_track['item']:
        session['CURRENT_ARTISTS'] = spotifyApi.get_current_artists(
            spotify=session.get('SPOTIFY'), current_track=session.get('CURRENT_TRACK'))
    return render_template('current_genres.html', current_track_name=session['CURRENT_TRACK']['item']['name'], current_artists=session.get('CURRENT_ARTISTS'), refresh_after_seconds=session.get('REFRESH_AFTER_SECONDS'))


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
