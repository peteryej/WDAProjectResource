
import socket
import datetime
import threading

bind_ip = '0.0.0.0'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(10)  # max backlog of connections

print 'Listening on {}:{}'.format(bind_ip, bind_port)


if __name__ == "__main__":
    client_socket1, address1 = server.accept()
    print 'Accepted connection from {}:{}'.format(address1[0], address1[1]) 

    client_socket2, address2 = server.accept()
    print 'Accepted connection from {}:{}'.format(address2[0], address2[1]) 

    client_socket1.send('ACK!')
    client_socket2.send('ACK!')
    client_socket1.close()
    client_socket2.close()