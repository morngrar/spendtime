#!/usr/bin/python3

import time
import sqlite3
import sys
import logging
import os

# Imports with dependencies
import ui


try:
    os.remove("timetable.log")
except:
    pass

# Uncomment if debug log is needed
#logging.basicConfig(filename="timetable.log", level=logging.DEBUG)

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

def delete_table(tablename):
    ui.show("This is where a table will be deleted.")

def worktime():
    start = time.time()
    input("Press enter when finished.\n")
    stop = time.time()
    duration = round(stop - start)
    return (start, stop, duration)

def total_seconds(table):
    seconds = 0
    for row in table:
        seconds += row[2]
    return seconds

def run_worktime(table = None):
    stamp = worktime()
    print("Time spent: ", round(stamp[2]/60, 1), "min\n")
    enter_record(stamp[0], stamp[1], stamp[2], table)

    print("In total ", round(total_seconds(read_table(table))/3600, 2), " hours.")
    time.sleep(3)


def menu():
    # TODO: Menu for managing tables and seeing total time spent in each
    heading = ui.underline("Main menu")
    options = [
        {"key":"l", "text":"List tables", "function":menu_list_tables},
        {"key":"n", "text":"Create new table", "function":menu_new_table}
    ]
    ui.menu(options, heading)

def menu_list_tables():
    tables = list_tables()
    heading = ui.underline("Available timetables")
    options = []
    i = 0

    if tables:
        for table in tables:
            i += 1
            options.append(
                {
                    "key":str(i),
                    "text":table,
                    "function":lambda:menu_table(table)
                }
            )
    options.append(
        {
            "key":"n",
            "text":"New table",
            "function":menu_new_table
        }
    )
#    if ui.menu(options, heading):
#        return 1
    ui.menu(options, heading)

def menu_new_table():
    tablename = input("\nName of new table: ")
    generate_db(table = tablename)
    menu_table(tablename)

def menu_table(tablename):
    heading = ui.underline(tablename)
    table = read_table(tablename)

    info = (
        "Total time spent: {0} hours\n"
    ).format(round(total_seconds(table)/3600, 2))

    options = [
        {
            "key":"s",
            "text":"Spend time on this",
            "function":lambda:this_table(tablename)
        },
        {
            "key":"d",
            "text":"Delete this table",
            "function":lambda:delete_table(tablename)
        }
    ]
    ui.menu(options, heading + info)
    return 1

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

    print("Spending time on", text)
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
