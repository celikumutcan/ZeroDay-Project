from flask import Blueprint, render_template, request, redirect, url_for, flash
from danfoss_ZeroDay import add_user, get_all_users, delete_user_by_id

# Create the admin Blueprint with a specific URL prefix
admin = Blueprint('admin', __name__, template_folder='templates')  # Prefix can be added during registration

# Renders the admin dashboard page with a list of users
@admin.route('/dashboard')
def dashboard():
    users = get_all_users()  # Fetches all users from the database
    return render_template('admin/admin_dashboard_page.html', users=users)

# Handles adding a new user, accessible via GET and POST methods
@admin.route('/add_user', methods=['GET', 'POST'])
def add_user_route():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_admin = request.form.get('is_admin') == 'on'

        if username and password:
            add_user(username, password, is_admin)
            flash("User added successfully!", "success")
            return redirect(url_for('admin.dashboard'))
        else:
            flash("Please provide a valid username and password.", "danger")
    return render_template('admin/add_user.html')

# Deletes a user based on the provided user ID
@admin.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    delete_user_by_id(user_id)
    flash("User deleted successfully!", "success")
    return redirect(url_for('admin.dashboard'))