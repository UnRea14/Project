import socket
import select
import ssl


def main():
    email = "liam14@gmail.com"
    password = "liam1402"
    name = "liam"
    client_sock = socket.socket()
    try:
        print("Connecting to server...")
        client_sock.connect(("127.0.0.1", 8820))
        print("Connected")
        message = name + "|" + email + "|" + password
        length = str(len(message))
        client_sock.send((length.zfill(3) + message).encode())
        while True:
            r_list, w_list, e_list = select.select([client_sock], [], [])
            for sock in r_list:
                print(sock)
                try:
                    length = sock.recv(3).decode()
                    try:
                        data = sock.recv(int(length)).decode()
                        print(data)
                    except ValueError:
                        print("Value Error")
                        quit()
                except ConnectionResetError:
                    print("Connection Reset Error")
                    quit()
    except ConnectionError:
        print("Connection Error - Server offline")
        quit()


if __name__ == "__main__":
    main()
