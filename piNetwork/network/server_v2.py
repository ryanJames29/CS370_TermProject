import socket
import threading
from gpiozero import LED
from time import sleep

red_LED = LED(26)
yellow_LED = LED(20)
green_LED = LED(6)

red_LED.on()

numClients = []

def multipleClients(client_socket, addr):
    print(f"Connection from {addr}\n")

    username1 = 'Desktop1'
    username2 = 'Desktop2'
    password1 = 'CS370'
    password2 = 'CS370'

    client_socket.send("Welcome to the server, ran by Raspberry Pi 5!\n".encode())

    client_socket.send("Username: ".encode())
    username_attempt = client_socket.recv(1024).decode().strip()

    # Prompt for password
    client_socket.send("Password: ".encode())
    password_attempt = client_socket.recv(1024).decode().strip()

    # Check username and password
    if (username_attempt == username1 and password_attempt == password1) or \
    (username_attempt == username2 and password_attempt == password2):
        numClients.append(addr) 
        size = len(numClients)
        if size == 1:
            red_LED.off()
            yellow_LED.on()
        elif size == 2:
            red_LED.off()
            yellow_LED.off()
            green_LED.on()
        client_socket.send("Login successful!\n".encode())
        # Proceed with further actions after successful login
        with open('/home/ryanjames/Desktop/CS370_TermProject/piNetwork/serverFiles/list.txt', 'r') as file:
            file_content = file.read()
        client_socket.send(file_content.encode())

        try:
            while True:
                #Message from the client
                message = client_socket.recv(1024).decode()
                print("Desktop:", message)

                if message.lower() == 'planets':
                    with open('/home/ryanjames/Desktop/CS370_TermProject/piNetwork/serverFiles/planets.txt', 'r') as file:
                        file_content = file.read()
                    client_socket.send(file_content.encode())
                elif message.lower() == 'helloWorld':
                    with open('/home/ryanjames/Desktop/CS370_TermProject/piNetwork/serverFiles/helloWorld.py', 'r') as file:
                        file_content = file.read()
                    client_socket.send(file_content.encode())
                elif message.lower() == 'homepage':
                    with open('/home/ryanjames/Desktop/CS370_TermProject/piNetwork/serverFiles/Homepage.txt', 'r') as file:
                        file_content = file.read()
                    client_socket.send(file_content.encode())
                elif message.lower() == 'project':
                    with open('/home/ryanjames/Desktop/CS370_TermProject/piNetwork/serverFiles/Project.txt', 'r') as file:
                        file_content = file.read()
                    client_socket.send(file_content.encode())
                elif message.lower() == 'list':
                    with open('/home/ryanjames/Desktop/CS370_TermProject/piNetwork/serverFiles/list.txt', 'r') as file:
                        file_content = file.read()
                    client_socket.send(file_content.encode())
                elif message.lower() == 'quit':
                    yellow_LED.off()
                    green_LED.off()
                    red_LED.on()
                    break
                else:
                    client_socket.send("Need anything else? (quit to exit)".encode())
        except Exception as e:
            print("Error:", e)
        finally:
            #close the client connection
            client_socket.close()
    else:
        client_socket.send("Invalid username or password!\n".encode())
        # Close connection or take appropriate action for failed login

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
