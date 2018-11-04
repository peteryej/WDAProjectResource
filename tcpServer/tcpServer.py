#"https://gist.github.com/Integralist/3f004c3594bbf8431c15ed6db15809ae"

import socket
import datetime
import threading

bind_ip = '0.0.0.0'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(10)  # max backlog of connections

print 'Listening on {}:{}'.format(bind_ip, bind_port)


def handle_client_connection(client_socket):
    request = client_socket.recv(512)    
    print(datetime.datetime.now())
    print 'Received {}'.format(request)
    print('--------------------------------------')
    #client_socket.send('ACK!')
    client_socket.close()


while True:
    client_sock, address = server.accept()
    print 'Accepted connection from {}:{}'.format(address[0], address[1])   
    client_handler = threading.Thread(
        target=handle_client_connection,
        # without comma you'd get a... TypeError: handle_client_connection()
        # argument after * must be a sequence, not _socketobject
        args=(client_sock, ))
    client_handler.start()
