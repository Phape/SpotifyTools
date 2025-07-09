# 🎵 Spotify Tools

A modern web application that enhances your Spotify experience by providing additional information about your favorite songs using the Spotify and Genius APIs.

## 🌟 Features

- **Track Analysis**: Get detailed information about your currently playing tracks
- **Lyrics Integration**: Fetch lyrics from Genius API
- **User Statistics**: View your top tracks and recently played songs
- **Modern UI**: Clean and responsive web interface

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ or Docker
- Spotify Developer Account
- Genius API Account

### 🐳 Docker (Recommended)

1. **Clone the repository**

   ```bash
   git clone https://github.com/Phape/SpotifyTools.git
   cd SpotifyTools
   ```

2. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   ```

3. **Create Docker network**

   ```bash
   docker network create net
   ```

4. **Start the application**

   **For Development (default - includes hot reload):**

   ```bash
   docker compose up -d --build
   ```

   **For Production (uses pre-built image):**

   ```bash
   docker compose -f docker-compose.yml up -d
   ```

5. **Access the application**
   - Open your browser and go to: `http://localhost:5000`

### 🐳 Docker Usage

Docker Compose automatically loads `docker-compose.override.yml` for development. To run in different modes:

**Development Mode (Default):**

```bash
docker-compose up -d --build    # Uses override file automatically (hot reload)
docker-compose logs -f flask    # Watch logs to see hot reload working
```

**Production Mode:**

```bash
docker-compose -f docker-compose.yml up -d     # Explicitly use only base file
docker-compose -f docker-compose.yml pull      # Update to newest version
```

**Key Differences:**

- **Development**: Uses `docker-compose.override.yml` → local build, hot reload, Flask dev server
- **Production**: Uses only `docker-compose.yml` → pre-built image, Gunicorn, stable


## 🐍 Local Python Development

1. **Clone and navigate**

   ```bash
   git clone https://github.com/Phape/SpotifyTools.git
   cd SpotifyTools/flask
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment**

   ```bash
   cp ../.env.example ../.env
   # Edit .env with your API credentials
   ```

5. **Run the application**

   ```bash
   python app.py
   ```

## 🔑 API Setup

### Spotify API

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)
2. Create a new application
3. Copy your `Client ID` and `Client Secret`
4. Add `http://127.0.0.1:5000/authorize` to Redirect URIs

### Genius API

1. Go to [Genius API Clients](https://genius.com/api-clients)
2. Create a new API client
3. Copy your `Client Access Token`

### Environment Variables

Update your `.env` file with your credentials:

```env
# Flask Configuration
FLASK_SECRET_KEY=your_secret_key_here

# Spotify API
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:5000/authorize

# Genius API
GENIUS_CLIENT_ACCESS_TOKEN=your_genius_access_token
```

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: Spotify Web API, Genius API
- **Deployment**: Docker, Gunicorn
- **Session Management**: Flask-Session (filesystem)

## 📁 Project Structure

```plaintext
SpotifyTools/
├── flask/                  # Main application
│   ├── app/               # Flask application
│   │   ├── __init__.py    # App initialization
│   │   ├── routes.py      # URL routes
│   │   └── settings.py    # Configuration
│   ├── static/            # CSS, JS, images
│   ├── templates/         # HTML templates
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Docker configuration
├── .env.example           # Environment template
├── docker-compose.yml     # Production compose
└── docker-compose.override.yml  # Development overrides
```

## 🔧 Development

### VS Code Setup

If you're using VS Code, check out the [Flask Tutorial in Visual Studio Code](https://code.visualstudio.com/docs/python/tutorial-flask) for detailed setup instructions.

### Production vs Development

- **Development**: Uses `docker-compose.override.yml` with debug mode
- **Production**: Uses `requirements-prod.txt` with Gunicorn and optimizations

## 🌐 Deployment

The application is deployed at: [spotifytools.phape.de](https://spotifytools.phape.de/)

## 📚 Documentation & Resources

### APIs & Libraries

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [Spotipy Documentation](https://spotipy.readthedocs.io)
- [Genius API](https://docs.genius.com/)

### Framework Documentation

- [Flask Documentation](https://flask.palletsprojects.com)
- [Flask-Session](https://flask-session.readthedocs.io)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

### Deployment & DevOps

- [Docker Compose](https://docs.docker.com/compose/)
- [Gunicorn Documentation](https://gunicorn.org/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Issues & Support

If you encounter any issues or have questions:

- Open an issue on [GitHub Issues](https://github.com/Phape/SpotifyTools/issues)
- Check existing issues for solutions

---

Made with ❤️ by [Phape](https://github.com/Phape)
