from flask import Blueprint, render_template, request, redirect, url_for, flash
from views.utils import login_required
from danfoss_ZeroDay import add_requirement_to_db, get_all_requirements, delete_requirement_by_id

requirement = Blueprint("requirement", import_name=__name__, template_folder="templates")

# Renders the requirements page after checking if the user is logged in
@requirement.route("/")
@login_required
def requirement_page():
    requirements = get_all_requirements()
    return render_template("required_documents_page.html", requirements=requirements)

# Adds a new requirement to the database if the requirement name is provided
@requirement.route('/add_requirement', methods=['POST'])
@login_required
def add_requirement():
    requirement_name = request.form.get('requirement_name')
    if requirement_name:
        add_requirement_to_db(requirement_name)
        flash("Requirement added successfully!", "success")
    else:
        flash("Please provide a valid requirement name.", "danger")
    return redirect(url_for('requirement.requirement_page'))

# Deletes a requirement from the database based on the provided requirement ID
@requirement.route('/delete_requirement/<int:requirement_id>', methods=['POST'])
@login_required
def delete_requirement(requirement_id):
    delete_requirement_by_id(requirement_id)
    flash("Requirement deleted successfully!", "success")
    return redirect(url_for('requirement.requirement_page'))