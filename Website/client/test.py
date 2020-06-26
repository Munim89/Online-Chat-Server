from client import Client
import time
from threading import  Thread

time.sleep(1)
c1 = Client("Tim")
time.sleep(1)
c2 = Client("Joe")

def update_messages():
    """
    Updates the global list of messages
    :return: None
    """
    run = True
    msgs = []
    while run:
        time.sleep(0.1) # update every 1/10 th of a second
        new_messages = c1.get_messages() # to get new messages from a client
        msgs.extend(new_messages)

        for msg in new_messages: # display new messages
            print(msg)
            if msg == "{quit}":
                run = False
                break

Thread(target=update_messages).start()

time.sleep(1)
c1.send_messages("Hello")
time.sleep(1)
c2.send_messages("hello")

time.sleep(1)
c1.send_messages("What's up")
time.sleep(1)
c2.send_messages("Nothing much")
time.sleep(5)

c1.disconnect()
time.sleep(7)
c2.disconnect()
