# Chat client

import sys
import socket
import select


def chat_client():
    if len(sys.argv) < 3:
        print('Usage : python chat_client.py hostname port')
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit()
     
    print('Connected to remote host. You can start sending messages')
    sys.stdout.write('[Me] ')
    sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
         
        for sock in read_sockets:            
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)

                if not data:
                    print('\nDisconnected from chat server')
                    sys.exit()

                else:
                    #prints data
                    sys.stdout.write(data.decode('utf-8'))
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()
            
            else:
                # user entered a message
                msg = sys.stdin.readline().encode('utf-8')
                s.send(msg)
                sys.stdout.write('[Me] ')
                sys.stdout.flush()


chat_client()

