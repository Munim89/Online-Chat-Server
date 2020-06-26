from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread, Lock
import time

class Client:
    """
    for communicating with the server
    """
    # Global constants
    HOST = "localhost"
    PORT = 5500
    ADDR = (HOST, PORT)
    BUFSIZ = 512

    def __init__(self, name):
        """
        Initializing object and sending it o the web server
        :param name: str
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_messages(name)
        self.lock = Lock()

    def receive_messages(self):
        """
        receive messages from the server
        return:
        """
        while True:
            try:
                # to make sure that the message is safe to access
                msg = self.client_socket.recv(self.BUFSIZ).decode()
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print("[FAILURE]: ", e)
                break

    def send_messages(self, msg):
        """
        Send messages to the server
        :param msg:str
        :return:None
        """
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()

    def get_messages(self):
        """
        Returns str messages
        :return: str
        """

        messages_copy = self.messages[:]
        self.lock.acquire()
        self.messages = []
        self.lock.release()

        return messages_copy

    def disconnect(self):
        self.send_messages(bytes("{quit}", "utf8"))