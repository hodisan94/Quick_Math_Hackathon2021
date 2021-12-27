import socket
import time
from threading import Thread

#daniel first commit
class Server:
    def __init__(self,tcp_port):
        self.udp_port = 13117
        self.tcp_port = tcp_port

        self.broad_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        self.broad_udp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
        self.ip = socket.gethostbyname(socket.gethostname())
        self.magicCookie = 0xabcddcba
        self.msg_type = 0x2
        self.msg = self.magicCookie.to_bytes(byteorder='big', length=4) + self.msg_type.to_bytes(byteorder='big', length=1) + self.tcp_port.to_bytes(byteorder='big', length=2)

        self.tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcp_socket.bind(("" , self.tcp_port))

        self.player_client1 = None
        self.player_client1_name = None
        self.player_client2 = None
        self.player_client2_name = None

    def check_players(self): #function to make sure the player are connected
        if self.player_client1 is None or self.player_client2 is None:
            return False
        else:
            return True

    def broadcast(self):
        print("Server started, listening on IP address " + str(self.ip))
        while not self.check_players():

            self.broad_udp_socket.sendto(self.msg , ('255.255.255.255', self.udp_port))
            time.sleep(1)


    def looking_for_mighty_and_fearless_players(self): #TODO need check this...
        #we want to find only two player
        self.tcp_socket.listen(2)
        while not self.check_players():
            if self.player_client1 is None:
                client_connection , client_address = self.tcp_socket.accept()
                self.player_client1 = client_connection
                self.player_client1_name = self.player_client1.recv(1024).decode('UTF-8')
            elif self.player_client2 is None:
                client_connection, client_address = self.tcp_socket.accept()
                self.player_client2 = client_connection
                self.player_client2_name = self.player_client1.recv(1024).decode('UTF-8')

    #TODO start game , end game, measure time , start server....








