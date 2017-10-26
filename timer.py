#!/usr/bin/python3

import time
import sqlite3

import ui

DATABASE_FILE = "worktime.db"

def setup_db():
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    return cursor, connection

def teardown_db(connection):
    connection.commit()
    connection.close()

    
def generate_db(table = None):
    cursor, connection = setup_db()

    if not table:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS time"
            "(start REAL PRIMARY KEY, stop REAL, duration INTEGER)"
        )
    else:
        cursor.execute(
            (
                "CREATE TABLE IF NOT EXISTS {0}"
                "(start REAL PRIMARY KEY, stop REAL, duration INTEGER)"
            ).format(table)
        )

    teardown_db(connection)


def read_table(table = None):
    cursor, connection = setup_db()
    
    dblist = []
    if not table:
        cursor.execute('SELECT * FROM time')
    else:
        cursor.execute('SELECT * FROM {0}'.format(table))
    data = cursor.fetchall()
    for row in data:
        dblist.append(row)

    teardown_db(connection)
    return dblist

    
def enter_record(start, stop, duration, table = None):
    cursor, connection = setup_db()

    if not table:
        cursor.execute(
            "INSERT INTO time VALUES (?, ?, ?)",
            (start, stop, duration)
        )
    else:
        cursor.execute(
            "INSERT INTO {0} VALUES (?, ?, ?)".format(table),
            (start, stop, duration)
        )

    teardown_db(connection)


def worktime():
    start = time.time()
    input("Press enter when finished.\n")
    stop = time.time()
    duration = round(stop - start)
    return (start, stop, duration)

    
def main():
    generate_db()
    
    stamp = worktime()
    print("Time spent: ", round(stamp[2]/60, 1), "min\n")
    enter_record(stamp[0], stamp[1], stamp[2])
    
    total_seconds = 0
    for row in read_table():
        #print(row)
        total_seconds += row[2]
        
    print("In total ", round(total_seconds/3600, 2), " hours.")
    time.sleep(3)
    

if __name__ == "__main__":
    main()


    
