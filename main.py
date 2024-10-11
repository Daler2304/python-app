import socket
import threading

# Список для хранения подключенных клиентов
online = []

# Словарь для хранения подключенных клиентов по user_id
clients = {}

def handle_client(client_socket, addr):
    print(f'Подключено к {addr}')

    # Используем номер порта как user_id
    user_id = addr[1]

    if user_id in online:
        print(f'Пользователь {user_id} уже онлайн.')
    else:
        online.append(user_id)

    # Сохраняем сокет клиента в словаре
    clients[user_id] = client_socket

    connected_client = None  # Идентификатор подключенного клиента

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break  # Клиент отключился

            if message.startswith('/connect'):
                # Обработка команды /connect
                _, target_user_id = message.split()
                target_user_id = int(target_user_id)

                if target_user_id in clients:
                    connected_client = target_user_id
                    client_socket.send(f'Вы подключены к пользователю {target_user_id}.'.encode('utf-8'))
                else:
                    client_socket.send(f'Пользователь {target_user_id} не найден.'.encode('utf-8'))

            elif connected_client is not None:
                # Если пользователь подключен, отправляем сообщение ему
                target_socket = clients[connected_client]
                target_socket.send(f'Сообщение от {user_id}: {message}'.encode('utf-8'))
            else:
                client_socket.send('Сначала выполните /connect <user_id>'.encode('utf-8'))

    except Exception as e:
        print(f'Ошибка при обработке клиента {addr}: {e}')

    finally:
        # Закрываем соединение и удаляем пользователя из списка и словаря
        client_socket.close()
        print(f'Connection with {addr} closed!')
        online.remove(user_id)
        del clients[user_id]

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Получаем порт из переменной окружения или используем 3000 по умолчанию
    PORT = int(os.getenv('PORT', 3000))
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(5)
    print(f'Сервер запущен на порту {PORT}. Ожидание подключения...')

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == '__main__':
    start_server()
