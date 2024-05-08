import socket

print("Connecting")
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    hostname = socket.gethostname()
    print(hostname)
    server_address = ('192.168.1.28', 12345)
    client_socket.connect(server_address)

    welcome_message = client_socket.recv(1024).decode()
    print(welcome_message)

    username = client_socket.recv(1024).decode()
    print(username)
    message = input("Desktop: ")
    client_socket.send(message.encode())

    password = client_socket.recv(1024).decode()
    print(password)
    message = input("Desktop: ")
    client_socket.send(message.encode())

    ID_prompt = client_socket.recv(1024).decode()
    print(ID_prompt)
    client_socket.send(message.encode())

    welcome_message = client_socket.recv(1024).decode()
    print("1",welcome_message)

    welcome_message = client_socket.recv(1024).decode()
    print("2",welcome_message)

    while True:
        message = input("Desktop: ")

        client_socket.send(message.encode())

        if message.lower() == 'quit':
            break

        response = client_socket.recv(1024).decode()
        print(response)
        response = client_socket.recv(1024).decode()
        print(response)
finally:
    client_socket.close()