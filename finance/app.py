import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import time

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

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


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_id = session["user_id"]

    stocks = db.execute("SELECT stock, symbol, SUM(shares) AS shares FROM ledger WHERE user_id = ? GROUP BY stock", user_id)
    capital = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

    cashBalance = capital[0]["cash"]

    portfolioValue = 0

    for stock in stocks:
        currentStock = lookup(stock["symbol"])
        stock["name"] = currentStock["name"]
        price = currentStock["price"]
        stock["price"] = price
        stock["value"] = stock["shares"] * price
        portfolioValue += stock["value"]

    total = cashBalance + portfolioValue

    return render_template("index.html", stocks=stocks, portfolioValue=portfolioValue, cashBalance=cashBalance, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "GET":

        return render_template("buy.html")

    elif request.method == "POST":

        now = datetime.now()
        offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
        offset = offset / 60 / 60 * -1

        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        # check if user inputted a number
        try:
            float(shares)
        except:
            return apology("invalid number of shares", 400)

        # check if the user inputted a valid symbol
        if not symbol:
            return apology("invalid symbol", 400)

        elif lookup(symbol) == None:
            return apology("invalid symbol", 400)

        # check if the user inputted a valid number of shares
        elif float(shares) < 1 or float(shares) % 1 != 0:
            return apology("invalid number of shares", 400)

        # lookup the stock
        quote = lookup(symbol)

        stock = {"name": quote["name"],
        "symbol": quote["symbol"],
        "price": quote["price"]}

        # calculate total price
        total_price = float(shares) * stock["price"]

        user_id = session["user_id"]

        # ensure user has enough money
        sql_capital = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = float(sql_capital[0]["cash"])

        if cash < total_price:

            return apology("not enough cash", 400)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - total_price, user_id)
        db.execute("CREATE TABLE IF NOT EXISTS ledger (user_id INTEGER NOT NULL, transaction_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, date_time, stock TEXT NOT NULL, symbol TEXT NOT NULL, shares INTEGER NOT NULL, price INTEGER NOT NULL, total_price INTEGER NOT NULL, transaction_type TEXT NOT NULL, UTC_offset INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))")
        db.execute("INSERT INTO ledger (user_id, date_time, UTC_offset, stock, symbol, shares, price, total_price, transaction_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", user_id, now, offset, stock["name"], stock["symbol"], shares, stock["price"], total_price, "buy")

        flash("purchased!")
        
        return redirect("/")




@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_id = session["user_id"]

    history = db.execute("SELECT transaction_id, stock, symbol, shares, price, total_price, transaction_type, date_time FROM ledger WHERE user_id = ?", user_id)

    for index in range(len(history)):
        history[index]["shares"] = abs(history[index]["shares"])

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("logged in!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("logged out!")

    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":

        return render_template("quote.html")

    elif request.method == "POST":

        symbol = request.form.get("symbol").upper()

        # ensure there is a symbol
        if not symbol:

            return apology("invalid symbol", 400)

        else:

            # lookup the symbol
            quote = lookup(symbol)

            # check if the symbol is valid
            try:

                stock = {"name": quote["name"],
                "symbol": quote["symbol"],
                "price": usd(quote["price"])}

            except TypeError:

                return apology("invalid symbol", 400)

            # pass the data into the html file if the symbol is valid
            else:

                now = datetime.now()
                offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
                offset = offset / 60 / 60 * -1
                return render_template("quoted.html", stock=stock, now=now, offset=offset)

    else:

        return apology("method not allowed", 405)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hash = generate_password_hash(password)

        # Ensure username was submitted

        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        # Ensure passwords match

        elif password != confirmation:
            return apology("passwords must match", 400)

        # password requirements
        elif len(request.form.get("password")) < 5:
            return apology("password must be 5 or more characters", 400)

        # Check if username exists

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) == 1:
            return apology("username already taken", 400)

        # Insert user into database

        db.execute("INSERT into users (username, hash) VALUES(?, ?)", username, hash)

        # Pull new user id
        new_user_id = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Remember which user has logged in

        session["user_id"] = new_user_id[0]["id"]

        # Redirect user to home page

        flash("registered!")

        return redirect("/")

    elif request.method == "GET":

        return render_template("register.html")

    else:

        return apology("method not allowed", 405)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "GET":

        user_id = session["user_id"]

        portfolio = db.execute("SELECT DISTINCT symbol FROM ledger WHERE user_id = ?", user_id)

        owned_symbols = []

        for index in range(len(portfolio)):
            owned_symbols.append(portfolio[index]["symbol"])

        return render_template("sell.html", owned_symbols=owned_symbols)

    elif request.method == "POST":

        now = datetime.now()
        offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
        offset = offset / 60 / 60 * -1
        user_id = session["user_id"]

        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")
        portfolio = db.execute("SELECT * FROM ledger WHERE user_id = ? AND symbol = ?", user_id, symbol)

        # check if the user inputted a valid symbol
        if not symbol:
            return apology("invalid symbol", 400)

        elif lookup(symbol) == None:
            return apology("invalid symbol", 400)

        # check if the user inputted a valid number of shares
        elif float(shares) <= 0 or float(shares) == ValueError:
            return apology("invalid number of shares", 400)

        # to do check if user inputted symbol is owned by the user
        if len(portfolio) < 1:
            return apology("you don't own this stock", 400)

        # lookup the stock
        quote = lookup(symbol)

        stock = {"name": quote["name"],
        "symbol": quote["symbol"],
        "price": quote["price"]}

        # calculate total sale price
        total_price = float(shares) * float(stock["price"])

        # ensure user has enough shares
        sql_shares = db.execute("SELECT SUM(shares) AS shares FROM ledger WHERE user_id = ? AND symbol = ?", user_id, symbol)

        if not sql_shares:
            return apology("no shares to sell", 400)

        owned_shares = float(sql_shares[0]["shares"])
        shares = float(shares)

        if shares > owned_shares:
            return apology("not enough shares", 400)

        sql_capital = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = float(sql_capital[0]["cash"])

        ledger_shares = shares * -1

        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + total_price, user_id)
        db.execute("INSERT INTO ledger (user_id, date_time, UTC_offset, stock, symbol, shares, price, total_price, transaction_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", user_id, now, offset, stock["name"], stock["symbol"], ledger_shares, stock["price"], total_price, "sell")

        flash("SOLD!")

        return redirect("/")
