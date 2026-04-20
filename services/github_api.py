import requests


def test_token(token):
    """
    Validates a GitHub personal access token by hitting the /user endpoint.
    Returns True if the server responds with HTTP 200, False otherwise.
    """
    try:
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        response = requests.get(
            "https://api.github.com/user",
            headers=headers,
            timeout=10,
        )
        return response.status_code == 200
    except Exception:
        return False


def fetch_repositories(token):
    """
    Fetches the most recently updated repositories for the authenticated user.
    Makes a GET request to /user/repos sorted by last updated, limited to 20.
    Returns a flat list of dicts:
        [
            {
                "name":        <str>  repository name,
                "description": <str>  repo description, or "" if None,
                "updated_at":  <str>  ISO-8601 datetime of last update,
                "html_url":    <str>  link to the repository on GitHub,
                "language":    <str|None>  primary language,
                "private":     <bool>  whether the repo is private,
                "fork":        <bool>  whether the repo is a fork,
            },
            ...
        ]
    Returns an empty list on any error.
    """
    try:
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        response = requests.get(
            "https://api.github.com/user/repos",
            headers=headers,
            params={"sort": "updated", "per_page": 20},
            timeout=10,
        )
        repos = response.json()

        if not isinstance(repos, list):
            return []

        result = []

        for repo in repos:
            if not isinstance(repo, dict):
                continue

            result.append({
                "name":        repo.get("name", ""),
                "description": repo.get("description") or "",
                "updated_at":  repo.get("updated_at", ""),
                "html_url":    repo.get("html_url", ""),
                "language":    repo.get("language"),
                "private":     repo.get("private", False),
                "fork":        repo.get("fork", False),
            })

        return result

    except Exception:
        return []


if __name__ == "__main__":
    token = "PASTE_YOUR_TOKEN_HERE"
    print(test_token(token))
    print(fetch_repositories(token))
