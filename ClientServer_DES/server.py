import socket
import threading
import signal

# Inisialisasi socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind address dan port
server_address = ('10.44.1.2', 5555)
server_socket.bind(server_address)

# Listen for incoming connections (maksimal 5 koneksi)
server_socket.listen(5)

# Daftar client yang terhubung
clients = {}

def forward_message(message, sender_socket):
    for client, client_socket in clients.items():
        if client_socket != sender_socket:
            try:

                client_socket.send(message)
            except:
                # Jika ada error, hapus client yang terputus
                del clients[client]
                print(f"Connection with {client} closed.")
                client_socket.close()

def handle_client(client_socket, client_name):
    try:
        while True:
            # Menerima pesan dari client
            data = client_socket.recv(1024)
            if not data:
                break

            if data.decode('utf-8') == "Client closing":
                print(f"Connection with {client_name} closed.")
                del clients[client_name]
                client_socket.close()
                break

            # Broadcast pesan ke semua client
            message = f"{client_name}: {data.decode('utf-8')}"
            # print(message)

            # Forward pesan ke semua client
            forward_message(message.encode('utf-8'), client_socket)

    except ConnectionError:
        # Jika koneksi terputus oleh client
        del clients[client_name]
        print(f"Connection with {client_name} closed.")
        client_socket.close()

    except Exception as e:
        print(f"An error occurred with client {client_name}: {str(e)}")
        del clients[client_name]
        client_socket.close()

def signal_handler(sig, frame):
    print("\nServer shutting down...")
    for client_socket in clients.values():
        client_socket.close()
    server_socket.close()
    exit()

# Menambahkan penanganan sinyal interrupt (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Menampilkan pesan saat server berhasil terhubung
print("Server started and listening for connections.")

while True:
    # Menunggu koneksi dari client
    client_socket, addr = server_socket.accept()

    # Meminta nama dari client
    client_name = client_socket.recv(1024).decode('utf-8')

    # Menambahkan client ke daftar
    clients[client_name] = client_socket

    # Menampilkan pesan saat client berhasil terhubung
    print(f"Client {client_name} connected.")

    # Menangani setiap koneksi dalam thread terpisah
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_name))
    client_handler.start()
