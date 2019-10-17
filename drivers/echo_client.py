import socket


def main():
    host = '192.168.0.49'
    port = 1717

    mySocket = socket.socket()
    mySocket.connect((host, port))

    message = input(" -> ")
    mySocket.send(message.encode())

    while message != 'q':
        data = mySocket.recv(1024).decode()
        print('Received from server: ' + data)
        if data == 'Ping':
            mySocket.send('Ping OK'.encode())
        elif data == 'check':
            mySocket.send('ok'.encode())
        else:
            mySocket.send('REPEAT'.encode())
        # message = input(" -> ")
    mySocket.close()


if __name__ == '__main__':
    main()



