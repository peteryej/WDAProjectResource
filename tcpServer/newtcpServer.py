#"https://gist.github.com/Integralist/3f004c3594bbf8431c15ed6db15809ae"

import socket
import datetime
import time
import threading

bind_ip = '0.0.0.0'
bind_port = 9999

localClient = None

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(100)  # max backlog of connections

print 'Listening on {}:{}'.format(bind_ip, bind_port)


def handle_client_connection(client_socket, isLocalClient):
    global localClient
    if not isLocalClient:
        request = client_socket.recv(512)
        curTime = datetime.datetime.now()
        print('--------------------------------------')
        print(curTime)
        print(request)
        print('--------------------------------------')

        if (localClient):
            strTime = curTime.strftime('%Y-%m-%d %H:%M:%S.%f')
            localClient.send(strTime+'\n'+request)

        client_socket.close()
    else:
        print('localClient connected')
        request = client_socket.recv(512)
        client_socket.close()
        localClient = None


while True:
    client_sock, address = server.accept()
    print 'Accepted connection from {}:{}'.format(address[0], address[1])
    
    
    isLocalClient = False
    if (address[0] == '127.0.0.1'):
        localClient = client_sock
        isLocalClient = True

    client_handler = threading.Thread(
        target=handle_client_connection,
        # without comma you'd get a... TypeError: handle_client_connection()
        # argument after * must be a sequence, not _socketobject
        args=(client_sock, isLocalClient,)
    )
    client_handler.start()
