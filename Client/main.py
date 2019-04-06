import socket
import time
from socket import error as SocketError
import _thread as thread


target = "127.0.0.1"

def listener():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((target, 9000))
    server_socket.listen(1)
    
    while True:
        try:
            clientsocket, adress = server_socket.accept()
        
            data = clientsocket.recv(1024)
            if not data:
                break
            print(data.decode())
        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                raise 
            pass
        finally: 
            clientsocket.close()

def worker():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while True:
        try:
            client_socket.connect((target, 9000))
            client_socket.sendall("F".encode())
            time.sleep(10)
        except ConnectionRefusedError as e:
            print(e)

        finally:
           client_socket.close()

def main():
    thread.start_new_thread(listener, ())
    thread.start_new_thread(worker, ())

    while True:
        pass

if __name__ == "__main__":
    main()