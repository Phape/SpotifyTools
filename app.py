import os
from flask import Flask, session, request, redirect, render_template
from flask_session import Session
import spotipy
import settings
import uuid

app = Flask(__name__)
app.config.from_object(settings)

Session(app)

if not os.path.exists('cache'):
    os.makedirs('cache')


@app.route('/')
def index():
    if 'uuid' not in session:
        session['uuid'] = uuid.uuid4()
    auth_manager = spotipy.oauth2.SpotifyOAuth(username=session.get('uuid'), cache_path="cache/{0}".format(session.get('uuid')))
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    if request.args.get("code"):
        session['token_info'] = auth_manager.get_access_token(code=request.args['code'], as_dict=False)
        return redirect('/')

    if not session.get('token_info'):
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'
        
    return render_template('index.html', spotify = spotify)


@app.route('/sign_out')
def sign_out():
    os.remove('cache/{0}'.format(session.get('uuid')))
    session.clear()
    return redirect('/')


@app.route('/playlists')
def playlists():
    if not session.get('token_info'):
        return redirect('/')
    else:
        auth_manager = spotipy.oauth2.SpotifyOAuth(username=session.get('uuid'), cache_path="cache/{0}".format(session.get('uuid')))
        spotify = spotipy.Spotify(auth_manager=auth_manager)
        return spotify.current_user_playlists()

if __name__ == "__main__":
    app.run(debug=True)