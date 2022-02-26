import socket
import select
import ssl


def main():
    email = "liam14@gmail.com"
    password = "liam1402"
    name = "liam"
    first_time = True
    client_sock = socket.socket()
    try:
        client_sock.connect(("127.0.0.1", 8820))
        print("Connected")
        while True:
            rlist, wlist, elist = select.select([client_sock], [client_sock], [])
            for sock in rlist:
                try:
                    length = sock.recv(3).decode()
                    try:
                        data = sock.recv(int(length)).decode()
                        print(data)
                        if first_time:
                            message = name + "|" + email + "|" + password
                            length = str(len(message))
                            sock.send((length.zfill(3) + message).encode())
                            first_time = False
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
