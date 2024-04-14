import socket
import select
import argparse

# optional arguments hooraay 🎉
parser = argparse.ArgumentParser(description='Chat server that listens on a specified port and allows multiple clients to connect and chat with each other.')
parser.add_argument('--port', type=int, default=9009, help='Port number to listen on. Default is 9009.')
parser.add_argument('--host', type=str, default='localhost', help='Host name to listen on. Default is localhost.')
parser.add_argument('--buffer', type=int, default=4096, help='Buffer size for receiving messages. Default is 4096.')

args = parser.parse_args()

HOST = args.host
PORT = args.port
RECV_BUFFER = args.buffer
SOCKET_LIST = []

def chat_server():

    # Using a stream socket because data integrity is important
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # IPv4, TCP
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    SOCKET_LIST.append(server_socket)
 
    print ("Chat server started on port " + str(PORT))

    while True:
        # Select lets us monitor sockets, we only use the read list
        ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)

        for sock in ready_to_read:
            if sock == server_socket:   # if there's a client connection
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print ("Client (%s, %s) connected" % addr)

                broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)
            else:
                # process data recieved from client,
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER).decode('utf-8')
                    if data:
                        # there is something in the socket
                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)
                    else:
                        # remove the socket that's broken
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)

                # exception
                except Exception as e:
                    print(e)
                    broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    if sock in SOCKET_LIST:
                        SOCKET_LIST.remove(sock)
                    continue
                    
    server_socket.close()

# broadcast chat messages to all connected clients


def broadcast(server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock:
            try :
                socket.send(message.encode('utf-8'))
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 

chat_server()


         
