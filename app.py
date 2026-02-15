from flas import Flask

app = Flask(__name__)
app.secret_key = 'cs-command-center-dev-key'

@app.route('/')
def home():
    return "CS Command Center Test Screen"

if __name__ == '__main__':
    app.run(debug=True)
