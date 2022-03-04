import socket
import ssl
import mysql.connector
import select


def main():
    print("Connecting to database server...")
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    print("Connected")
    db_cursor = db.cursor()
    print("Checking if database exists...")
    sql = "SHOW DATABASES LIKE 'App_Database'"
    db_cursor.execute(sql)
    check = db_cursor.fetchall()
    if not check:
        print("Database doesn't exists")
        db_cursor.execute("CREATE DATABASE App_Database")
        print("Database created")
    print("Database exists")
    print("Connecting to database...")
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="App_Database"
    )
    print("Connected")
    db_cursor = db.cursor()
    db_cursor.execute("SHOW TABLES")
    check = db_cursor.fetchall()
    if not check:
        print("No tables in database")
        print("Creating users table")
        sql = "CREATE TABLE users (name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))"
        db_cursor.execute(sql)
        print("Users table created")
    elif ("users",) not in check:
        print("Creating users table")
        sql = "CREATE TABLE users (name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))"
        db_cursor.execute(sql)
        print("Users table created")
    messages_to_send = []
    client_sockets = []
    server_sock = socket.socket()
    server_sock.bind(('0.0.0.0', 8820))
    server_sock.listen()
    while True:
        r_list, w_list, e_list = select.select([server_sock] + client_sockets, client_sockets, [], 0.01)
        for sock in r_list:
            if sock is server_sock:
                connection, client_address = sock.accept()
                client_sockets.append(connection)
                print("Client connected")
            else:
                try:
                    length = sock.recv(3).decode()
                    if length == '':  # sock disconnected
                        client_sockets.remove(sock)
                        sock.close()
                    else:
                        try:
                            data = sock.recv(int(length)).decode()
                            print(data)
                            if "|" in data:  # insert new user into users table
                                t = False
                                split_data = data.split("|")
                                user_name = split_data[0]
                                user_email = split_data[1]
                                user_password = split_data[2]  # later need to encrypt the password
                                db_cursor.execute("SELECT * FROM users")
                                users_info = db_cursor.fetchall()
                                for user in users_info:
                                    if user_email in user:
                                        message = "Email already exists in system"
                                        print(message)
                                        length = str(len(message))
                                        messages_to_send.append((sock, length.zfill(3) + message))
                                        t = True
                                        break
                                if t:
                                    break
                                sql_command = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                                values = (user_name, user_email, user_password)
                                db_cursor.execute(sql_command, values)
                                db.commit()
                                message = "Inserted user"
                                length = str(len(message))
                                messages_to_send.append((sock, length.zfill(3) + message))
                                print(message + " " + user_name)
                        except ValueError:
                            print("Value Error")
                            client_sockets.remove(sock)
                            sock.close()
                except ConnectionResetError:
                    print("Connection Reset Error")
                    client_sockets.remove(sock)
                    sock.close()
        for message in messages_to_send:
            current_socket, data = message
            for sock in client_sockets:
                if sock is current_socket:
                    sock.send(data.encode())
        messages_to_send = []


if __name__ == "__main__":
    main()
