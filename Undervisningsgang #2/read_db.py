#Viser de sidste 20 records i databasen

import sqlite3
conn = sqlite3.connect('minDB.db')
try:
    cur = conn.cursor()
    cur.execute('SELECT * FROM VEJR order by datetime desc Limit 20')

    for row in cur:
        print(f'date = {row[0]}, temp={row[1]}C, humidity={row[2]}%')
except sqlite3.Error as e:
    print(f'Error calling SQL: "{e}"')
finally:
    conn.close() # Close connection to server
