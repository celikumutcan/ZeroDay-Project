ZeroDay Project

Project Description
My ZeroDay Project is designed to help new employees by giving them all the important documents and safety videos they need before their first day. This way, they’re prepared in advance, making the onboarding process smoother and saving time.

Technology Stack

For the backend, I chose Python Flask because it's lightweight and powerful.
The frontend is built with HTML, CSS, and Bootstrap for a clean, responsive design.
PostgreSQL is my database, initially set up locally but now expanded with admin functionalities.
I'm using Blueprint in Flask to keep my code organized.
For cloud deployment, Heroku will be used in the next stage.
Features

User Authentication: Users log in with a username and password for secure access.
Documents Section: Displays a list of important documents for new employees.
Videos Section: Contains essential workplace safety videos.
Admin Functionality:
Admins can now manage users, videos, and requirements directly via an admin dashboard.
They can add, update, or delete users, videos, and requirements dynamically.
Project Structure

HTML Files: Stored in "templates/" and extend from "base.html".
CSS Files: Custom styles are kept in "static/css/".

Python Files:
"server.py" manages the main server setup and routes, now including admin functionalities.
"requirement.py", "video.py", and "utils.py" handle specific sections like requirements and videos.
"queries.py" includes functions for database operations.
"admin.py" is newly added for admin-related backend functionality.
Templates:
"login_page.html", "home_page.html", "required_documents_page.html", "videos_page.html", and "admin_dashboard.html".
Usage

Home Page: Overview and navigation links for employees and admins.
Required Documents Section: Employees can view required documents. Admins can add/delete them.
Videos Section: Employees can view videos. Admins can add/delete them.
Admin Dashboard: Accessible only by admins for user and content management.

Future Milestones

Complete deployment on Heroku with Heroku Postgres for the database.
Conduct unit tests and optimize the app for scalability.
Simulate real-world usage by testing with a larger dataset.
Submission Tracking

Proposal: My initial project proposal is saved in the proposal/ directory.
Progress Report: Progress report files are saved in the progress_report/ directory.
Final Report: The final report is saved in the final_report/ directory.

Created by
Umutcan CELIK - 2024