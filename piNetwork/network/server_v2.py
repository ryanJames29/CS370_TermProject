import socket
import threading
import os
import time
# import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522
from gpiozero import LED
from time import sleep

red_LED = LED(26)
yellow_LED = LED(20)
green_LED = LED(6)

red_LED.on()
# (Username, Password) : physical id
users = {('Desktop1', 'CS370'): 596170611542,
         ('Desktop2', 'CS370'): 584195496087}

numClients = []

def check_credentials(username_attempt, password_attempt):
    if (username_attempt, password_attempt) in users:
        #return check_id_card((username_attempt, password_attempt))
        return True
    return False


# def check_id_card(usercredentials):
#     reader = SimpleMFRC522()
#     try:
#         print("Please scan ID")
#         uid = reader.read_id()
#         if (users.get(usercredentials) == uid):
#             print("ID approved")
#             return True
#         else:
#             print("Incorrect ID scanned")
#             return False
#     finally:
#         GPIO.cleanup()


def set_light(size):
    if size == 0:
        red_LED.on()
        green_LED.off()
        yellow_LED.off()
    elif size == 1:
        red_LED.off()
        green_LED.off()
        yellow_LED.on()
    else:
        red_LED.off()
        yellow_LED.off()
        green_LED.on()


def send_message(filename):
    base = '/home/ryanjames/Desktop/CS370_TermProject/piNetwork/serverFiles/'
    file_path = file_path = os.path.join(base, filename)
    with open(file_path, 'r') as file:
        file_content = file.read()
    client_socket.send(file_content.encode())


def multipleClients(client_socket, addr):
    print(f"Connection from {addr}\n")

    client_socket.send("Welcome to the server, ran by Raspberry Pi 5!\n".encode())

    client_socket.send("Username: ".encode())
    username_attempt = client_socket.recv(1024).decode().strip()

    # Prompt for password
    client_socket.send("Password: ".encode())
    password_attempt = client_socket.recv(1024).decode().strip()

    if check_credentials(username_attempt, password_attempt):
        numClients.append(addr)
        set_light(len(numClients))

        client_socket.send("Login successful!\n".encode())
        # Proceed with further actions after successful login
        send_message('list.txt')

        try:
            while True:
                # Message from the client
                message = client_socket.recv(1024).decode()
                print("[Desktop]:", message)

                if message.lower() == 'planets':
                    send_message('planets.txt')
                elif message.lower() == 'helloWorld':
                    send_message('helloWorld.txt')
                elif message.lower() == 'homepage':
                    send_message('homepage.txt')
                elif message.lower() == 'project':
                    send_message('project.txt')
                elif message.lower() == 'quit':
                    break
                else:
                    send_message('list.txt')

                client_socket.send("Need anything else? (quit to exit)".encode())
        except Exception as e:
            print("Error:", e)
        finally:
            numClients.remove(addr)
            set_light(len(numClients))
            client_socket.close()
    else:
        client_socket.send("Invalid username or password!\n".encode())

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '0.0.0.0'
port = 12345
server_socket.bind((host, port))

server_socket.listen(5)
print("Raspberry Pi is waiting for incoming connections...")

while True:
    # accept client connection
    client_socket, addr = server_socket.accept()

    client_thread = threading.Thread(target=multipleClients, args=(client_socket, addr))
    client_thread.start()

