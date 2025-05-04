from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Session config
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database
db = SQL("sqlite:///chat.db")

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def apology(message, code=400):
    return render_template("apology.html", top=code, bottom=message), code


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return apology("must provide username", 400)
        if not password:
            return apology("must provide password", 400)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        return redirect("/messages")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return apology("must provide username", 400)
        if not password:
            return apology("must provide password", 400)
        if password != confirmation:
            return apology("passwords don't match", 400)
        existing = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing:
            return render_template("apology_username.html")
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            generate_password_hash(password)
        )
        flash("Registered successfully! Please log in.")
        return redirect("/login")
    return render_template("register.html")


@app.route("/messages", methods=["GET", "POST"])
@login_required
def messages():
    if request.method == "POST":
        recipient = request.form.get("recipient")
        message = request.form.get("message")
        if not recipient:
            return apology("must provide a recipient", 400)
        if not message:
            return apology("must provide a message", 400)
        user = db.execute("SELECT id FROM users WHERE username = ?", recipient)
        if not user:
            return apology("recipient does not exist", 400)
        db.execute(
            "INSERT INTO messages (message, sender_id, recipient_id) VALUES (?, ?, ?)",
            message,
            session["user_id"],
            user[0]["id"]
        )
        flash("Message sent!")
        return redirect("/messages")
    messages = db.execute("""
        SELECT messages.message, messages.time,
               sender.username AS sender_username,
               recipient.username AS recipient_username
        FROM messages
        JOIN users sender ON messages.sender_id = sender.id
        JOIN users recipient ON messages.recipient_id = recipient.id
        WHERE messages.sender_id = ? OR messages.recipient_id = ?
        ORDER BY messages.time DESC
    """, session["user_id"], session["user_id"])
    return render_template("messages.html", messages=messages)


@app.errorhandler(404)
def not_found(e):
    return apology("Page not found", 404)


if __name__ == "__main__":
    app.run(debug=True)
