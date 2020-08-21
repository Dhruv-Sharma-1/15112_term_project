import socket
import threading
from queue import Queue


#CITED -- Sockets Client Demo by Rohan Varma and Kyle Chin
HOST = "127.0.0.1"
PORT = 51001
BACKLOG = 5

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(BACKLOG)
print ("Looking for Connection")

def handleClient(client, server, ID, clientele):
    client.setblocking(1)
    msg = ""
    while True:
        try:
            msg += client.recv(4096).decode("utf-8")
            command = msg.split("\n")
            while len(command) > 1:
                readyMsg = command[0]
                msg = "\n".join(command[1:])
                serverChannel.put(str(ID) + " " + readyMsg)
                command = msg.split("\n")
        except:
            return None

def serverThread(clientele, serverChannel):
    while True:
        msg = serverChannel.get(True, None)
        # print("msg recv: ", msg)
        msgList = msg.split(" ")
        senderID = msgList[0]
        task = msgList[1]
        details = " ".join(msgList[2:])
        if details != "":
            for ID in clientele:
                if ID != senderID:
                    sendMsg = task + " " + senderID + " " + details + "\n"
                    clientele[ID].send(sendMsg.encode())
                    # print("> sent to %s:" % ID, sendMsg[:-1])
        serverChannel.task_done()


clientele = dict()
names = ["Player1", "Player2", "Player3", "Player4", "Player5"]
playerNum = 0
serverChannel = Queue(100)
thread = threading.Thread(target = serverThread,
                                            args = (clientele, serverChannel))
thread.start()

while True:
    client, address = s.accept()
    myID = names[playerNum]
    print (myID, playerNum)
    for ID in clientele:
        clientele[ID].send(("newPlayer %s\n" % myID).encode())
        client.send(("newPlayer %s\n" % ID).encode())
    clientele[myID] = client
    client.send(("myIDis %s\n" % myID).encode())
    print ("connection recieved from %s" % myID)
    threading.Thread(target = handleClient,
                    args = (client, serverChannel, myID, clientele)).start()
    playerNum += 1
