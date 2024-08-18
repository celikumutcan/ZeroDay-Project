import os
import sys

import psycopg2 as dbapi2

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
    """
]

# Function to initialize the database with the given URL
def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()

# Main execution block to run the initialization
if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py")
        sys.exit(1)
    initialize(url)