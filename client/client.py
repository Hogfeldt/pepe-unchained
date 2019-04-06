import socket
import time
import json
from socket import error as SocketError
import _thread as thread

from blockchain.block import Block, dict_to_block


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
            connection_socket, adress = server_socket.accept()
            while "\n" not in message_buffer:
                raw_buff = connection_socket.recv(1024)
                message_buffer += raw_buff.decode()
            request = message_buffer.split("\n")[0]
            message_buffer = message_buffer.split("\n")[1:]

            # Handle request
            if "SIGNAL chain changed" in request:
                while "\n" not in message_buffer:
                    raw_buff = connection_socket.recv(1024)
                    message_buffer += raw_buff.decode()
                chain_length = message_buffer.split("\n")[0]
                while len([b for b in message_buffer.split("\n") if b]) < chain_length:
                    raw_buff = connection_socket.recv(1024)
                    message_buffer += raw_buff.decode()
                json_blocks = message_buffer.split("\n")[:chain_length]
                new_chain = [dict_to_block(json.loads(j)) for j in json_blocks]
                
                # ask for the new chain
                pass
            elif "GET chain" in request:
                chain_length = "%s\n" % len(chain)
                connection_socket.sendall(chain_length.encode())
                for b in chain:
                    block_to_send = "%s\n" % json.dumps(b.__dict__)
                    connection_socket.sendall(block_to_send.encode())
            elif "SIGNAL peers changed" in request:
                # ash for new peer list
                pass
            elif "GET peers" in request:
                peers_length = "%s\n" % len(peers)
                connection_socket.sendall(peers_length.encode())
                for p in peers:
                    peer_to_send = "%s\n" % p
                    connection_socket.sendall(peer_to_send.encode())

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
                # mine chain
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
    peers = []
    chain = []
    try:
        # Socket setup
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((content_provider, 9000))
        # Reauest chain
        start_request = "GET chain\n"
        client_socket.sendall(start_request.encode())
        while "\n" not in message_buffer:
            raw_data = client_socket.recv(1024)
            message_buffer += raw_buff.decode()
        # TODO: create a constructor for Block taking a json string
        client_socket.close()

        # Socket setup
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((content_provider, 9000))
        # Reauest peers
        start_request = "GET peers\n"
        client_socket.sendall(start_request.encode())
        while "\n" not in message_buffer:
            raw_data = client_socket.recv(1024)
            message_buffer += raw_buff.decode()
        # TODO: create a peers list taking a json string
        return (chain, peers)
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
