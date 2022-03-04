import socket
import select
import ssl


def send_user_info(name, email, password, client_sock):
    message = name + "|" + email + "|" + password
    length = str(len(message))
    client_sock.send((length.zfill(3) + message).encode())


def main():
    email = "liam142@gmail.com"
    password = "liam1402"
    name = "liam"
    client_sock = socket.socket()
    try:
        print("Connecting to server...")
        client_sock.connect(("127.0.0.1", 8820))
        print("Connected")
        send_user_info(name, email, password, client_sock)
        while True:
            r_list, w_list, e_list = select.select([client_sock], [], [])
            for sock in r_list:
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
