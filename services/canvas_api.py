import requests


def test_token(token, canvas_url):
    """
    Validates a Canvas API token by hitting the /api/v1/users/self endpoint.
    Returns True if the server responds with HTTP 200, False otherwise.
    """
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{canvas_url}/api/v1/users/self",
            headers=headers,
            timeout=10,
        )
        return response.status_code == 200
    except Exception:
        return False


def fetch_assignments(token, canvas_url):
    """
    Fetches all assignments across a user's active Canvas courses.

    Steps:
      1. GET /api/v1/courses  (enrollment_state=active)
      2. For each course, GET /api/v1/courses/{id}/assignments
      3. Collect name, course name, due_at, and html_url for every assignment.

    Returns a flat list of dicts:
        [
            {
                "name":     <str>  assignment title,
                "course":   <str>  course name,
                "due_at":   <str|None>  ISO-8601 datetime or None,
                "html_url": <str>  link to the assignment in Canvas,
            },
            ...
        ]
    Returns an empty list on any error.
    """
    try:
        headers = {"Authorization": f"Bearer {token}"}

        courses_response = requests.get(
            f"{canvas_url}/api/v1/courses",
            headers=headers,
            params={"enrollment_state": "active", "per_page": 100},
            timeout=10,
        )
        courses = courses_response.json()

        if not isinstance(courses, list):
            return []

        assignments = []

        for course in courses:
            if not isinstance(course, dict):
                continue

            course_id = course.get("id")
            course_name = course.get("name", "Unknown Course")

            if not course_id:
                continue

            try:
                assignments_response = requests.get(
                    f"{canvas_url}/api/v1/courses/{course_id}/assignments",
                    headers=headers,
                    params={"per_page": 100},
                    timeout=10,
                )
                course_assignments = assignments_response.json()

                if not isinstance(course_assignments, list):
                    continue

                for assignment in course_assignments:
                    if not isinstance(assignment, dict):
                        continue

                    assignments.append({
                        "name":     assignment.get("name", "Untitled"),
                        "course":   course_name,
                        "due_at":   assignment.get("due_at"),
                        "html_url": assignment.get("html_url", ""),
                    })

            except Exception:
                continue

        return assignments

    except Exception:
        return []
