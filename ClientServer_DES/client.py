import socket
import threading
from des import *

key = '1234abcd'
bin_key = text_to_binary(key)[0]
round_keys = generateKeys(bin_key)

# Inisialisasi socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect ke server
server_address = ('localhost', 5555)
client_socket.connect(server_address)

# Meminta nama dari client
client_name = input("Insert your name: ")
client_socket.send(client_name.encode('utf-8'))

def receive_messages():
    try:
        while True:
            # Menerima pesan dari server
            data = client_socket.recv(1024)

            print(f"\nReceived messages from {data.decode('utf-8')}")
            
            # Dekripsi pesan sebelum menampilkan
            decrypted_message = decrypt_message(data.decode('utf-8').split(': ')[1], round_keys)
        
            print(f"Decrypted messages: {decrypted_message}")
    except:
        # Jika ada error, tutup koneksi
        client_socket.close()

# Memulai thread untuk menerima pesan
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Function to encrypt a message
def encrypt_message(message, round_keys):
    # Padding the message to make its length a multiple of 8
    while len(message) % 8 != 0:
        message += ' '

    encrypted_message = ""
    for i in range(0, len(message), 8):
        chunk = message[i:i+8]
        bin_chunk = text_to_binary(chunk)
        encrypted_chunk = ""
        for sub_chunk in bin_chunk:
            result = encrypt(sub_chunk, round_keys)
            encrypted_chunk += result
        encrypted_message += binary_to_text(encrypted_chunk)
    return encrypted_message

# Function to decrypt a message
def decrypt_message(encrypted_message, round_keys):
    decrypted_message = ""
    for i in range(0, len(encrypted_message), 8):
        chunk = encrypted_message[i:i+8]
        bin_chunk = text_to_binary(chunk)
        decrypted_chunk = ""
        for sub_chunk in bin_chunk:
            result = decrypt(sub_chunk, round_keys)
            decrypted_chunk += result
        decrypted_message += binary_to_text(decrypted_chunk)
    return decrypted_message

# Mengirim pesan ke server
try:
    while True:
        message = input("Enter your messages: ")
        # Enkripsi pesan sebelum mengirim ke server
        encrypted_message = encrypt_message(message, round_keys)
        client_socket.send(encrypted_message.encode('utf-8'))
        print(f"Your messages has been sent!")
except:
    # Jika ada error, tutup koneksi
    client_socket.close()