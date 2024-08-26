import os
import time
import csv
import datetime
import pytz
import requests
import urllib
import uuid

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, render_template, request, session
from functools import wraps
from datetime import datetime
import pytz

from helpers import login_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///blog.db")

@app.route("/")
def index():
    return render_template("layout.html")

@app.route("/layout")
def layout():
    return render_template("layout.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if password != confirmation:
            return render_template("error.html", message="Password does not match confirmation password!")

        hash = generate_password_hash(password)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 0:
            db.execute("INSERT INTO Users (username, password_hash) VALUES(?, ?)", username, hash)
            return redirect("/")
        else:
            return render_template("error.html", message="Username already exists!")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1:
            return render_template("error.html", message="unregistered username!")
        elif not check_password_hash(rows[0]["password_hash"], request.form.get("password")):
            return render_template("error.html", message="incorrect password!")

        session["user_id"] = rows[0]["id"]

        return redirect(url_for('display_blogs'))

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()
    
    return redirect("/")

@app.route("/post_blog", methods=["GET", "POST"])
@login_required
def post_blog():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("blog_content")
        user_id = session["user_id"]
        edt = pytz.timezone('US/Eastern')
        current_time = datetime.now(edt)
        db.execute("INSERT INTO Posts (user_id, title, content, created_at) VALUES (?, ?, ?, ?)", user_id, title, content, current_time)
        db.execute("UPDATE Users SET blog_count = blog_count + 1 WHERE id = ?", user_id)
        return redirect("/home")
    else:
        return render_template("post.html")

@app.route("/home", methods=["GET", "POST"])
@login_required
def display_blogs():
    user_id = session["user_id"]
    blogs = db.execute("SELECT * FROM Posts WHERE user_id = ?", user_id)
    blog_count = db.execute("SELECT blog_count FROM Users WHERE id = ?", user_id)[0]["blog_count"]
    return render_template("home.html", blogs=blogs, blog_count=blog_count)

@app.route("/post")
def post():
    return render_template("post.html")

@app.route("/delete_blog", methods=["DELETE"])
@login_required
def delete():
    blog_id = request.args.get("blogId")
    user_id = session["user_id"]
    db.execute("DELETE FROM Posts WHERE id = ? AND user_id = ?", blog_id, user_id)
    db.execute("UPDATE Users SET blog_count = blog_count - 1 WHERE id = ?", user_id)
    return jsonify({"success": True, "message": "Blog successfully deleted."})

@app.route("/edit_blog", methods=["GET", "PUT"])
@login_required
def edit_or_update_blog():
    user_id = session["user_id"]

    if request.method == "GET":
        blog_id = request.args.get("blogId")
        blog = db.execute("SELECT title, content FROM Posts WHERE user_id = ? AND id = ?", user_id, blog_id)
        if blog:
            return jsonify(success=True, title=blog[0]['title'], content=blog[0]['content'])
        else:
            return jsonify(success=False), 404

    elif request.method == "PUT":
        blog_id = request.form.get("blogId")
        title = request.form.get("title")
        content = request.form.get("content")
        result = db.execute("UPDATE Posts SET title = ?, content = ? WHERE user_id = ? AND id = ?", title, content, user_id, blog_id)
        if result:
            return jsonify(success=True)
        else:
            return jsonify(success=False), 404
