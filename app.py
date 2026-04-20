import os
from flask import Flask, request, redirect, url_for, session, jsonify, render_template
from dotenv import load_dotenv
from flask_dance.contrib.github import make_github_blueprint, github
from services.canvas_api import test_token, fetch_assignments
from services.github_api import fetch_repositories

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cs-command-center-dev-key")

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
    username = resp.json().get("login")
    session['github_username'] = username
    return render_template('success.html', github_username=username)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/canvas-setup', methods=['GET', 'POST'])
def canvas_setup():
    if request.method == 'POST':
        token = request.form.get('token', '').strip()
        canvas_url = request.form.get('canvas_url', '').strip()

        if test_token(token, canvas_url):
            session['token'] = token
            session['canvas_url'] = canvas_url
            return redirect(url_for('dashboard'))

        # TODO: replace with render_template('canvas_setup.html', error="Invalid token or Canvas URL")
        return "Invalid token or Canvas URL. Please try again."

    # TODO: replace with render_template('canvas_setup.html')
    return "Settings page placeholder"


@app.route('/dashboard')
def dashboard():
    token = session.get('token')
    canvas_url = session.get('canvas_url')

    if not token:
        return redirect(url_for('canvas_setup'))

    assignments = fetch_assignments(token, canvas_url)

    # TODO: replace with render_template('dashboard.html', assignments=assignments)
    return "Dashboard placeholder"


# --- DEV ROUTES (remove before public deployment) ---

@app.route('/dev/canvas')
def dev_canvas():
    token = session.get('token')
    canvas_url = session.get('canvas_url')
    if not token:
        return jsonify({"error": "No Canvas token in session"})
    return jsonify(fetch_assignments(token, canvas_url))


@app.route('/dev/github')
def dev_github():
    if not github.authorized:
        return jsonify({"error": "Not logged in"})
    token = github.token["access_token"]
    return jsonify(fetch_repositories(token))


if __name__ == '__main__':
    app.run(debug=True)
