import socket
import ssl
import select
import db_handler


def insert_user(user_name, user_email, user_password, sock, messages_to_send, db_handler1):
    t = False
    db_handler1.db_cursor.execute("SELECT * FROM users")
    users_info = db_handler1.db_cursor.fetchall()
    for user in users_info:
        if user_email in user:
            message = "Email already exists in system"
            print(message)
            length = str(len(message))
            messages_to_send.append((sock, length.zfill(3) + message))
            t = True
            break
    sql_command = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    values = (user_name, user_email, user_password)
    db_handler1.db_cursor.execute(sql_command, values)
    db_handler1.db_connector.commit()
    message = "Inserted user"
    length = str(len(message))
    messages_to_send.append((sock, length.zfill(3) + message))
    print(message + " " + user_name)
    return t


def main():
    db_handler1 = db_handler.DbHandler()
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
                                split_data = data.split("|")
                                user_name = split_data[0]
                                user_email = split_data[1]
                                user_password = split_data[2]  # later need to encrypt the password
                                t = insert_user(user_name, user_email, user_password, sock, messages_to_send, db_handler1)
                                if t:
                                    break
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
