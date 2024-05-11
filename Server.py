# Завдання 1
# Реалізуйте клієнт-серверний додаток, що дозволяє двом
# користувачам грати в гру «Хрестики — нулики». Один із
# гравців ініціює гру. Якщо другий гравець підтверджує, то
# гра починається. Гру можна припинити. Той хто припинив
# гру — програв. Після завершення гри можна ініціювати повторний матч.

import socket
import threading
def play_game(conn1, conn2):
    board = [' ' for _ in range(9)]
    current_player = 'X'

    conn1.send(b"Гра починається! Ви граєте 'X'. Очікування гравця 2...")
    conn2.send(b"Гра починається! Ви граєте 'O'. Підтвердження для початку гри.")

    confirmation = conn2.recv(1024).decode()
    if confirmation.lower() == 'yes':
        conn1.send(b"Гра починається!")
        conn2.send(b"Гра починається!")
        send_board_to_players(conn1, conn2, board)
        while True:
            move1 = int(conn1.recv(1024).decode())
            make_move(move1, 'X', conn1, conn2, board)
            if is_game_over(board):
                break

            move2 = int(conn2.recv(1024).decode())
            make_move(move2, 'O', conn1, conn2, board)
            if is_game_over(board):
                break

def make_move(position, symbol, conn1, conn2, board):
    if board[position] == ' ':
        board[position] = symbol
        current_player = 'X' if symbol == 'O' else 'O'
        send_board_to_players(conn1, conn2, board)

def send_board_to_players(conn1, conn2, board):
    board_str = '|'.join(board[:3]) + '\n' + '|'.join(board[3:6]) + '\n' + '|'.join(board[6:])
    conn1.send(board_str.encode())
    conn2.send(board_str.encode())

def is_game_over(board):
    # Перевіряємо на перемогу, нічию або продовження гри
    return (board[0] == board[1] == board[2] != ' ' or
            board[3] == board[4] == board[5] != ' ' or
            board[6] == board[7] == board[8] != ' ' or
            board[0] == board[3] == board[6] != ' ' or
            board[1] == board[4] == board[7] != ' ' or
            board[2] == board[5] == board[8] != ' ' or
            board[0] == board[4] == board[8] != ' ' or
            board[2] == board[4] == board[6] != ' ' or
            ' ' not in board)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(2)

    print("Сервер запущено. Очікування гравців...")

    while True:
        conn1, addr1 = server_socket.accept()
        print("Гравець 1 приєднався:", addr1)
        conn2, addr2 = server_socket.accept()
        print("Гравець 2 приєднався:", addr2)

        play_game(conn1, conn2)

        conn1.close()
        conn2.close()

if __name__ == "__main__":
    main()
#
# Завдання 2
# Реалізуйте клієнт-серверний додаток з можливістю надсилати файли.
# Один користувач ініціює надсилання файлу, другий
# підтверджує. Після підтвердження починається надсилання.
# Якщо відправка була вдалою, повідомте про це відправника.


def receive_file(conn, filename):
    with open(filename, 'wb') as file:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            file.write(data)
    print(f"Файл {filename} успішно отримано.")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Сервер запущено. Очікування клієнта...")

    while True:
        conn, addr = server_socket.accept()
        print("Клієнт приєднався:", addr)

        filename = conn.recv(1024).decode()
        print("Клієнт надіслав запит на отримання файлу:", filename)

        confirmation = input("Чи підтверджуєте надсилання файлу? (yes/no): ")
        conn.send(confirmation.encode())

        if confirmation.lower() == 'yes':
            receive_file(conn, filename)

        conn.close()

if __name__ == "__main__":
    main()
# Завдання 3
# Реалізуйте клієнт-серверний додаток , який дозволяє
# користувачам спілкуватися в одному чаті. Кожен користувач
# входить у чат під своїм логіном та паролем. Повідомлення,
# надіслане в чат, видно всім користувачам чату.




class ChatServer:
    def __init__(self):
        self.host = 'localhost'
        self.port = 12345
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Сервер запущено. Очікування клієнтів...")

        while True:
            conn, addr = self.server_socket.accept()
            print("Клієнт приєднався:", addr)
            threading.Thread(target=self.handle_client, args=(conn,)).start()

    def handle_client(self, conn):
        conn.send("Ласкаво просимо! Введіть свій логін:".encode())
        login = conn.recv(1024).decode()
        conn.send("Введіть пароль:".encode())
        password = conn.recv(1024).decode()

        self.clients[login] = conn
        print(f"Клієнт {login} приєднався до чату.")

        while True:
            try:
                message = conn.recv(1024).decode()
                if not message:
                    break
                print(f"{login}: {message}")
                self.broadcast(message, login)
            except:
                break

        print(f"Клієнт {login} вийшов з чату.")
        del self.clients[login]
        conn.close()

    def broadcast(self, message, sender):
        for login, client_conn in self.clients.items():
            if login != sender:
                try:
                    client_conn.send(f"{sender}: {message}".encode())
                except:
                    del self.clients[login]
                    client_conn.close()

chat_server = ChatServer()
chat_server.start()
