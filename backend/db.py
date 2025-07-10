import sqlite3

conn = sqlite3.connect("database_file")

with sqlite3.connect("database_file") as conn:
    try:
        conn.execute("""
            CREATE TABLE USERS (
                USER_ID INTEGER PRIMARY KEY NOT NULL,
                USER_EMAIL varchar(50),
                USERS_PASSWORD varchar(60)
        )
        """)

    except sqlite3.OperationalError as e:
        print("Failed to open database: ", e)