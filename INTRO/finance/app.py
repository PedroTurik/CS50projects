import os

from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# disputario


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# salafrario


@app.route("/")
@login_required
def index():
    balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    total_balance = balance
    stocks = db.execute("SELECT symbol, SUM(quantity) FROM history WHERE account_id=? GROUP BY symbol", session["user_id"])
    cur_price = []
    for i, x in enumerate(stocks):
        temp = lookup(x["symbol"])["price"]
        cur_price.append(temp)
        total_balance += stocks[i]["SUM(quantity)"]*cur_price[i]

    return render_template("index.html", stocks=stocks, cur_price=cur_price, balance=balance, total_balance=total_balance)
# umanitario


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        info = lookup(request.form.get("symbol"))
        quantity = request.form.get("shares")
        if not info or not quantity:
            return apology("fill all fields correctly", 400)
        try:
            quantity = int(quantity)
        except:
            return apology("incorrect input")
        if quantity <= 0:
            return apology("incorrect input", 400)
        symbol = info["symbol"]
        price = info["price"]
        # colagem aqui
        date = datetime.now()
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        cash = cash - (price*quantity)
        if cash < 0:
            return apology("not enough money", 400)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
        db.execute("INSERT INTO history (account_id, symbol, price, quantity, date) VALUES(?, ?, ?, ?, ?)",
                   session["user_id"], symbol, price, quantity, date)
        return redirect("/")
    else:
        return render_template("buy.html")

# pitoresco


@app.route("/history")
@login_required
def history():
    history = db.execute("SELECT symbol, price, quantity, date FROM history WHERE account_id=?", session["user_id"])
    return render_template("history.html", history=history)

# sabinado


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# chucrute


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# comissario


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if quote:
            return render_template("quoted.html", quote=quote)
        else:
            return apology("non-existant quote")
    else:
        return render_template("quote.html")

# commentsario


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        used_name = db.execute("SELECT username FROM users WHERE username = ?", name)
        if password != confirmation:
            return apology("password and confirmation are not equal", 400)
        if name and password and confirmation:
            if used_name:
                return apology("username already taken", 400)
            else:
                db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", name, generate_password_hash(password))
                return redirect("/login")
        return apology("empty fields", 400)
    else:
        return render_template("register.html")

# comentario


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        info = lookup(request.form.get("symbol"))
        quantity = request.form.get("shares")
        if not info or not quantity:
            return apology("input error", 400)
        symbol = info["symbol"]
        price = info["price"]
        try:
            quantity = int(quantity)
        except:
            return apology("incorrect input", 400)
        if quantity <= 0:
            return apology("incorrect input", 400)
        date = datetime.now()
        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        new_cash = current_cash + (price*quantity)
        share = db.execute("SELECT symbol, SUM(quantity) FROM history WHERE account_id=? and symbol=? GROUP BY symbol", session["user_id"],
                           symbol)[0]["SUM(quantity)"]
        if share < quantity:
            return apology("not enough shares", 400)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])
        db.execute("INSERT INTO history (account_id, symbol, price, quantity, date) VALUES(?, ?, ?, ?, ?)",
                   session["user_id"], symbol, price, -1*quantity, date)
        return redirect("/")
    else:
        owned_stocks = db.execute("SELECT DISTINCT symbol FROM history WHERE account_id=?", session["user_id"])
        return render_template("sell.html", owned_stocks=owned_stocks)
        # libertario