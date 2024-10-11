import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            response = client_socket.recv(1024).decode('utf-8')
            if response:
                print(response)
            else:
                break
        except Exception as e:
            print(e)
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('89.111.155.205', 2304))

    user_id = client_socket.getsockname()[1]
    print(f'Ваш ID: {user_id}')
    print('Чтобы подключиться к другому пользователю, используйте команду /connect <user_id>.')

    # Запускаем поток для получения сообщений
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        message = input('Введите сообщение: ')
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode('utf-8'))

    client_socket.close()
    print("Соединение закрыто.")

if __name__ == "__main__":
    start_client()
