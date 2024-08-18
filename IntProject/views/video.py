from flask import Blueprint, request, render_template, redirect, url_for
from queries import *
from views.utils import login_required

# Creates a Blueprint for the video module
video = Blueprint("video", __name__, template_folder="templates")

# Defines a route for the videos page, accessible via GET and POST methods
@video.route("/", methods=['GET', 'POST'])
@login_required
def videos_page():
    if request.method == "GET":
        # Fetches video details from the database
        videos = select("id, name, url, likes, dislikes", "video", asDict=True)
        return render_template("videos_page.html", videos=videos)
    elif request.method == "POST":
        video_id = request.form.get('video_id')
        action = request.form.get('action')
        
        # Debugging output
        print(f"Video ID: {video_id}")
        print(f"Action: {action}")
        
        if action == "like":
            # Increments the like count for the video
            update("video", "likes=likes+1", f"id={video_id}")
        elif action == "dislike":
            # Increments the dislike count for the video
            update("video", "dislikes=dislikes+1", f"id={video_id}")
        
        # Redirects to the videos page after updating
        return redirect(url_for('video.videos_page'))