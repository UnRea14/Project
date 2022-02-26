import socket
import ssl
import mysql.connector
import select


def main():
    db = mysql.connector.connect(
        host="",  # change to real host
        user="",  # change to real user
        password="",  # change to real password
        database=""  # change to real database
    )
    db_cursor = db.cursor()
    messages_to_send = []
    client_sockets = []
    server_sock = socket.socket()
    server_sock.bind(('0.0.0.0', 8820))
    server_sock.listen()
    while True:
        rlist, wlist, elist = select.select([server_sock] + client_sockets, client_sockets, [], 0.01)
        for sock in rlist:
            if sock is server_sock:
                connection, client_address = sock.accept()
                client_sockets.append(connection)
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
                                split_data = data.split("|")
                                user_name = split_data[0]
                                user_email = split_data[1]  # later need to encrypt the password
                                user_password = split_data[2]
                                sql_command = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                                values = (user_name, user_email, user_password)
                                db_cursor.execute(sql_command, values)
                                db.commit()
                                print(f"Inserted user {user_name}")
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
