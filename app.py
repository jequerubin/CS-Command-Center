import os
from flask import Flask, request, redirect, url_for, session, jsonify, render_template
from dotenv import load_dotenv
from flask_dance.contrib.github import make_github_blueprint, github
from models import db, User
from encryption import encrypt_token, decrypt_token
from services.canvas_api import test_token, fetch_assignments
from services.github_api import fetch_repositories
from services.hackernews_api import fetch_top_stories
from services.weather_api import fetch_weather

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cs-command-center-dev-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

github_bp = make_github_blueprint(
    client_id=os.environ.get("GITHUB_CLIENT_ID"),
    client_secret=os.environ.get("GITHUB_CLIENT_SECRET"),
    redirect_url="/success",
)
app.register_blueprint(github_bp, url_prefix="/login")


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    error = session.pop('error', None)
    return render_template('login.html', error=error)


@app.route('/success')
def success():
    if not github.authorized:
        session['error'] = "GitHub authorization failed. Please try again."
        return redirect(url_for('login'))

    resp = github.get("/user")
    user_data = resp.json()
    username = user_data.get("login")
    raw_github_token = github.token["access_token"]

    session['github_username'] = username

    user = User.query.filter_by(github_username=username).first()

    if user is None:
        user = User(
            github_username=username,
            github_token=encrypt_token(raw_github_token),
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('canvas_setup'))

    if user.canvas_token is None:
        return redirect(url_for('canvas_setup'))

    session['token'] = decrypt_token(user.canvas_token)
    return redirect(url_for('loading'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/settings')
def settings():
    return redirect(url_for('canvas_setup'))


@app.route('/canvas-setup', methods=['GET', 'POST'])
def canvas_setup():
    username = session.get('github_username')
    if not username:
        return redirect(url_for('login'))

    if username:
        user = User.query.filter_by(github_username=username).first()
        if user and user.canvas_token:
            return redirect(url_for('loading'))

    if request.method == 'POST':
        token = request.form.get('token', '').strip()

        if test_token(token):
            username = session.get('github_username')
            user = User.query.filter_by(github_username=username).first()
            if user:
                user.canvas_token = encrypt_token(token)
                db.session.commit()
            session['token'] = token
            return redirect(url_for('loading'))

        return render_template('canvas_setup.html', error="Invalid Canvas token. Please check and try again.")

    return render_template('canvas_setup.html')

def assignmentsSort(assignment):
    return (assignment['due_at'] is None, assignment['due_at'])

@app.route('/loading')
def loading():
    username = session.get('github_username')
    if not username:
        return redirect(url_for('login'))
    return render_template('loading.html')

@app.route('/dashboard')
def dashboard():
    token = session.get('token')

    if not token:
        username = session.get('github_username')
        if username:
            user = User.query.filter_by(github_username=username).first()
            if user and user.canvas_token:
                token = decrypt_token(user.canvas_token)
                session['token'] = token

    if not token:
        return redirect(url_for('canvas_setup'))

    assignments = fetch_assignments(token)

    # Fetch GitHub repositories using stored token
    github_repos = []
    username = session.get('github_username')
    if username:
        user = User.query.filter_by(github_username=username).first()
        if user and user.github_token:
            github_repos = fetch_repositories(decrypt_token(user.github_token))

    news_stories = fetch_top_stories(limit=15)[:5]

    return render_template(
        'dashboard.html',
        assignments=assignments,
        github_repos=github_repos,
        loading=False,
        news_stories=news_stories
    )


# --- DEV ROUTES (remove before public deployment) ---

@app.route('/dev/canvas')
def dev_canvas():
    token = session.get('token')
    if not token:
        return jsonify({"error": "No Canvas token in session"})
    return jsonify(fetch_assignments(token))


@app.route('/dev/github')
def dev_github():
    if not github.authorized:
        return jsonify({"error": "Not logged in"})
    token = github.token["access_token"]
    return jsonify(fetch_repositories(token))

  
@app.route('/dev/news')
def dev_news():
    return jsonify(fetch_top_stories())


@app.route("/dev/weather")
def dev_weather():
    token = os.environ.get("WEATHER_API_KEY")
    data = fetch_weather(token)
    return data


if __name__ == '__main__':
    app.run(debug=True)
