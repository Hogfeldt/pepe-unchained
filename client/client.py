import socket
import time
import json
from random import randint
from socket import error as SocketError
import _thread as thread

from blockchain.block import Block, dict_to_block, calculate_hash
from blockchain.utils import replace_chain, find_block


target = "127.0.0.1"
MY_IP = "0.0.0.0"
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
                message_buffer = message_buffer.split("\n")[1:]
                while len([b for b in message_buffer.split("\n") if b]) < chain_length:
                    raw_buff = connection_socket.recv(1024)
                    message_buffer += raw_buff.decode()
                json_blocks = message_buffer.split("\n")[:chain_length]
                new_chain = [dict_to_block(json.loads(j)) for j in json_blocks]
                chain = replace_chain(chain, new_chain)
            elif "GET chain" in request:
                chain_length = "%s\n" % len(chain)
                connection_socket.sendall(chain_length.encode())
                for b in chain:
                    block_to_send = "%s\n" % json.dumps(b.__dict__)
                    connection_socket.sendall(block_to_send.encode())
            elif "SIGNAL peers changed" in request:
                while "\n" not in message_buffer:
                    raw_buff = connection_socket, recv(1024)
                    message_buffer += raw_buff.decode()
                peers_length = message_buffer.split("\n")[0]
                message_buffer = message_buffer.split("\n")[1:]
                while len([p for p in message_buffer.split("\n") if p]) < peers_length:
                    raw_buff = connection_socket, recv(1024)
                    message_buffer += raw_buff.decode()
                new_peers = [
                    p for p in message_buffer.split("\n") if p != "" and p != MY_IP
                ]
                for p in new_peers:
                    if p not in peers:
                        peers.append(p)
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
            latest_block = chain[-1]
            nonce = randint(0, 2 ** 100)
            while latest_block == chain[-1]:
                hash = calculate_hash(
                    latest_block.index + 1,
                    latest_block.hash,
                    "lol catz",
                    latest_block.difficulty,
                    nonce,
                )
                if hash_matched_difficulty(hash, latest_block.difficulty):
                    new_block = Block(
                        latest_block.index + 1,
                        hash,
                        latest_block.previous_hash,
                        time.time(),
                        "lol catz",
                        latest_block.difficulty,
                        nonce,
                    )
                    chain.append(new_block)
                    try: 
                        for p in peers
                            connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            connection_socket.connect((p, 9000))
                            connection_socket.sendall("SIGNAL chain changed\n".encode())
                            chain_length = "%s\n" % str(len(chain))
                            connection_socket.sendall(chain_length.encode())
                            for b in chain:
                                json_block = "%s\n" % json.dumps(b.__dict__)
                                connection_socket.sendall(json_block.encode())
                    finally:
                        client_socket.close()
                    break
                nonce += 1

def get_start_info_from_server():
    """ Ask the content provider for the chain and peers """
    content_provider = "0.0.0.0" # TODO: Fake till you make it
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
        chain_length = message_buffer.split("\n")[0]
        message_buffer = message_buffer.split("\n")[1:]
        while len([b for b in message_buffer.split("\n") if b]) < chain_length:
            raw_buff = connection_socket.recv(1024)
            message_buffer += raw_buff.decode()
        json_blocks = message_buffer.split("\n")[:chain_length]
        chain = [dict_to_block(json.loads(j)) for j in json_blocks]
        client_socket.close()
        message_buffer = ""

        # Socket setup
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((content_provider, 9000))
        # Request peers
        start_request = "GET peers\n"
        client_socket.sendall(start_request.encode())
        while "\n" not in message_buffer:
            raw_data = client_socket.recv(1024)
            message_buffer += raw_buff.decode()
        peers_length = message_buffer.split("\n")[0]
        message_buffer = message_buffer.split("\n")[1:]
        while len([p for p in message_buffer.split("\n") if p]) < peers_length:
            raw_buff = connection_socket, recv(1024)
            message_buffer += raw_buff.decode()
        peers = [p for p in message_buffer.split("\n") if p != "" and p != MY_IP]
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
