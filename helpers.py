import datetime
from functools import wraps
from flask import redirect, render_template, session

def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", top=code, bottom=message), code

def login_required(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_time():
    """Return current time as a string for message timestamps."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_time(timestr):
    """
    Format a time string (YYYY-MM-DD HH:MM:SS) to a more readable format.
    Example output: 'Apr 29, 2025, 03:15 PM'
    """
    try:
        dt = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%b %d, %Y, %I:%M %p")
    except Exception:
        return timestr  # fallback to original if parsing fails
