# Description: This script subscribes to the MQTT broker and logs the temperature and humidity data to a SQLite database


import sqlite3
from datetime import datetime
from time import sleep

import paho.mqtt.subscribe as subscribe

db_path = "db/sensor_data.db"


def create_table():
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()

    # Check if the table already exists
    curs.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='stue' LIMIT 1;"
    )
    if curs.fetchone():
        print("Table already exists")
    else:
        query = """CREATE TABLE stue (datetime TEXT, temperature REAL, humidity REAL)"""
        try:
            curs.execute(query)
            conn.commit()
            print("Table created successfully")
        except Exception as e:
            print("Error:", e)
            print("Failed to connect to the database")
            conn.rollback()
        finally:
            curs.close()


def log_stue_data(client, userdata, message):

    query = """INSERT INTO stue (datetime, temperature, humidity) VALUES (?, ?, ?)"""
 
    # Example of payload: b'2024-03-02 16:52:54|22.0|41.0' 
    msg_str = message.payload.decode("utf-8")

    time = msg_str.split("|")[0]
    temperature = msg_str.split("|")[1]
    humidity = msg_str.split("|")[2]
    data = (time, temperature, humidity)
    print(f"Data to be inserted: {data}")

    # Connect to the database
    try:
        conn = sqlite3.connect(db_path)
        curs = conn.cursor()
        curs.execute(query, data)
        conn.commit()
        # print(f"Data inserted successfully: {data}")
    except Exception as e:
        print("Error:", e)
        print("Failed to connect to the database")
        conn.rollback()
        # conn.close()
    finally:
        curs.close()
    sleep(0.5)

def start_logging():
    try:
        create_table()
        subscribe.callback(log_stue_data, "stue/data", hostname="52.178.210.165")


    except Exception as e:
        print("Error:", e)

    except KeyboardInterrupt:
        print("Program stopped by the user")



start_logging()