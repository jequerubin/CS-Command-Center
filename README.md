# TuskCS

A student dashboard for Cal State Fullerton Computer Science students. Aggregates Canvas LMS assignments, GitHub repositories, local weather, and tech news into a single interface.

## Team Members

- Jordan Querubin
- Edgar Vergara
- Nathan Vi

## Features

- **Canvas Assignments** — Displays upcoming unsubmitted assignments due within the next 2 weeks, pulled from all active courses via the Canvas LMS API.
- **GitHub Repositories** — Shows your most recently updated repositories with language, description, and update date via GitHub OAuth.
- **Weather** — Current conditions in Fullerton via OpenWeatherMap.
- **Tech News** — Top stories from Hacker News, sorted by score.
- **Pomodoro Timer** — Built-in work/break timer with configurable sessions.
- **Quick Links** — One-click access to CSUF student resources (Student Portal, CS Department, Career Center, Tutoring Services).

## Tech Stack

- Python 3.10+, Flask, Jinja2
- SQLite + SQLAlchemy (user and token storage)
- Fernet encryption (token security)
- GitHub OAuth via Flask-Dance
- Canvas LMS API, GitHub API, OpenWeatherMap API, Hacker News API

## Project Structure

```
tuskcs/
├── app.py                     # Flask routes, OAuth, DB init
├── models.py                  # SQLAlchemy User model
├── encryption.py              # Fernet encrypt/decrypt utilities
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (not committed)
├── .env.example               # Template for .env
├── services/
│   ├── canvas_api.py          # Canvas LMS integration
│   ├── github_api.py          # GitHub API integration
│   ├── hackernews_api.py      # Hacker News API integration
│   └── weather_api.py         # OpenWeatherMap integration
├── templates/
│   ├── base.html              # Shared layout (header, nav)
│   ├── login.html             # GitHub OAuth login page
│   ├── loading.html           # Loading screen with skeleton UI
│   ├── canvas_setup.html      # Canvas token setup flow
│   └── dashboard.html         # Main dashboard with all cards
├── static/
│   ├── style.css              # Global styles
│   ├── TuskCS_Favicon.png     # App icon
│   └── TuskCS_Banner.png      # Login page banner
└── instance/
    └── app.db                 # SQLite database (auto-generated)
```

## Setup

### 1. Clone and create virtual environment

```bash
git clone <repository-url>
cd tuskcs
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy the example and fill in your values:

```bash
cp .env.example .env
```

Required variables:

| Variable | Description | How to get it |
|----------|-------------|---------------|
| `SECRET_KEY` | Flask session signing key | Run `python3 -c "import secrets; print(secrets.token_hex(24))"` |
| `FERNET_KEY` | Token encryption key | Run `python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"` |
| `GITHUB_CLIENT_ID` | GitHub OAuth app client ID | [GitHub Developer Settings](https://github.com/settings/developers) → New OAuth App |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth app client secret | Same as above |
| `WEATHER_API_KEY` | OpenWeatherMap API key | [openweathermap.org](https://openweathermap.org/api) → Sign up (free tier) |

### 3. Configure GitHub OAuth App

In your GitHub OAuth app settings, set the callback URL to:

```
http://localhost:5000/login/github/authorized
```

### 4. Run

```bash
python app.py
```

or

```bash
flask run
```

Open `http://localhost:5000` in your browser.

### VSCode Setup

If using VSCode: when prompted to create a virtual environment, click Yes. VSCode will activate it automatically. Confirm by checking for `('venv': venv)` in the bottom-left corner. Then install dependencies and run from the integrated terminal.

## User Flow

1. **Login** — Authenticate via GitHub OAuth
2. **Canvas Setup** — Paste your Canvas API token (first login only)
3. **Dashboard** — View assignments, repos, weather, news, and tools

Returning users skip Canvas setup — the token is encrypted and stored in the database.

## Dev Routes

These routes return raw JSON for testing (remove before deployment):

| Route | Data |
|-------|------|
| `/dev/canvas` | Filtered Canvas assignments |
| `/dev/github` | GitHub repositories |
| `/dev/news` | Hacker News top stories |
| `/dev/weather` | Current weather data |

## Canvas API Note

The Canvas API endpoint for CSUF is `https://csufullerton.instructure.com` (not `canvas.fullerton.edu`, which is the browser-facing URL). This is hardcoded in `services/canvas_api.py`.

## Contributing

See the Project Board for available tickets. Create feature branches off `main` and submit PRs. Use "Closes #X" in PR descriptions to link issues.
