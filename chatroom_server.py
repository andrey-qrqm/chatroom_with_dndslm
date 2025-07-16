# Python program to implement server side of chat room.
import socket
import logging
import sys
from dotenv import load_dotenv
import os
import requests
'''Replace "thread" with "_thread" for python 3'''
import threading

# Configure logging
logging.basicConfig(
    filename='chat.log',             # Log file name
    filemode='a',                    # Append mode
    level=logging.INFO,              # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'
)


load_dotenv()
#print("Model_port:", os.getenv("Model_port"))
#print("Model_ip:", os.getenv("Model_ip"))

model_ip = os.getenv("Model_ip")
model_port = os.getenv("Model_port")

if model_ip is None or model_port is None:
    print("Environment variables Model_ip and Port_ip must be set.")
    sys.exit(1)

MAX_TOKENS = 50

logging.info("Script runs")

def get_response(prompt, max_tokens):

    payload = {
        "model": "custom_m",
        "prompt": prompt,
        "stream": False,
        "max_tokens": max_tokens
    }
    OLLAMA_URL = f"http://{model_ip}:{model_port}/generate_ai"
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        logging.info(f"response - {response}")
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        logging.error(f"get response Raised Exception - {e}")
        return f"Error: {e}"


"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# checks whether sufficient arguments have been provided
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()

# takes the first argument from command prompt as IP address
IP_address = str(sys.argv[1])

# takes second argument from command prompt as port number
Port = int(sys.argv[2])

"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind((IP_address, Port))

"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)
server.settimeout(1.0)

logging.info("server set to listen")

list_of_clients = []


def clientthread(conn, addr):
    # sends a message to the client whose user object is conn
    conn.send("Welcome to this chatroom!".encode())
    logging.info(f"Welcome send")
    while True:
        try:
            message = conn.recv(2048).decode()
            logging.info(f"{message} received")

            if message[:3] == "!ai":
                logging.info(f"message {message} STARTS WITH !AI")
                print("<" + addr[0] + "> " + message)
                try:
                    response = get_response(message[3:], MAX_TOKENS)
                    logging.info(f"message {message} responded with {response}")
                    message_to_send = "<" + addr[0] + "> " + response
                    conn.send(message_to_send.encode())
                    broadcast(message_to_send, conn)
                except Exception as e:
                    logging.info(f"CONNECTION REFUSED ERROR: {e}")

            elif message:
                """prints the message and address of the
                user who just sent the message on the server
                terminal"""
                print("<" + addr[0] + "> " + message)

                # Calls broadcast function to send message to all
                message_to_send = "<" + addr[0] + "> " + message
                broadcast(message_to_send, conn)

            else:
                """message may have no content if the connection
                is broken, in this case we remove the connection"""
                remove(conn)
                logging.info(f"{conn} remove")

        except Exception as e:
            logging.error(f"Exception in clientthread: {e}")
            remove(conn)
            break


"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode())
                logging.info(f"{clients} sends message {message}")
            except:
                clients.close()
                logging.info(f"{clients} remove")
                # if the link is broken, we remove the client
                remove(clients)


"""The following function simply removes the object
from the list that was created at the beginning of
the program"""


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
        logging.info(f"{connection} removed")


try:
    while True:
        try:
            """Accepts a connection request and stores two parameters,
            conn which is a socket object for that user, and addr
            which contains the IP address of the client that just
            connected"""
            conn, addr = server.accept()

            """Maintains a list of clients for ease of broadcasting
            a message to all available people in the chatroom"""
            list_of_clients.append(conn)

            # prints the address of the user that just connected
            print(addr[0] + " connected")
            logging.info(f"{addr[0]} connected")

            t = threading.Thread(target=clientthread, args=(conn, addr), daemon=True)
            t.start()
        except socket.timeout:
            continue

except KeyboardInterrupt:
    print("Shutting down server.")
    for c in list_of_clients:
        c.close()
    server.close()
    sys.exit(0)

conn.close()
remove(conn)
logging.info(f"Connection with {addr[0]} closed")