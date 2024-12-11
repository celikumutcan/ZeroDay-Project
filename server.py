from flask import Flask, redirect, url_for, render_template, request, session, flash
from psycopg2 import extensions
from queries import *

# Importing the requirement Blueprint
from danfoss_ZeroDay import initialize
from views.admin import admin
from views.requirement import requirement
from views.utils import login_required
from views.video import video

# Register Unicode extensions for PostgreSQL
extensions.register_type(extensions.UNICODE)
extensions.register_type(extensions.UNICODEARRAY)

app = Flask(__name__)
app.secret_key = 'METUNCC'  # Secret key for session management

# Registering Blueprints for modular route handling
# Registering Blueprints for modular route handling
app.register_blueprint(requirement, url_prefix="/requirement")
app.register_blueprint(video, url_prefix="/videos")
app.register_blueprint(admin, url_prefix="/admin")

# Database configuration
HEROKU = True
if not HEROKU:
    os.environ['DATABASE_URL'] = "dbname='danfoss_db' user='postgres' host='localhost' password='umut62'"
    initialize(os.environ.get('DATABASE_URL'))  # Initialize the database connection

# Route for the home page, requires user to be logged in
@app.route("/")
@login_required  # Ensure the user is logged in
def home_page():
    return render_template("home_page.html")  # Render the home page template

# Route for the login page, handles GET and POST methods
@app.route("/login", methods=["GET", "POST"])
def login():
    if 'username' in session:  # Check if the user is logged in
        return redirect(url_for('home_page'))  # Redirect to the home page

    if request.method == "POST":  # If the form is submitted
        username = request.form.get("username")  # Get username
        password = request.form.get("password")  # Get password

        # Validate the input fields
        if not username:
            flash("Username cannot be empty.", "warning")
            return redirect(url_for('login'))  # Redirect back to log in
        if not password:
            flash("Password cannot be empty.", "warning")
            return redirect(url_for('login'))  # Redirect back to log in

        # Query to get user information from the database
        user = select("username, password, is_admin", "users", f"username='{username}'", asDict=True)

        # Check if the user exists and validate the password
        if not user:
            flash("No such username found.", "danger")
            return redirect(url_for('login'))  # Redirect back to log in
        elif user['password'] != password:  # If the password is incorrect
            flash("Incorrect password.", "danger")
            return redirect(url_for('login'))  # Redirect back to log in
        else:
            # Set session variables for the logged-in user
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']  # Add the admin status to the session
            return redirect(url_for('home_page'))  # Redirect to the home page

    return render_template("login_page.html")  # Render the login page template

# Route for logging out, requires user to be logged in
@app.route("/logout")
@login_required
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('login'))

# Main entry point for the application
if __name__ == "__main__":
    app.run(debug=True if not HEROKU else False)  # Run the app in debug mode for local development