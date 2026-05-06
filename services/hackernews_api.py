import requests


def test_token():
    """
    Validates connectivity to Hacker News.
    Returns True if the server responds with HTTP 200, False otherwise.
    """
    try:
        response = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=10,
        )
        return response.status_code == 200
    except Exception:
        return False


def fetch_top_stories(limit=5):
    """
    Fetches top stories:
        [
            {
                "title":       <str>  Story Title, poll, html,
                "author":      <str>  Author name,
                "url":         <str>  The URL of the story,
                "score":       <int>  story's score or votes of pollopt,
                "comments":    <int>  total comment count,
            },
            ...
        ]
    Returns an empty list on any error.
    """
    try:
        ids_response = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=10,
        )
        story_ids = ids_response.json()
        if not isinstance(story_ids, list):
            return []
        
        stories = []
        
        for story_id in story_ids[:limit]:
            try:
                item_response = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                    timeout=10
                )
                item = item_response.json()
                stories.append({
                    "title":       item.get("title", "untitiled"),
                    "author":      item.get("by", "unkown"),
                    "url":         item.get("url", ""),
                    "score":       item.get("score", 0),
                    "comments":    item.get("descedents", 0),
                })
            except Exception:
                continue

        return sorted(stories, key=lambda s: s["score"], reverse=True)
    
    except Exception:
        return []


if __name__ == "__main__":
    print(test_token())
    print(fetch_top_stories())
