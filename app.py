from flask import Flask, request, redirect, url_for, session,render_template
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

def assignmentsSort(assignment):
    return (assignment['due_at'] is None, assignment['due_at'])

@app.route('/dashboard')
def dashboard():
    token = session.get('token')
    canvas_url = session.get('canvas_url')

    if not token:
        return redirect(url_for('settings'))

    assignments = fetch_assignments(token, canvas_url)
    assignments = sorted(assignments, key=assignmentsSort)
    
    courses = sorted(set(a['course'] for a in assignments))
    
    selected_course = request.args.get('course', 'All courses')
   
    selected_query = request.args.get('search', '').strip().lower()
    if selected_query:
        assignments = [a for a in assignments if selected_query in a['name'].lower()]
    if selected_course != 'All courses':
        assignments = [a for a in assignments if a['course'] == selected_course]

    # TODO: replace with render_template('dashboard.html', assignments=assignments)
    return render_template(
        'dashboard.html', assignments=assignments,
        courses = courses,
        selected_query=selected_query,
        selected_course=selected_course,
        loading=False)

if __name__ == '__main__':
    app.run(debug=True)