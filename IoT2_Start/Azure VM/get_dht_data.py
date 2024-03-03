#   This file contains the function to get the latest data from the DHT sensor
#   in the living room. The data is stored in a SQLite database.
#   The function returns the datetime, temperature and humidity of the latest
#   data. The number of rows to be returned can be specified as an argument to
#   the function. The default number of rows is 10.
#   The function is used in the Flask app to display the latest data on the
#   web page.

import sqlite3
from datetime import datetime

import sqlite3


db_path = 'db/sensor_data.db'

def get_stue_data(number_of_rows=10):
    """
    This function retrieves the latest sensor data from the 'stue' table in the database.

    Args:
        number_of_rows (int): The number of rows to fetch from the database. Default is 10.

    Returns:
        datetime (list): A list of datetime values.
        temperature (list): A list of temperature values.
        humidity (list): A list of humidity values.
    """

    # SQL query to fetch data from the 'stue' table
    query = "SELECT * FROM stue ORDER BY datetime DESC;"

    # Initialize lists to store the data
    datetime = []
    temperature = []
    humidity = []

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        curs = conn.cursor()

        # Execute the SQL query
        curs.execute(query)

        # Fetch the specified number of rows
        rows = curs.fetchmany(number_of_rows)

        # Iterate over the rows and append the data to the lists
        for row in rows:
            datetime.append(row[0])
            temperature.append(row[1])
            humidity.append(row[2])

        # Return the lists of data
        return datetime, temperature, humidity

    except Exception as e:
        # Print any errors that occur
        print('Error:', e)
        print('Failed to connect to the database')

        # Rollback any changes if an error occurs
        conn.rollback()

    finally:
        # Close the cursor
        curs.close()