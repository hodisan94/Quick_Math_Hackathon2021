from threading import Thread
import colors
from Client import Client
from Server import Server


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #server = Server(2049)
    client = Client("Maccabi")
    client_ = Client("not_Maccabi")

    #serverThread = Thread(target=server.start_server_end_server,daemon=True)
    clientThread = Thread(target=client.start)
    client_Thread = Thread(target=client_.start)


    #serverThread.start()

    clientThread.start()
    client_Thread.start()

    #serverThread.join()
    clientThread.join()
    client_Thread.join()






# See PyCharm help at https://www.jetbrains.com/help/pycharm/
