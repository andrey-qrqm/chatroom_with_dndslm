import socket
import sys
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(2048).decode()
            if message:
                print(message)
            else:
                print("\nDisconnected from server.")
                sock.close()
                break
        except:
            break

def send_messages(sock):
    while True:
        try:
            message = input()
            sock.send(message.encode())
        except:
            break

if len(sys.argv) != 3:
    print("Usage: python script.py <IP> <PORT>")
    sys.exit()

IP_address = sys.argv[1]
Port = int(sys.argv[2])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((IP_address, Port))

# Start threads for sending and receiving
threading.Thread(target=receive_messages, args=(server,), daemon=True).start()
send_messages(server)

server.close()
