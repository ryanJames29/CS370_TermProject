import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('10.0.0.148', 12345)
client_socket.connect(server_address)

welcome_message = client_socket.recv(1024).decode()
print(welcome_message)

initial_message = client_socket.recv(1024).decode()
print(initial_message)

while True:
    message = input("Desktop: ")
    
    client_socket.send(message.encode())
    
    if message.lower() == 'quit':
        break
    
    response = client_socket.recv(1024).decode()
    print("Server:", response)

client_socket.close()