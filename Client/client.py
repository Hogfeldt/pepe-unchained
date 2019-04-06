import sys
from socket import *
from lib import Lib

PORT = 9000
BUFSIZE = 1000
# TODO: Message length lugter, og skal ændres til noget der giver mening.
MESSAGE_LENGTH = 100

def receivePeers(peerAddress) :
    message_buffer = b''
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((peerAddress, PORT))

     try:
     raw_response = client_socket.recv(MESSAGE_LENGTH)
     message_buffer += raw_response
     response = message_buffer[:MESSAGE_LENGTH].strip().decode()
    #Skal sende peers når modtaget GET peers
        while response == "GET peers" :
            client_socket.send((+ peers).encode())
            #Skal stoppes når alle peers er sendt.

     finally:
        client_socket.close()




def getPeers(peerAddress) :

    message_buffer = b''
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((peerAddress, PORT))

    try:
        client_socket.send(('%s\n' % "GET peers").encode())
        while ("\n" not in message_buffer) :
            raw_response = client_socket.recv(MESSAGE_LENGTH)
            message_buffer += raw_response
        response = message_buffer[:MESSAGE_LENGTH].strip().decode()
        return response
    finally:
        client_socket.close()

#Få alle peers' addresser.


def changeInChain() :
# Broadcast funktion - changeInChain
    message_buffer = b''
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((peerAddress, PORT))

    try:
        io.sockets.emit('chain got changed', { receivers: 'everyone'})
        while ("\n" not in message_buffer) :
            raw_response = client_socket.recv(MESSAGE_LENGTH)
            message_buffer += raw_response
        response = message_buffer[:MESSAGE_LENGTH].strip().decode()
        if response == "what changed":
            sendChange()
            # Skal stoppes når alle peers er sendt.
    finally:
        client_socket.close()


def sendChange() :
    return getChange()
#Sender ændring i kæde - sendChange


def getChange() :
#Sammenlign kendt chain med ny chain. Hvilke ændringer - getChange
message_buffer = b''
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((peerAddress, PORT))

try:
    client_socket.send(('%s\n' % "").encode())

    #return change
finally:
    client_socket.close()

def newPeer() :
        


def main(argv):

