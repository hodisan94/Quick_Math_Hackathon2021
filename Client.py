import socket
import struct
#https://docs.python.org/3/library/struct.html
import time
import msvcrt
import colors


class Client:
    '''
    The client is a single-threaded app, which has three states:
    ● Looking for a server. You leave this state when you get an offer message.
    ● Connecting to a server. You leave this state when you successfully connect using TCP
    ● Game mode - collect characters from the keyboard and send them over TCP. collect
        data from the network and print it on screen.
    '''
    def __init__(self,team_name,udp_port=13117,tcp_port=None):
        '''
        :param port: port number for tcp connection
        :param team : team name
        '''
        self.team_name = team_name
        self.udp_port = udp_port
        self.udp_socket = None
        self.__tcp_port = tcp_port
        self.tcp_socket = None
        self.magic_cookie = 0xabcddcba
        self.message_type = 0x2
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # https://gist.github.com/cry/9e435d54cbe95fe9fddc2e0596409265
        self.udp_socket.bind(('', self.udp_port))
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



    def start(self):
        '''
        this function call the open_for_offers function - while this thread in the open_for_offers function the client state : Looking for a server
        the open_for_offers function listen to server requests over UDP socket
        when a server request received , we call the connect function and the client state becomes "Connecting to a server"
        the connect function "talks" with the server over TCP connection,
        as soon as the TCP connection with the server is established - we call the play function and client state becomes "Game Mode"
        server send a welcome message' this message will be print to screen and user need to insert input,
        this input will be send to server(or not send till timeout(10 secondes) or the other client allready sent)
        then the server will announce the winner
        and TCP connection will be closed(tcp_port and tcp_socket will be deleted
        after it, call the open_for_offers function and repeat until #TODO: until ?

        :return:
        '''
        self.open_for_offers()


    def open_for_offers(self):
        '''
        client state : Looking for a server
        listen for servers
        :return:
        '''
        colors.print_Green("Client started, listening for offer requests...")
        # socket_exists = False
        # while not socket_exists:
        #     try:
        #         # socket.AF_INET AF_INET - family = Internet
        #         # socket.SOCK_DGRAM - type UDP
        #         self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        #         socket_exists = True
        #     except socket.error:
        #         # print("Something goes bananas --> solve your UDP problems")
        #         continue
        # """
        # socket.setsocketopt() need to done before bind
        # https: // stackoverflow.com / questions / 6380057 / python - binding - socket - address - already - in -use
        # https://docs.python.org/3/library/socket.html
        # """
        # self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # #self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # https://gist.github.com/cry/9e435d54cbe95fe9fddc2e0596409265
        # self.udp_socket.bind(('', self.udp_port))
        while True:#TODO: how we prevent inf loop?
            """
            get masseage from server
            https://pythontic.com/modules/socket/recvfrom
            message , address = self.udp_socket.recvfrom(1024)
            """
            message,address = self.udp_socket.recvfrom(1024)
            #TODO : talk about the message foramt!!!
            magic_cookie_received,message_type_received,server_port = struct.unpack(">IbH",message)
            #sainty check
            if (magic_cookie_received==self.magic_cookie and message_type_received==self.message_type):
                #colors.print_Green("Received offer from ",address[0],",attempting to connect...")
                print("Received offer from ", address[0], ",attempting to connect...")
                return self.connect_to(address,server_port)

    def connect_to(self,address,server_port):
        '''
        client state : Connecting to a server
        connent to server with TCP
        :param self:
        :param address: address
        :param server_port: server port
        :return: True is connection succeeded, False if connection failed
        '''
        #socket.SOCK_STREAM - TCP connection
        try:
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("101")
            self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print("102")
            self.tcp_socket.connect((address[0],server_port))
            print("103")
            self.tcp_socket.send(bytes(self.team_name + "\n",'UTF-8'))
            print("104")
        except socket.error as err:#connect failed - go back to "client state : Looking for a server"
            #self.tcp_socket.close()
            what_he_said = "The ##*&@#*#% %##&*%*& server said me that : " + str(err)
            colors.print_Red(what_he_said)
            colors.print_Red("So........\nThere were problems with this server...\n(wait until you see how he looks like ...)\nNo matter, there are plenty of other servers in Hackathon so I'm back to listening for offer requests from other servers...")
            try:
                self.tcp_socket.close()
            except socket.error:
                self.tcp_socket = None
            self.__tcp_port = None
            self.tcp_socket = None
            return self.open_for_offers()
        return self.play()

    def play(self):
        '''
        client state : Game mode
        :return:
        '''
        try:
            welcome_message = self.tcp_socket.recv(1024).decode('UTF-8')
        except socket.error as err:
            colors.print_Yellow(self.team_name)
            colors.print_Yellow("Has problem with the Server welcome message...")
            return

        colors.print_Cyan(welcome_message)
        #TODO: decide which library to use - msvcrt or keyboard
        #msvcrt
        answer = msvcrt.getch()
        #answer = msvcrt.getch.getch()
        if (answer!='\000' and answer!='\xe0' and answer!=None):
            self.tcp_socket.send(answer)
        end_message = self.tcp_socket.recv(1024).decode('UTF-8')
        colors.print_Green(end_message)
        try:
            self.tcp_socket.close()
            colors.print_Red("Server disconnected, listening for offer requests...")
            self.__tcp_port = None
            self.tcp_socket = None
            return self.open_for_offers()
        except:
            colors.print_Red("There are some issues with closing this TCP connection...\nHope we did not break the internet ;-(")
            colors.print_Red("Server disconnected, listening for offer requests...")
            self.__tcp_port = None
            self.tcp_socket = None
            return self.open_for_offers()








            





