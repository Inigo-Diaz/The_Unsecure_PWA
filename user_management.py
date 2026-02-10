import secrets
import bcrypt
import sqlite3 as sql
import time
import random


def insertUser(username, password, DoB):
    # 1. Generate a salt (random data added to the password)
    salt = bcrypt.gensalt()
    # 2. Hash the password (one-way scramble)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    # 3. Insert the HASH instead of the raw password
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)",
        (username, hashed_password.decode("utf-8"), DoB),
    )
    con.commit()
    con.close()


def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()

    # 1. FIX: Use Parameterized Query (Fixes SQL Injection too!)
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    con.close()

    # 2. FIX: Normalize the Data
    # If the user exists, we use their real password hash.
    # If not, we use a fake one. This ensures the next steps run regardless.
    if row:
        stored_password = row[0]
    else:
        stored_password = "invalid_placeholder_password"

    # 3. FIX: Always do the File I/O
    # Previously, this only happened for valid users (leaking info).
    # Now we do it for everyone.
    try:
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
        with open("visitor_log.txt", "w") as file:
            file.write(str(number + 1))
    except:
        pass  # Ignore file errors for this demo

    # 4. FIX: Constant Time Comparison
    # secrets.compare_digest takes the same time whether it matches or not.
    # We compare the input password against either the real or the fake one.
    is_valid = secrets.compare_digest(stored_password, password)

    # 5. Return Result
    # Only return True if the user actually existed AND password matched.
    if row and is_valid:
        return True
    else:
        return False


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()
