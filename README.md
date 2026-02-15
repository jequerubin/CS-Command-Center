# CS Command Center

Student dashboard for viewing Canvas assignments and GitHub repositories.

## Team Members
- Jordan Querubin
- Edgar Vergara
- Nathan Vi

## Tech Stack
- Python 3.10+
- Flask
- Canvas LMS API
- GitHub API

## Setup Instructions

### Terminal Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd cs-command-center
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
python app.py
```

6. Open browser to `http://localhost:5000`

### VSCode Setup

1. Open project folder in VSCode

2. When prompted "Do you want to create a virtual environment?", click **Yes**

3. VSCode will automatically activate the virtual environment

4. Open terminal in VSCode (should see `(venv)` at the start)

5. Install dependencies:
```bash
pip install -r requirements.txt
```

6. Run the application:
```bash
python app.py
```

7. Open browser to `http://localhost:5000`

**Note:** Check bottom-left of VSCode window - should show `('venv': venv)`

## Project Structure
```
cs-command-center/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
├── static/             # CSS, JavaScript, images
└── services/           # API integration logic
```

## Sprint 1 Goal

Display Canvas assignments in a web interface

## Contributing

See Project Board for available tickets. Follow the GitHub Workflow Guide for PR process.
