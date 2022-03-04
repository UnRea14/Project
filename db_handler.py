import mysql.connector


class DbHandler:
    def __init__(self):
        print("Connecting to database server...")
        db_connector = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        print("Connected")
        self.db_cursor = db_connector.cursor()
        print("Checking if database exists...")
        sql = "SHOW DATABASES LIKE 'App_Database'"
        self.db_cursor.execute(sql)
        check = self.db_cursor.fetchall()
        if not check:
            print("Database doesn't exists")
            self.db_cursor.execute("CREATE DATABASE App_Database")
            print("Database created")
        print("Database exists")
        print("Connecting to database...")
        self.db_connector = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="App_Database"
        )
        print("Connected")
        self.db_cursor = self.db_connector.cursor()
        self.db_cursor.execute("SHOW TABLES")
        check = self.db_cursor.fetchall()
        if not check:
            print("No tables in database")
            print("Creating users table")
            sql = "CREATE TABLE users (name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))"
            self.db_cursor.execute(sql)
            print("Users table created")
        elif ("users",) not in check:
            print("Creating users table")
            sql = "CREATE TABLE users (name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))"
            self.db_cursor.execute(sql)
            print("Users table created")

