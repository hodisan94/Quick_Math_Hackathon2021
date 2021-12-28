import random
import socket
import struct
import time
from threading import Thread , Event

import colors


class Server:
    def __init__(self,tcp_port):
        self.udp_port = 13117
        self.tcp_port = tcp_port

        self.broad_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        self.broad_udp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
        self.ip = socket.gethostbyname(socket.gethostname())
        self.magicCookie = 0xabcddcba
        self.msg_type = 0x2
        self.msg = struct.pack(">IbH",self.magicCookie,self.msg_type,self.tcp_port)
        self.tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.tcp_socket.bind(("", self.tcp_port))

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


    def looking_for_mighty_and_fearless_players(self):
        #we want to find only two player
        self.tcp_socket.listen(2)
        while not self.check_players():
            if self.player_client1 is None:
                client_connection , client_address = self.tcp_socket.accept()
                self.player_client1 = client_connection
                self.player_client1_name = self.player_client1.recv(1024).decode('UTF-8')
                # print("Received offer from " +str(self.player_client1) + ", attempting to connect...")
            elif self.player_client2 is None:
                client_connection, client_address = self.tcp_socket.accept()
                self.player_client2 = client_connection
                self.player_client2_name = self.player_client2.recv(1024).decode('UTF-8')
                # print("Received offer from " +str(self.player_client1) + ", attempting to connect...")




    def start_server_end_server(self):
        t1 = Thread(target=self.broadcast, daemon=True)
        t2 = Thread(target=self.looking_for_mighty_and_fearless_players, daemon=True)

        t1.start()
        t2.start()

        while not self.check_players():
            time.sleep(0.1)

        #waiting 10 sec before starting the game for the clients
        print('\x1b[6;30;45m' + 'R U Ready to rumble ?' + '\x1b[0m')
        for i in range(0,9):
            colors.print_Cyan(10-i)
            time.sleep(1)
        print('\x1b[6;30;45m' + '     YALLA     ' + '\x1b[0m')
        colors.print_Cyan("1")
        print('\x1b[6;30;45m' + 'Open your STORY' + '\x1b[0m')
        print('')

        the_winner_msg = self.start_game()

        self.player_client1.send(bytes(the_winner_msg,'UTF-8'))
        self.player_client2.send(bytes(the_winner_msg,'UTF-8'))

        self.tcp_socket.close()
        time.sleep(1.5)
        print('\x1b[5;30;42m' + '   Game over, sending out offer requests...   ' + '\x1b[0m')
        #print("Game over, sending out offer requests...")



    def start_game(self):
        #selecting two random numbers that the sum of them wont be greather then 9
        num1 = random.randint(0,9)
        num2 = random.randint(0,(9-num1))
        res = num1+num2
        nice_msg = "Welcome to Quick Math \nPlayer 1: " + self.player_client1_name +"Player 2: " + self.player_client2_name +"==\n"+"Please answer the following question as fast as you can:\nHow much is " +str(num1) + "+" + str(num2)+"?"

        #sending the starting msg to both clients
        self.player_client1.send(bytes(nice_msg, 'UTF-8'))
        self.player_client2.send(bytes(nice_msg, 'UTF-8'))

        pause_event = Event()
        who_won_who_won=[]

        t_for_player1 = Thread(target=self.get_answer, args=[self.player_client1, pause_event, who_won_who_won, 1])
        t_for_player2 = Thread(target=self.get_answer, args=[self.player_client2, pause_event, who_won_who_won, 2])

        t_for_player1.start()
        t_for_player2.start()

        #wating and giving the player time to answer the question
        while not pause_event.is_set():
            time.sleep(0.1)


        finish_msg = "Game over!\nThe correct answer was " +str(res)+"!\n"
        # if we got an answer from one of the player we will check who it is and who won
        if len(who_won_who_won) != 0:
            if who_won_who_won[1] == self.player_client1:
                if str(who_won_who_won[0].decode('UTF-8')) == str(res): #hope it will work
                    finish_msg = finish_msg + "Congratulations to the winner: "+self.player_client1_name
                else:
                    finish_msg = finish_msg + "Congratulations to the winner:" +self.player_client2_name

            elif who_won_who_won[0] == self.player_client2:
                if str(who_won_who_won[1].decode('UTF-8')) == str(res): #hope it will work
                    finish_msg = finish_msg + "Congratulations to the winner:" + self.player_client2_name
                else:
                    finish_msg = finish_msg + "Congratulations to the winner:" + self.player_client1_name
        #no one answerd in the given time so its a draw
        else:
            finish_msg = finish_msg + "both teams are losers...so we had to call for a draw."
        #print(finish_msg)
        return finish_msg


    def get_answer(self , player , event , winner_info_list , num):
        right_now = time.time()
        limit_time = right_now+10
        player.setblocking(0)
        while not event.is_set():
            try:
                winner_info_list[0] = player.recv(1024) #answer
                winner_info_list[1] = player #the player
            except:
                pass
            #reached time limit
            if time.time() > limit_time:
                event.set()
                #print("timeout")
                return
            #check if we got an answer by now
            if len(winner_info_list) != 0:
                event.set()
                return



if __name__ == '__main__':
    while True:
        new_server = Server(2045)
        serverT = Thread(target=new_server.start_server_end_server)
        serverT.start()
        serverT.join()
    #new_server.start_server_end_server()




