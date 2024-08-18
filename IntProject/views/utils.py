from functools import wraps
from flask import session, redirect, url_for

# Decorator to ensure the user is logged in before accessing the route
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:  # If the user is not logged in
            return redirect(url_for('login'))  # Redirect to the login page
        return f(*args, **kwargs)
    return decorated_function