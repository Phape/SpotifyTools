import os
from flask import Flask, session, request, redirect, render_template
from flask_session import Session
import spotipy
import settings
import uuid
import time

app = Flask(__name__)
app.config.from_object(settings)

Session(app)


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
        session['AUTH_MANAGER'] = spotipy.oauth2.SpotifyOAuth(username=session.get(
            'uuid'), cache_path="cache/{0}".format(session.get('uuid')))
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
    app.run(debug=True)
