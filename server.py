# Tcp Chat server

import socket, select


class ChatRoom:
    number = 0
    memberList = []

    def __init__(self, number, name, socket):
        self.number = number
        self.memberList.append({'name': name, 'socket': socket})

    def enter(self, name, socket):
        self.memberList.append({'name': name, 'socket': socket})

    def exit(self, name, socket):
        self.memberList.remove({'name': name, 'socket': socket})
        if len(self.memberList) == 0:
            chatroomList.remove(self)

    def broadcastData(self, name, socket, type, data = ''):
        if type == 'exit':
            for info in self.memberList:
                if name != info['name']:
                    try:
                        info['socket'].send(name + 'leave ChatRoom' + self.number)
                    except:
                        info['socket'].close()
                        self.exit(info['name'], info['socket'])
            self.exit(name, socket)
            return 1
        if type == 'enter':
            for info in self.memberList:
                try:
                    info['socket'].send(name + 'enter ChatRoom' + self.number)
                except:
                    info['socket'].close()
                    self.exit(info['name'], info['socket'])
            return 1
        print type, data
        for info in self.memberList:
            if name != info['name']:
                try:
                    info['socket'].send(name + ': ' + data)
                except:
                    info['socket'].close()

def command_handler(name, socket, message):
    command = message.split()[0]
    if command == '/exit':
        for room in chatroomList:
            for info in room.memberList:
                if name == info['name']:
                    room.broadcastData(name, socket, 'exit')
                    user.room = ''
        return ''
    if command == '/enter':
        for room in chatroomList:
            if room.number == (message.split())[1]:
                room.broadcastData(name, socket, 'enter')
                room.enter(name, socket)
                print chatroomList[0].memberList
                return room
        newRoom = ChatRoom((message.split())[1], name, socket)
        chatroomList.append(newRoom)
        return newRoom




class User:
    name = ''
    socket = ''
    room = '123'

    def __init__(self, name, socket):
        self.name = name
        self.socket = socket


def test():
    userList.append(User('zz', 'zz'))

if __name__ == "__main__":
    chatroomList = []
    userList = []

    # test()

    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096  # Advisable to keep it as an exponent of 2
    PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    print "Chat server started on port " + str(PORT)

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])

        for sock in read_sockets:
        # New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr

        # Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        if data[0] == '/':
                            login = 0
                            for user in userList:
                                if user.socket == sock:
                                    user.room = command_handler(user.name, sock, data)
                                    login = 1
                                    break

                            if login == 0:
                                userList.append(User(data, sock))

                        else:
                            print user.room
                            for user in userList:
                                if user.socket == sock:
                                    user.room.broadcastData(user.name, user.socket, 'msg' ,data)
                except:
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

    server_socket.close()
