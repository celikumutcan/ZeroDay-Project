# This script provides utility functions for interacting with a PostgreSQL database.
# - `insert`: Inserts a new record into a specified table.
# - `select`: Retrieves records from a specified table with optional filtering.
# - `update`: Updates existing records in a specified table.
# - `delete`: Deletes records from a specified table.
# - `run`: Executes the given SQL query and handles database connections and errors.
# -*- coding: utf-8 -*-
import os
import psycopg2 as db

def insert(table, columns, values, returnID=True):
    if returnID:
        query = """INSERT INTO {} ({}) VALUES({}) RETURNING id""".format(table, columns, values)
        return run(query)
    else:
        query = """INSERT INTO {} ({}) VALUES({})""".format(table, columns, values)
        run(query)

def select(columns, table, where=None, asDict=False):
    keywords = []
    if asDict:
        keywords = columns.replace(' ', '').split(',')
    if where is not None:
        query = """SELECT {} FROM {} WHERE {}""".format(columns, table, where)
    else:
        query = """SELECT {} FROM {}""".format(columns, table)
    return run(query, keywords)

def update(table, columns, where):
    query = """UPDATE {} SET {} WHERE {}""".format(table, columns, where)
    print(f"Executing Query: {query}")  # Sorgu çıktısı ekleyin
    run(query)

def delete(table, where):
    query = """DELETE FROM {} WHERE {}""".format(table, where)
    run(query)

def run(query, keywords=[]):
    connection = None
    cursor = None
    result = None
    print("\nAttempted Query \n", query, "\n--------\n")
    try:
        connection = db.connect(os.getenv("DATABASE_URL"))
        cursor = connection.cursor()
        cursor.execute(query)
        if not ('DROP' in query or 'UPDATE' in query or 'DELETE' in query):
            result = cursor.fetchall()
    except db.DatabaseError as dberror:
        if connection is not None:
            connection.rollback()
        result = dberror
        print("Error:::", result)
    finally:
        if connection is not None:
            connection.commit()
            connection.close()
        if cursor is not None:
            cursor.close()
        if keywords:
            final_result = [list(i) for i in result]
            result_dict_array = []
            for row in final_result:
                dictionary = {}
                for i, keyword in enumerate(keywords):
                    dictionary[keyword] = row[i]
                result_dict_array.append(dictionary)
            if len(result_dict_array) == 1:
                return result_dict_array[0]
            return result_dict_array
        return result