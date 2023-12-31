import socket
import threading

# Permutation Compression 1: Ignore parity bit (8th bit), result 56 bit
pc1 = [
    57, 49, 41, 33, 25, 17, 9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4
]

# Permutation Compression 2: Compression of key from 56 bits to 48 bits
pc2 = [
    14, 17, 11, 24,  1,  5,
     3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Number of bit shifts for each round
shift_round = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Initial Permutation Table
initial_perm = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17,  9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Expansion Permuation Table
exp_perm = [
    32,  1,  2,  3,  4,  5, 4, 5,
    6,  7,  8,  9,  8,  9, 10, 11,
    12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21,
    22, 23, 24, 25, 24, 25, 26, 27,
    28, 29, 28, 29, 30, 31, 32, 1
]

# S-box Permutation Table
sbox_perm = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],

    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],

    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],

    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],

    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],

    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],

    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],

    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

# P-box Permutation Table
pbox_perm = [
    16, 7, 20, 21, 29, 12, 28, 17,  1, 15, 23, 26,  5, 18, 31, 10,
     2, 8, 24, 14, 32, 27,  3,  9, 19, 13, 30,  6, 22, 11,  4, 25
]

# Final Permutation Table
inverse_initial_perm = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41,  9, 49, 17, 57, 25
]

def text_to_binary(text):
    binary_result = ""
    for char in text:
        binary_char = bin(ord(char))[2:].zfill(8)
        binary_result += binary_char

    return [binary_result[i:i+64] for i in range(0, len(binary_result), 64)]

def binary_to_text(binary_list):
    binary_str = ''.join(binary_list)
    text = ""
    for i in range(0, len(binary_str), 8):
        char_binary = binary_str[i:i+8]
        char = chr(int(char_binary, 2))
        text += char
    return text

def binary_to_hex(binary_str):
    # Convert decimal to hexadecimal
    hexadecimal_number = format(int(binary_str, 2), 'X')

    return hexadecimal_number

def permute(source, table):
    result = ""
    for i in table:
        result += source[i - 1]
    return result

def left_shift_binary(binary_str, n):
    return binary_str[n:] + binary_str[:n]

def binary_xor(bin_str1, bin_str2):
    # Ensure both binary strings have the same length
    max_len = max(len(bin_str1), len(bin_str2))
    bin_str1 = bin_str1.zfill(max_len)
    bin_str2 = bin_str2.zfill(max_len)

    result = ''
    for i in range(max_len):
        if bin_str1[i] == bin_str2[i]:
            result += '0'
        else:
            result += '1'

    return result

def decimal_to_binary(decimal):
    if decimal == 0:
        return "0000"

    binary_str = ""
    while decimal > 0:
        binary_str = str(decimal % 2) + binary_str
        decimal //= 2

    while len(binary_str) < 4:
        binary_str = '0' + binary_str

    return binary_str

def generateKeys(key):
    round_keys = []

    # 64 bits to 56 bits
    pc1_key = permute(key, pc1)

    left = pc1_key[0:28]
    right = pc1_key[28:56]

    for i in range(0, 8):
        left = left_shift_binary(left, shift_round[i])
        right = left_shift_binary(right, shift_round[i])

        # 56 bits to 48 bits
        round_key = permute(left + right, pc2)

        round_keys.append(round_key)

    return round_keys

def encrypt(plaintext, round_keys):
    # initial permutation
    ip_plaintext = permute(plaintext, initial_perm)
    left = ip_plaintext[0:32]
    right = ip_plaintext[32:64]
    for i in range(0, 8):
        #print("Round Key: ", i + 1, " = ", binary_to_hex(left), " ; ", binary_to_hex(right), " ; " , binary_to_hex(round_keys[i]))
        # right 32 bit to 48 bit
        right_expanded = permute(right, exp_perm)

        right_xored = binary_xor(right_expanded, round_keys[i])

        # back from right 48 bit to 32 bit
        right_sboxed = ""
        for j in range(0, 48, 6):
            chunk = right_xored[j:j + 6]
            row = int(chunk[0] + chunk[5], 2)
            col = int(chunk[1:5], 2)

            # Get the value from the S-Box
            right_sboxed += decimal_to_binary(sbox_perm[j//6][row][col])

        right_pboxed = permute(right_sboxed, pbox_perm)
        right_result = binary_xor(left, right_pboxed)

        left = right
        right = right_result

    cipher_text = permute((right + left), inverse_initial_perm)
    return cipher_text

def decrypt(ciphertext, round_keys):
    rev_round_keys = round_keys[::-1]
    return encrypt(ciphertext, rev_round_keys)

key = '1234abcd'
bin_key = text_to_binary(key)[0]
round_keys = generateKeys(bin_key)

# Inisialisasi socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect ke server
server_address = ('10.44.1.2', 5555)
client_socket.connect(server_address)

# Meminta nama dari client
client_name = input("Insert your name: ")
client_socket.send(client_name.encode('utf-8'))

def receive_messages():
    try:
        while True:
            # Menerima pesan dari server
            data = client_socket.recv(1024)

            if not data:
                print("\nServer closed the connection.")
                break

            received_message = data.decode('utf-8')
            if received_message == "Client closing":
                print("\nServer closed the connection.")
                break

            print(f"\nReceived messages from {received_message}")

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

except KeyboardInterrupt:
    print("\nClosing client...")
    # Kirim pesan khusus ke server sebelum menutup koneksi
    try:
        client_socket.send("Client closing".encode('utf-8'))
        client_socket.close()
    except:
        pass
