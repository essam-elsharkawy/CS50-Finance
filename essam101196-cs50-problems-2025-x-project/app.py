from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



def init_db():
    with sqlite3.connect("finance.db") as conn:
        cur = conn.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        hash TEXT NOT NULL
                    )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        amount REAL NOT NULL,
                        category TEXT NOT NULL,
                        note TEXT,
                        date TEXT NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )""")
init_db()


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")

    with sqlite3.connect("finance.db") as conn:
        cur = conn.cursor()
        cur.execute("""SELECT amount, category, note, date
                       FROM expenses
                       WHERE user_id = ?
                       ORDER BY date DESC
                       LIMIT 10""", (session["user_id"],))
        expenses = cur.fetchall()

    return render_template("index.html", expenses=expenses)



@app.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect("/login")

    amount = request.form.get("amount")
    category = request.form.get("category")
    note = request.form.get("note")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect("finance.db") as conn:
        cur = conn.cursor()
        cur.execute("""INSERT INTO expenses (user_id, amount, category, note, date)
                       VALUES (?, ?, ?, ?, ?)""",
                       (session["user_id"], amount, category, note, date))
        conn.commit()

    return redirect("/")



@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect("/login")

    with sqlite3.connect("finance.db") as conn:
        cur = conn.cursor()
        cur.execute("""SELECT amount, category, note, date
                       FROM expenses
                       WHERE user_id = ?
                       ORDER BY date DESC""", (session["user_id"],))
        expenses = cur.fetchall()

    return render_template("history.html", expenses=expenses)



@app.route("/chart")
def chart():
    if "user_id" not in session:
        return redirect("/login")

    with sqlite3.connect("finance.db") as conn:
        cur = conn.cursor()
        cur.execute("""SELECT category, SUM(amount)
                       FROM expenses
                       WHERE user_id = ?
                       GROUP BY category""", (session["user_id"],))
        rows = cur.fetchall()

    categories = [row[0] for row in rows]
    amounts = [row[1] for row in rows]

    return render_template("chart.html", categories=categories, amounts=amounts)



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # تحقق من البيانات
        if not username:
            return "Must provide username"
        if not password:
            return "Must provide password"
        if password != confirmation:
            return "Passwords do not match"

        # تشفير الباسورد
        hash = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return "Username already exists"

        return redirect("/login")

    else:
        return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        with sqlite3.connect("finance.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, hash FROM users WHERE username = ?", (username,))
            user = cur.fetchone()

        if user is None or not check_password_hash(user[1], password):
            return "Invalid username or password"

        session["user_id"] = user[0]
        return redirect("/")

    return render_template("login.html")



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")



if __name__ == "__main__":
    app.run(debug=True)
