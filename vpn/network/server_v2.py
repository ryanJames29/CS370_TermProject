import socket
import threading

def multipleClients(client_socket, addr):
    print(f"Connection from {addr}\n")

    client_socket.send("Welcome to the server, ran by Raspberry Pi 5!".encode())

    client_socket.send("Ready to receive messages".encode())

    with open('/home/ryanjames/Desktop/vpn/clientFiles/list.txt', 'r') as file:
        file_content = file.read()
    client_socket.send(file_content.encode())

    try:
        while True:
            #Message from the client
            message = client_socket.recv(1024).decode()
            print("Desktop:", message)

            if message.lower() == 'planets':
                with open('/home/ryanjames/Desktop/vpn/clientFiles/planets.txt', 'r') as file:
                    file_content = file.read()
                client_socket.send(file_content.encode())
            elif message.lower() == 'helloWorld':
                with open('/home/ryanjames/Desktop/vpn/clientFiles/helloWorld.py', 'r') as file:
                    file_content = file.read()
                client_socket.send(file_content.encode())
            elif message.lower() == 'homepage':
                with open('/home/ryanjames/Desktop/vpn/clientFiles/Homepage.txt', 'r') as file:
                    file_content = file.read()
                client_socket.send(file_content.encode())
            elif message.lower() == 'project':
                with open('/home/ryanjames/Desktop/vpn/clientFiles/Project.txt', 'r') as file:
                    file_content = file.read()
                client_socket.send(file_content.encode())
            elif message.lower() == 'list':
                with open('/home/ryanjames/Desktop/vpn/clientFiles/list.txt', 'r') as file:
                    file_content = file.read()
                client_socket.send(file_content.encode())
            elif message.lower() == 'quit':
                break
            else:
                client_socket.send("Need anything else? (quit to exit)".encode())
    except Exception as e:
        print("Error:", e)
    finally:
        #close the client connection
        client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '0.0.0.0'
port = 12345
server_socket.bind((host, port))

server_socket.listen(5)
print("Raspberry Pi is waiting for incoming connections...")

while True:
    #accept client connection
    client_socket, addr = server_socket.accept()

    client_thread = threading.Thread(target=multipleClients, args=(client_socket, addr))
    client_thread.start()