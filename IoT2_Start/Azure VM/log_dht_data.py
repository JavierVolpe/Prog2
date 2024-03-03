# Import necessary libraries
import sqlite3
from datetime import datetime
from time import sleep
import paho.mqtt.subscribe as subscribe

# Define the path to the SQLite database
db_path = "db/sensor_data.db"

def create_table():
    """
    This function creates a new table in the SQLite database if it doesn't already exist.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()

    # Check if the table already exists
    curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stue' LIMIT 1;")
    if curs.fetchone():
        print("Table already exists")
    else:
        # SQL query to create a new table
        query = """CREATE TABLE stue (datetime TEXT, temperature REAL, humidity REAL)"""
        try:
            # Execute the SQL query
            curs.execute(query)
            conn.commit()
            print("Table created successfully")
        except Exception as e:
            print("Error:", e)
            print("Failed to connect to the database")
            conn.rollback()
        finally:
            # Close the cursor
            curs.close()

def log_stue_data(client, userdata, message):
    """
    This function logs the temperature and humidity data to the SQLite database.

    Args:
        client: The MQTT client instance for this callback
        userdata: The private user data as set in Client() or userdata_set()
        message: An instance of MQTTMessage. This is a class with members topic, payload, qos, retain.
    """
    # SQL query to insert data into the 'stue' table
    query = """INSERT INTO stue (datetime, temperature, humidity) VALUES (?, ?, ?)"""

    # Decode the message payload and split it into components
    msg_str = message.payload.decode("utf-8")
    time, temperature, humidity = msg_str.split("|")
    data = (time, temperature, humidity)
    print(f"Data to be inserted: {data}")

    # Connect to the database
    try:
        conn = sqlite3.connect(db_path)
        curs = conn.cursor()
        # Execute the SQL query
        curs.execute(query, data)
        conn.commit()
    except Exception as e:
        print("Error:", e)
        print("Failed to connect to the database")
        conn.rollback()
    finally:
        # Close the cursor
        curs.close()
    sleep(0.5)

def start_logging():
    """
    This function starts the logging process.
    """
    try:
        # Create the table if it doesn't exist
        create_table()
        # Subscribe to the MQTT topic and log the data
        subscribe.callback(log_stue_data, "stue/data", hostname="52.178.210.165")
    except Exception as e:
        print("Error:", e)
    except KeyboardInterrupt:
        print("Program stopped by the user")

# Start the logging process
start_logging()