import socket
import ssl
import select


def main():
    messages_to_send = []
    client_sockets = []
    server_sock = socket.socket()
    server_sock.bind(('0.0.0.0', 8820))
    server_sock.listen()
    while True:
        rlist, wlist, elist = select.select([server_sock] + client_sockets, client_sockets, [], 0.01)
        for sock in rlist:
            if sock is server_sock:
                connection, client_addr = sock.accept()
                client_sockets.append(connection)
                message = "005Hello"
                messages_to_send.append((connection, message))

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
                            if data == "upload file":
                                message = "002ok"
                                messages_to_send.append((sock, message))

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
