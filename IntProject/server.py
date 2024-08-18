import os
from flask import Flask, redirect, url_for, render_template, request, session, flash
from psycopg2 import extensions
from queries import *
from views.requirement import requirement  # Importing the requirement Blueprint
from danfoss_ZeroDay import initialize
from views.utils import login_required
from views.video import video

# Register Unicode extensions for PostgreSQL
extensions.register_type(extensions.UNICODE)
extensions.register_type(extensions.UNICODEARRAY)

app = Flask(__name__)
app.secret_key = 'bestoneMETUNCC'  # Adding a secret key for session management

# Registering Blueprints
app.register_blueprint(requirement, url_prefix="/requirement")
app.register_blueprint(video, url_prefix="/videos")

HEROKU = False
if not HEROKU: 
    os.environ['DATABASE_URL'] = "dbname='danfoss_db' user='postgres' host='localhost' password='umut62'"
    initialize(os.environ.get('DATABASE_URL'))

# Route for the home page, requires login
@app.route("/")
@login_required
def home_page():
    return render_template("home_page.html")

# Route for the login page, handles GET and POST methods
@app.route("/login", methods=["GET", "POST"])
def login():
    if 'username' in session:
        return redirect(url_for('home_page'))
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Check if username or password fields are empty
        if not username:
            flash("Username cannot be empty.", "warning")
            return redirect(url_for('login'))  # Refresh the page
        if not password:
            flash("Password cannot be empty.", "warning")
            return redirect(url_for('login'))  # Refresh the page
        
        # Verify user credentials from the database
        user = select("username, password", "users", f"username='{username}'", asDict=True)
        
        if not user:
            flash("No such username found.", "danger")
            return redirect(url_for('login'))  # Refresh the page
        elif user['password'] != password:
            flash("Incorrect password.", "danger")
            return redirect(url_for('login'))  # Refresh the page
        else:
            session['username'] = user['username']  # Start the session
            return redirect(url_for('home_page'))
    
    return render_template("login.html")

# Route for logging out, requires login
@app.route("/logout")
@login_required
def logout():
    session.pop('username', None)  # End the session
    return redirect(url_for('login'))

if __name__ == "__main__":
    if not HEROKU:
        app.run(debug=True)
    else:
        app.run()