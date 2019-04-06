import socket
import time
from socket import error as SocketError
import _thread as thread

from blockchain.block import Block


target = "127.0.0.1"
chain = []
peers = []


def listener():
    """ The listener will handle incomming requests og signals from peers """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", 9000))
    server_socket.listen(1)

    message_buffer = ""

    while True:
        try:
            clientsocket, adress = server_socket.accept()
            while "\n" not in message_buffer:
                raw_buff = clientsocket.recv(1024)
                message_buffer += raw_buff.decode()
            request = message_buffer.split("\n")[0]
            message_buffer = message_buffer.split("\n")[1:]

            # Handle request
            if "SIGNAL chain changed" in request:
                # ask for the new chain
                pass
            elif "GET chain" in request:
                # send back a copy of chain
                pass

        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                raise
            pass
        finally:
            clientsocket.close()
            # Flush message_buffer
            message_buffer = ""


def worker():
    """ This worker will try to mine a new block until the block is mined og the chain has changed """
    try:
        while True:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((target, 9000))
                client_socket.sendall("F".encode())
                time.sleep(1)
            except ConnectionRefusedError as e:
                print(e)

            finally:
                client_socket.close()
    except KeyboardInterrupt:
        client_socket.close()


def get_start_info_from_server():
    """ Ask the content provider for the chain and peers """
    content_provider = "0.0.0.0"
    message_buffer = ""
    try:
        # Socket setup
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((content_provider, 9000))
        # Reauest chain
        start_request = "GET chain \n"
        client_socket.sendall(start_request.encode())
        

        # Request peers
        return ([], [])
    finally:
        client_socket.close()


def main():
    chain, peers = get_start_info_from_server()
    thread.start_new_thread(listener, ())
    time.sleep(2)
    thread.start_new_thread(worker, ())

    while True:
        pass


if __name__ == "__main__":
    main()
