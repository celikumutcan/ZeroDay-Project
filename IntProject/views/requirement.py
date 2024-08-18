from flask import Blueprint, render_template
from views.utils import login_required

# Creates a Blueprint for the requirement module
requirement = Blueprint("requirement", import_name=__name__, template_folder="templates")

# Defines a route for the requirement page, accessible only to logged-in users
@requirement.route("/")
@login_required 
def requirement_page():
    return render_template("requirement_page.html")
