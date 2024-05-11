#Завдання1

import socket
import threading
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'
    port = 12345
    client_socket.connect((host, port))

    print("Ви приєдналися до гри 'Хрестики — нулики'.")

    while True:
        response = client_socket.recv(1024).decode()
        print(response)
        if "починається" in response:
            confirmation = input("Підтверджуєте початок гри? (yes/no): ")
            client_socket.send(confirmation.encode())
            if confirmation.lower() == 'yes':
                break

    while True:
        response = client_socket.recv(1024).decode()
        print(response)
        if "переміг" in response or "закінчилась" in response:
            break
        if "Ваш хід" in response:
            move = input("Введіть номер клітинки (0-8): ")
            client_socket.send(move.encode())

    client_socket.close()


#Завдання 2
def send_file(filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'
    port = 12345
    client_socket.connect((host, port))

    client_socket.send(filename.encode())

    confirmation = client_socket.recv(1024).decode()
    if confirmation.lower() == 'yes':
        with open(filename, 'rb') as file:
            for data in file:
                client_socket.send(data)
        print(f"Файл {filename} успішно надіслано.")
    else:
        print("Відмовлено в надсиланні файлу.")

    client_socket.close()


filename = input("Введіть назву файлу для надсилання: ")
send_file(filename)

#Завдання 3

class ChatClient:
    def __init__(self):
        self.host = 'localhost'
        self.port = 12345
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.client_socket.connect((self.host, self.port))

        login = input("Введіть свій логін: ")
        self.client_socket.send(login.encode())

        password = input("Введіть пароль: ")
        self.client_socket.send(password.encode())

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        while True:
            message = input()
            self.client_socket.send(message.encode())

    def receive(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                print(message)
            except:
                break


chat_client = ChatClient()
chat_client.start()

