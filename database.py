import sqlite3
import hashlib

def connect_sqlite3(dbname):
    connection = sqlite3.connect(dbname, check_same_thread=False)
    # connect to the database file with the given name
    return connection
    # return the connection object


# function to execute a database change command
def db_change(connection, sql):
    cursor = connection.cursor()
    # create a cursor object for database operations
    cursor.execute(sql)
    # execute the given SQL command
    connection.commit()
    # commit the changes made to the database


# function to execute a database query command
def db_query(connection, sql):
    cursor = connection.cursor()
    # create a cursor object for database operations
    cursor.execute(sql)
    # execute the given SQL command
    rows = cursor.fetchall()
    # fetch all rows returned by the command
    return rows
    # return the rows fetched from the database


connection = connect_sqlite3("parkingspots.db")

# create a SQL command to create the 'users' table if it does not exist
sql = """ CREATE TABLE IF NOT EXISTS parkingspots(
    ID INT,
    latitude TEXT,
    longitude TEXT
    );
"""

# execute the 'CREATE TABLE' command
db_change(connection, sql)


def add_new_parking_spot(latitude, longitude):
    # Check if a parking spot with the same latitude and longitude already exists
    latitude_hash = hashlib.sha256(str(latitude).encode()).hexdigest()
    longitude_hash = hashlib.sha256(str(longitude).encode()).hexdigest()
    sql = f"""SELECT * FROM parkingspots WHERE latitude = "{latitude_hash}" AND longitude = "{longitude_hash}" """
    rows = db_query(connection, sql)
    if len(rows) > 0:
        print("Parking spot already exists")
        return

    # If the parking spot doesn't exist, insert it into the database
    sql = """SELECT * FROM parkingspots"""
    rows = db_query(connection, sql)
    id = len(rows) + 1
    sql = f"""INSERT INTO parkingspots (ID,latitude,longitude) VALUES ("{id}","{latitude_hash}","{longitude_hash}");"""
    db_change(connection, sql)
    print("New parking spot added successfully")
