import os  # For accessing environment variables
import sys  # For system-specific parameters and functions
import psycopg2 as dbapi2  # PostgreSQL database interaction

# SQL statements to initialize the database tables
INIT_STATEMENTS = [
    """
    create table if not exists users(
        id serial primary key,
        username varchar not null unique,
        password varchar not null
    )
    """,
    """
    create table if not exists video(
        id serial primary key,
        name varchar not null,
        url varchar not null,
        likes integer default 0 not null,
        dislikes integer default 0 not null
    )
    """,
    """
    ALTER TABLE users ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT FALSE
    """,
    """
    create table if not exists requirements(
        id serial primary key,
        name varchar not null
    )
    """
]

# Initialize the database with the given URL
def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()

# Function to add a user
def add_user(username, password, is_admin):
    """Insert a new user into the users table."""
    query = """
    INSERT INTO users (username, password, is_admin)
    VALUES (%s, %s, %s)
    """
    params = (username, password, is_admin)

    with dbapi2.connect(os.getenv("DATABASE_URL")) as connection:
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()

# Function to get all users
def get_all_users():
    """Retrieve all users from the users table."""
    query = "SELECT id, username, password, is_admin FROM users"
    with dbapi2.connect(os.getenv("DATABASE_URL")) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        users = cursor.fetchall()
    return users

# Function to delete a user by ID
def delete_user_by_id(user_id):
    """Delete a user by their ID from the users table."""
    query = "DELETE FROM users WHERE id = %s"
    with dbapi2.connect(os.getenv("DATABASE_URL")) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        connection.commit()

# Function to add a requirement
def add_requirement_to_db(name):
    """Insert a new requirement into the requirements table."""
    query = """
    INSERT INTO requirements (name)
    VALUES (%s)
    """
    params = (name,)

    with dbapi2.connect(os.getenv("DATABASE_URL")) as connection:
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()

# Function to get all requirements
def get_all_requirements():
    """Retrieve all requirements from the requirements table."""
    query = "SELECT id, name FROM requirements"
    with dbapi2.connect(os.getenv("DATABASE_URL")) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        requirements = cursor.fetchall()
    return requirements

# Function to delete a requirement by ID
def delete_requirement_by_id(requirement_id):
    """Delete a requirement by its ID from the requirements table."""
    query = "DELETE FROM requirements WHERE id = %s"
    with dbapi2.connect(os.getenv("DATABASE_URL")) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (requirement_id,))
        connection.commit()

# Main execution to run the initialization
if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python danfoss_ZeroDay.py")
        sys.exit(1)
    initialize(url)