# db.py

import mysql.connector

try:
    # Connect to MySQL
    connection = mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="1234",      # Replace with your MySQL password
        database="ai_career_guidance"
    )

    # Check if connection is successful
    if connection.is_connected():
        print("✅ Connected to MySQL Successfully!")

        # Create Cursor
        cursor = connection.cursor()

        # Execute SQL Query
        cursor.execute("SELECT DATABASE();")

        # Fetch Result
        database = cursor.fetchone()

        # Display Current Database
        print("Current Database:", database)

        # Close Cursor
        cursor.close()

# Handle Errors
except mysql.connector.Error as err:
    print("❌ Error:", err)

# Close Connection
finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("🔒 MySQL Connection Closed.")