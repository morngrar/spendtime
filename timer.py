#!/usr/bin/python3

import time
import sqlite3

DATABASE_FILE = "worktime.db"

def generate_db():
    # connecting to the database file
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    # creating a new SQLite table with one column
    c.execute(
        "CREATE TABLE IF NOT EXISTS time"
        "(start REAL PRIMARY KEY, stop REAL, duration INTEGER)"
    )

    # Committing changes and closing the connection to the database
    conn.commit()
    conn.close()

def read_db():
    print("Reading database...")
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    
    dblist = []
    c.execute('SELECT * FROM time')
    data = c.fetchall()
    for row in data:
        dblist.append(row)

    conn.close()
    return dblist
    
def enter_record(start, stop, duration):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    c.execute(
        "INSERT INTO time VALUES (?, ?, ?)",
        (start, stop, duration)
    )

    conn.commit()
    conn.close()
    
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
    for row in read_db():
        #print(row)
        total_seconds += row[2]
        
    print("In total ", round(total_seconds/3600, 2), " hours.")
    time.sleep(3)
    

if __name__ == "__main__":
    main()


    
