from flask import Flask, request, redirect, url_for, session
from services.canvas_api import test_token, fetch_assignments

app = Flask(__name__)
app.secret_key = 'cs-command-center-dev-key'


@app.route('/')
def home():
    return "CS Command Center Test Screen"


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        token = request.form.get('token', '').strip()
        canvas_url = request.form.get('canvas_url', '').strip()

        if test_token(token, canvas_url):
            session['token'] = token
            session['canvas_url'] = canvas_url
            return redirect(url_for('dashboard'))

        # TODO: replace with render_template('settings.html', error="Invalid token or Canvas URL")
        return "Invalid token or Canvas URL. Please try again."

    # TODO: replace with render_template('settings.html')
    return "Settings page placeholder"


@app.route('/dashboard')
def dashboard():
    token = session.get('token')
    canvas_url = session.get('canvas_url')

    if not token:
        return redirect(url_for('settings'))

    assignments = fetch_assignments(token, canvas_url)

    # TODO: replace with render_template('dashboard.html', assignments=assignments)
    return "Dashboard placeholder"


if __name__ == '__main__':
    app.run(debug=True)
