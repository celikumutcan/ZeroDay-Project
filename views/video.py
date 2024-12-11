from flask import Blueprint, request, render_template, redirect, url_for, flash
from views.utils import login_required
from queries import select, insert, delete, update

# Creates a Blueprint for the video module
video = Blueprint("video", import_name=__name__, template_folder="templates")

# Defines a route for the videos page, accessible via GET and POST methods
@video.route("/", methods=['GET', 'POST'])
@login_required
def videos_page():
    # Fetches video details from the database
    if request.method == "GET":
        videos = select("id, name, url, likes, dislikes", "video", asDict=True)
        return render_template("videos_page.html", videos=videos)

    elif request.method == "POST":
        video_id = request.form.get('video_id')
        action = request.form.get('action')

        if action == "like":
            # Increments the like count for the video
            update("video", "likes=likes+1", f"id={video_id}")
            flash("You liked the video!", "success")

        elif action == "dislike":
            # Increments the dislike count for the video
            update("video", "dislikes=dislikes+1", f"id={video_id}")
            flash("You disliked the video!", "success")

        elif action == "delete":
            # Deletes the video from the database
            if video_id:
                delete("video", f"id={video_id}")
                flash("Video deleted successfully!", "success")

        # Redirects to the videos page after updating
        return redirect(url_for('video.videos_page'))

# Defines a route for adding a new video, accessible via POST method
@video.route("/add", methods=['POST'])
@login_required
def add_video():
    name = request.form.get('video_name')
    url = request.form.get('video_url')

    if name and url:
        insert("video", "name, url, likes, dislikes", f"'{name}', '{url}', 0, 0")
        flash("Video added successfully!", "success")
    else:
        flash("Please provide both name and URL.", "error")

    return redirect(url_for('video.videos_page'))