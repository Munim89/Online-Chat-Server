from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

# Global constants
HOST = ""
PORT = 5500
BUFSIZ = 512
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10

# Global Variables
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)  # to setup the SERVER


def broadcast(msg, name):
    """
    send new messages to all clients
    :param msg: bytes["utf8"]
    :param name: str
    :return:
    """
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name, "utf8") + msg)
        except Exception as e:
            print("[FAILURE]: ", e)


def client_communication(person):
    """
    Thread to handle all messages from client
    :param person:Person
    :return:None
    """
    client = person.client

    # first message broadcasted is always the persons name
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)

    msg = bytes(f"{name} has joined the chat!", "utf8")
    broadcast(msg, "")  # to broadcast welcome message

    while True:
        try:
            msg = client.recv(BUFSIZ)

            if msg == bytes("{quit}", "utf8"):
                client.close()
                persons.remove(person)
                broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
                print(f"[DISCONNECTED] {name} has disconnected...")
                break
            else: # else send message to all other clients
                broadcast(msg, name + ": ")
                print(f"{name}: ", msg.decode("utf8"))

        except Exception as e:
            print("[FAILURE]: " + str(e))
            break


def wait_for_connection():
    """
    Wait for connection from new client, start new thread when connected
    :return:None
    """
    run = True
    while run: # wait for new connections
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)  # to create a new person at a new connection
            persons.append(person)

            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[FAILURE]: ", e)
            run = False

    print("SERVER CRASHED")


# To start a new Thread
if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)  # open server to listen for maximum connections
    print("[STARTED]Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
