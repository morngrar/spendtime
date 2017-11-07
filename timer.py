#!/usr/bin/python3

import time
import sqlite3
import sys
import logging
import os

try:
    os.remove("timetable.log")
except:
    pass

# Uncomment if debug log is needed
#logging.basicConfig(filename="timetable.log", level=logging.DEBUG)

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

def list_tables():
    cursor, connection = setup_db()
    result = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )
    returnlist = []
    for data in result:
        returnlist.append(data[0])
    teardown_db(connection)
    return returnlist

def worktime():
    start = time.time()
    input("Press enter when finished.\n")
    stop = time.time()
    duration = round(stop - start)
    return (start, stop, duration)

def run_worktime(table = None):
    stamp = worktime()
    print("Time spent: ", round(stamp[2]/60, 1), "min\n")
    enter_record(stamp[0], stamp[1], stamp[2], table)

    total_seconds = 0
    for row in read_table(table):
        total_seconds += row[2]

    print("In total ", round(total_seconds/3600, 2), " hours.")
    time.sleep(3)


def menu():
    print(list_tables())


def this_table(text = None):
    """Run worktime with specific table. Fails on non-existing table"""
    global ARGUMENT_TEXT

    if not text:
        ARGUMENT_TEXT = True
        return

    tables = list_tables()
    if text not in tables:
        print("This timetable doesn't exist yet!")
        return

    run_worktime(table=text)

def main():
    global ARGUMENT_TEXT
    ARGUMENT_TEXT = False   # if true, the argument is text needed for function
    ARGUMENT_DICT = {
        "-m":menu,
        "-t":this_table
    }

    generate_db()

    last_argument = None
    if len(sys.argv) > 1:
        for argument in sys.argv:
            logging.debug("Start of argument loop: {0}".format(argument))

            if ARGUMENT_TEXT:
                logging.debug("Argument text true")

                ARGUMENT_DICT[last_argument](text = argument)
                ARGUMENT_TEXT = False

                logging.debug("returned from argument function")
            else:
                logging.debug("Argument text false")

                if argument not in ARGUMENT_DICT.keys():
                    logging.debug("Argument not in dict")
                    continue

                logging.debug("calling argument function")
                ARGUMENT_DICT[argument]()

                logging.debug(
                    "returned from argument function(text false)"
                )
            last_argument = argument
    else:
        logging.debug("arguments <= 1")
        run_worktime()

if __name__ == "__main__":
    main()
