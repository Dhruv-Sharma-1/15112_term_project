import socket
import threading
from queue import Queue
import math
import copy
import random
from tkinter import *
from tp_logic import *
from tp_cards import *

######
#All my code except lines 15 - 36, cited from  Sockets Client Demo by Rohan
# Varma and Kyle Chin
# and lines 1133 - 1178, cited from 112 website



#CITED --
HOST = "127.0.0.1"
PORT = 51001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
serverMsg = Queue(100)
print ("Connected to Server")

def handleServerMsg(server, serverMsg):
    server.setblocking(1)
    msg = ""
    command = ""
    while True:
        msg += server.recv(4096).decode("utf-8")
        command = msg.split("\n")
        while len(command) > 1:
            readyMsg = command[0]
            msg = "\n".join(command[1:])
            serverMsg.put(readyMsg)
            command = msg.split("\n")

threading.Thread(target = handleServerMsg, args = (s, serverMsg)).start()

def playTeenPatti():
    width, height = 800, 600
    run(width, height, serverMsg, s)

# States:
# 0 ---> HomeScreen
# 1 ---> Board GamePlay
# 2 ---> Instructions Page
# 3 ---> Options
# 4 ---> Variations
# 5 ---> Winner Screen


def init(data):
    data.state = 0
    data.players = 1
    data.clickName = False
    data.myID = None
    data.name = data.myID
    data.deck = createDeck()
    data.variation = 0
    if data.variation == 0:
        data.numCards = 3
    data.hands = None
    data.handsImgs = None
    boardPath = "term_project/Images/table.gif"
    data.board = PhotoImage(file = boardPath)
    backPath = "term_project/Images/back.gif"
    data.cardBack = PhotoImage(file = backPath)
    backflatpath = "term_project/Images/backflat.gif"
    data.backflat = PhotoImage(file = backflatpath)
    # backleft = "/Users/dhruvsharma/Desktop/term_project/Images/back313.gif"
    # data.backleft = PhotoImage(file = backleft)
    # backright = "/Users/dhruvsharma/Desktop/term_project/Images/back47.gif"
    # data.backright = PhotoImage(file = backright)
    homepath = "term_project/HomeScreen/acetrail.gif"
    data.home = PhotoImage(file = homepath)
    playpath = "term_project/HomeScreen/play.gif"
    data.play = PhotoImage(file = playpath)
    instrctpath = "term_project/HomeScreen/rules.gif"
    data.instrct = PhotoImage(file = instrctpath)
    namepath = "term_project/HomeScreen/name.gif"
    data.nameImg = PhotoImage(file = namepath)
    multipath = "term_project/HomeScreen/multi.gif"
    data.multi = PhotoImage(file = multipath)
    betpath = "term_project/Images/bet.gif"
    data.betImg = PhotoImage(file = betpath)
    showpath = "term_project/Images/show.gif"
    data.showImg = PhotoImage(file = showpath)
    raisepath = "term_project/Images/raise.gif"
    data.raiseImg = PhotoImage(file = raisepath)
    sideshowpath = "term_project/Images/sideshow.gif"
    data.sideshowImg = PhotoImage(file = sideshowpath)
    seepath = "term_project/Images/see.gif"
    data.seecards = PhotoImage(file = seepath)
    packpath = "term_project/Images/fold.gif"
    data.foldImg = PhotoImage(file = packpath)
    redpath = "term_project/HomeScreen/red.gif"
    data.redback = PhotoImage(file = redpath)
    acepath = "term_project/HomeScreen/ace.gif"
    data.aceback = PhotoImage(file = acepath)
    introtext = "term_project/HomeScreen/intro.gif"
    data.intro = PhotoImage(file = introtext)
    trailpath = "term_project/HomeScreen/trail.gif"
    data.trailimg = PhotoImage(file = trailpath)
    purepath = "term_project/HomeScreen/pureseq.gif"
    data.pureseqimg = PhotoImage(file = purepath)
    seqpath = "term_project/HomeScreen/sequence.gif"
    data.seqimg = PhotoImage(file = seqpath)
    colorpath = "term_project/HomeScreen/color.gif"
    data.colorimg = PhotoImage(file = colorpath)
    pairpath = "term_project/HomeScreen/pair.gif"
    data.pairimg = PhotoImage(file = pairpath)
    highpath = "term_project/HomeScreen/highcard.gif"
    data.highimg = PhotoImage(file = highpath)
    bestpath = "term_project/HomeScreen/besthand.gif"
    data.bestxt = PhotoImage(file = bestpath)
    mufflispath = "term_project/HomeScreen/mufflis.gif"
    data.mufflis = PhotoImage(file = mufflispath)
    data.samplehands = createSampleHands(data)
    data.blind = True
    data.myturn = True
    data.sideShow = False
    data.show = False
    data.chips = 1000
    data.mufflisGame = False
    data.buyin = 1
    data.round = 1
    data.fold = False
    data.Cbet = 2
    data.pot = 0
    data.gameStart = False
    data.winner = None
    data.wins = 0
    data.sideShowWinner = None
    data.sideShowLoser = None
    data.skip = False
    data.others = dict()


def createHandImage(data):
    handImage = set()
    for card in data.hands:
        img = card.drawMe()
        handImage.add(img)
    return handImage


def mousePressed(event, data):
    ex, ey = event.x, event.y
    msg = ""
    if data.state == 0:
        if clickPlay(ex, ey, data):
            data.state = 3
        if clickInstrct(ex, ey, data):
            data.state = 2

    if data.state == 1:
        if data.myturn:
            if data.skip:
                if clickAnywhere(ex, ey, data):
                    msg = "fold %s\n" %data.myID
                    data.myturn = False
            else:
                if clickFold(ex, ey, data):
                    data.fold = True
                    msg = "fold %s\n" % data.myID
                    data.myturn = False
                if clickBet(ex, ey, data):
                    if data.blind:
                        blindBet = data.Cbet // 2
                        data.chips -= blindBet
                        data.pot += blindBet
                    else:
                        data.chips -= data.Cbet
                        data.pot += data.Cbet
                    data.myturn = False
                    msg = "bet %d %d\n" % (data.pot, data.Cbet)
                if clickRaise(ex, ey, data):
                    data.Cbet *= 2
                    if data.blind:
                        blindBet = data.Cbet // 2
                        data.chips -= blindBet
                        data.pot += blindBet
                    else:
                        data.chips -= data.Cbet
                        data.pot += data.Cbet
                    data.myturn = False
                    msg = "raise %d %d\n" % (data.pot, data.Cbet)
                if clickSeeCards(ex, ey, data):
                    data.blind = False
                    msg = "cardSeen %s\n" % data.name
                if clickShow(ex, ey , data):
                    data.chips -= data.Cbet
                    data.pot += data.Cbet
                    data.myturn = False
                    msg = "askShow {pot} {hand}\n" .format(hand = data.hands,
                                                        pot = data.pot)
                if clickSideshow(ex, ey, data):
                    data.chips -= data.Cbet
                    data.pot += data.Cbet
                    ID = checkTypeShow(data)[1]
                    data.myturn = False
                    msg = "sideShow {id} {pot} {hand}\n" .format(id = ID,
                                                pot = data.pot, hand = data.hands)

    if data.state == 3:
        if clickInputName(ex, ey, data):
            data.clickName = True
            data.name = input("Enter Name: ")
            msg = "inputName %s\n" % data.name
        if data.clickName:
            if clickOutsideNameBox(ex, ey, data):
                data.clickName = False
        if clickMultiplayer(ex, ey, data):
            if data.gameStart:
                data.state = 1
            else:
                data.gameStart = True
                data.state = 1
                data.hands = dealCards(data.deck, 1, data.numCards)[0]
                data.handsImgs = createHandImage(data)
                msg = "gameStarted {}\n" .format(data.deck)
        if clickMufflis(ex, ey, data):
            if data.gameStart:
                data.state = 1
            else:
                data.gameStart = True
                data.state = 1
                data.mufflisGame = True
                data.hands = dealCards(data.deck, 1, data.numCards)[0]
                data.handsImgs = createHandImage(data)
                msg = "mufflis {}\n" .format(data.deck)

    if data.state == 5:
        if clickAnywhere(ex, ey, data):
            data.state = 1
            data.pot = 0
            data.winner = None
            data.round += 1
            turn = random.randint(1, data.players)
            playerState = "B"
            for ID in data.others:
                playerName = data.others[ID][0]
                data.others[ID] = (playerName, playerState)
            data.deck = createDeck()
            hands = dealCards(data.deck, data.players, data.numCards)
            playerNum = int(data.myID[-1])
            if playerNum == turn:
                data.myturn = True
            data.blind = True
            data.fold = False
            data.skip = False
            data.Cbet = 2
            data.hands = hands[playerNum - 1]
            data.handsImgs = createHandImage(data)
            msg = "newGame {t} {hand}\n" .format(hand = hands, t = turn)

    if msg != "":
        # print ("sending: ", msg)
        data.server.send(msg.encode())

def clickPlay(ex, ey, data):
    x0, x1 = data.width/4 - 288/2, data.width/4 + 288/2
    y0, y1 = 7*data.height/8 - 81/2, 7*data.height/2 + 81/2
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickAnywhere(ex, ey, data):
    return (0 <= ex <= data.width) and (0 <= ey <= data.height)

def clickInstrct(ex, ey, data):
    x0, x1 = 3*data.width/4 - 360/2, 3*data.width/4 + 360/2
    y0, y1 = 7*data.height/8 - 81/2, 7*data.height/2 + 81/2
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickInputName(ex, ey, data):
    x0, x1 = data.width/2 - 292/2, data.width/2 + 292/2
    y0, y1 = data.height/4 - 81/2, data.height/4 + 81/2
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickOutsideNameBox(ex, ey, data):
    x0, x1 = data.width/2 - 292/2, data.width/2 + 292/2
    y0, y1 = data.height/4 - 81/2, data.height/4 + 81/2
    return (ex < x0) or (ex > x1) or (ey < y0) or (ey > y1)

def clickMultiplayer(ex, ey, data):
    x0, x1 = data.width/2 - 290/2, data.width/2 + 290/2
    y0, y1 = data.height/2 - 81/2, data.height/2 + 81/2
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickMufflis(ex, ey, data):
    x0, x1 = data.width/2 - 246/2, data.width/2 + 246/2
    y0, y1 = 3*data.height/4 - 73/2, 3*data.height/4 + 73/2
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickFold(ex, ey, data):
    x0, x1 = data.width/5 - 126/2, data.width/5 + 126/2
    y0, y1 = 7*data.height/8 - 48/2, 7*data.height/8 + 48/2
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickBet(ex, ey, data):
    x0, x1 = 2*data.width/5 - 125/2, 2*data.width/5 + 125/2
    y0, y1 = 7*data.height/8 - 53/2, 7*data.height/8 + 53/2
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickRaise(ex, ey, data):
    x0, x1 = 3*data.width/5 - 125/2, 3*data.width/5 + 125/2
    y0, y1 = 7*data.height/8 - 53/2, 7*data.height/8 + 53/2
    return (x0 <= ex <= x1) and (y0 <= ey <= y1)

def clickSeeCards(ex, ey, data):
    x0, x1 = 4*data.width/5 - 126/2, 4*data.width/5 + 126/2
    y0, y1 = 5*data.height/6 - 48/2, 5*data.height/6 + 48/2
    if data.blind:
        return (x0 <= ex <= x1) and (y0 <= ey <= y1)
    return False

def clickShow(ex, ey, data):
    x0, x1 = 4*data.width/5 - 125/2, 4*data.width/5 + 125/2
    y0, y1 = 5.5*data.height/6 - 53/2, 5.5*data.height/6 + 53/2
    if data.blind:
        return False
    if checkTypeShow(data) != None and checkTypeShow(data)[0] == "show":
        return (x0 <= ex <= x1) and (y0 <= ey <= y1)
    return False

def clickSideshow(ex, ey, data):
    x0, x1 = 4*data.width/5 - 126/2, 4*data.width/5 + 126/2
    y0, y1 = 5.5*data.height/6 - 54/2, 5.5*data.height/6 + 54/2
    if data.blind:
        return False
    if checkTypeShow(data) != None and checkTypeShow(data)[0] == "sideShow":
        return (x0 <= ex <= x1) and (y0 <= ey <= y1)
    return False

def keyPressed(event, data):
    ek = event.keysym
    ec = event.char
    msg = ""
    if data.state == 0:
        if ec == "p":
            data.state = 1
        if ec == "i":
            data.state = 2

    if data.state == 1:
        if ec == "e":
            msg = "quitGame\n"
            init(data)
        if data.myturn and ec == "s":
            data.blind = False
        if data.winner != None and ek == "Return":
            data.state = 5
            msg = "winner {winner} {pot}\n" .format(winner = data.winner,
                                                    pot = data.pot)
        if data.sideShowWinner != None and ek == "Return":
            msg = "sideshowComplete {win} {lose}\n" .format(win =
                            data.sideShowWinner, lose = data.sideShowLoser)
        if data.sideShowWinner != None and ek == "space":
            data.sideShowWinner = None
            data.sideShowLoser = None
            msg = "sideshowOver %s\n" % data.myID

    if data.state == 2:
        if ec == "e" or ec == "b":
            data.state = 0
        if ek == "BackSpace" or ek == "Delete":
            data.state = 0

    if data.state == 3:
        if ec == "e" or ec == "b":
            data.state = 0

    if data.state == 5:
        if ec == "e" or ec == "b":
            data.state = 1
            data.pot = 0
            data.winner = None
            data.round += 1
            turn = random.randing(1, data.players)
            playerState = "B"
            for ID in data.others:
                playerName = data.others[ID][0]
                data.others[ID] = (playerName, playerState)
            data.deck = createDeck()
            hands = dealCards(data.deck, data.players, data.numCards)
            playerNum = int(data.myID[-1])
            if playerNum == turn:
                data.myturn = True
            data.blind = True
            data.fold = False
            data.Cbet = 2
            data.hands = hands[playerNum - 1]
            data.handsImgs = createHandImage(data)
            msg = "newGame {t} {hand}\n" .format(hand = hands, t = turn)


    if msg != "":
        # print ("sending: ", msg)
        data.server.send(msg.encode())

def checkWin(data):
    for ID in data.others:
        playerState = data.others[ID][1]
        if playerState != "F":
            return False
    return True




def timerFired(data):
    if data.fold:
        data.skip = True
    if data.chips < 0:
        data.chips = 1000
        data.buyin += 1
    if data.pot > 0 and checkWin(data):
        data.winner = data.myID
        data.myturn = False
    while serverMsg.qsize() > 0:
        msg = serverMsg.get(False)
        try:
            print("received: ", msg, "\n")
            msg = msg.split()
            command = msg[0]

            if command == "inputName":
                playerID = msg[1]
                playerName = msg[2]
                playerState = data.others[playerID][1]
                data.others[playerID] = (playerName, playerState)

            if command == "myIDis":
                data.myID = msg[1]

            if command == "newPlayer":
                playerID = msg[1]
                data.others[playerID] = ("", "B")
                data.players += 1

            if command == "gameStarted":
                if data.state != 1:
                    playerID = msg[1]
                    data.myturn = False
                    deckstring = msg[2:]
                    data.deck = makeDeckfromString(deckstring)
                    data.gameStart = True
                    data.hands = dealCards(data.deck, 1, data.numCards)[0]
                    data.handsImgs = createHandImage(data)

            if command == "mufflis":
                data.mufflisGame = True
                if data.state != 1:
                    playerID = msg[1]
                    data.myturn = False
                    deckstring = msg[2:]
                    data.deck = makeDeckfromString(deckstring)
                    data.gameStart = True
                    data.hands = dealCards(data.deck, 1, data.numCards)[0]
                    data.handsImgs = createHandImage(data)



            if command == "quitGame":
                playerID = msg[1]
                del data.others[playerID]

            if command == "fold":
                playerID = msg[1]
                playerState = "F"
                playerName = data.others[playerID][0]
                data.others[playerID] = (playerName, playerState)
                if checkTurn(data, playerID):
                    data.myturn = True

            if command == "bet":
                playerID = msg[1]
                data.pot = int(msg[2])
                data.Cbet = int(msg[3])
                if checkTurn(data, playerID):
                    data.myturn = True

            if command == "raise":
                playerID = msg[1]
                data.pot = int(msg[2])
                data.Cbet = int(msg[3])
                if checkTurn(data, playerID):
                    data.myturn = True

            if command == "cardSeen":
                playerID = msg[1]
                playerState = "S"
                playerName = data.others[playerID][0]
                data.others[playerID] = (playerName, playerState)

            if command == "winner":
                data.winner = msg[2]
                data.state = 5
                playerID = msg[1]
                data.pot = int(msg[3])
                if data.winner == data.myID:
                    data.wins += 1
                    data.chips += data.pot

            if command == "askShow":
                playerID = msg[1]
                data.pot = int(msg[2])
                if not data.fold:
                    handstring = msg[3:]
                    oppHand = makeShowHandfromString(handstring)
                    if data.mufflisGame:
                        winner = compareMufflis(data.hands, oppHand)
                    else:
                        winner = compareHands(data.hands, oppHand)
                    if winner == data.hands:
                        data.winner = data.myID
                        data.chips += data.pot
                        data.wins += 1
                    else:
                        data.winner = playerID
                        data.fold = True

            if command == "sideShow":
                playerID = msg[1]
                showID = msg[2]
                data.pot = int(msg[3])
                if data.myID == showID:
                    handstring = msg[4:]
                    oppHand = makeShowHandfromString(handstring)
                    if data.mufflisGame:
                        winner = compareMufflis(data.hands, oppHand)
                    else:
                        winner = compareHands(data.hands, oppHand)
                    if winner == data.hands:
                        data.sideShowWinner = data.myID
                        data.sideShowLoser = playerID
                        data.myturn = True
                    else:
                        data.fold = True
                        data.myturn = False
                        data.skip = True
                        data.sideShowWinner = playerID
                        data.sideShowLoser = data.myID

            if command == "sideshowComplete":
                playerID = msg[1]
                winner = msg[2]
                loser = msg[3]
                data.sideShowWinner = winner
                data.sideShowLoser = loser
                if loser == data.myID:
                    data.fold = True
                    data.myturn = False
                    data.skip = True
                else:
                    playerState = "F"
                    playerName = data.others[loser][0]
                    data.others[loser] = (playerName, playerState)
                mynum = int(data.myID[-1])
                prevID = "Player" + str(mynum - 1)
                if winner == data.myID:
                    data.myturn = False
                elif prevID == winner:
                    data.myturn = False
                elif prevID == loser:
                    data.myturn = True

            if command == "sideshowOver":
                playerID = msg[1]
                data.sideShowWinner = None
                data.sideShowLoser = None

            if command == "newGame":
                playerID = msg[1]
                mynum = int(data.myID[-1])
                turn = int(msg[2])
                if turn == mynum:
                    data.myturn = True
                handstring = msg[3:]
                hands = makeNewHandsfromString(handstring)
                data.hands = hands[mynum - 1]
                data.handsImgs = createHandImage(data)
                data.state = 1
                data.pot = 0
                data.winner = None
                data.round += 1
                data.blind = True
                data.skip = False
                data.fold = False
                data.Cbet = 2
                playerState = "B"
                for ID in data.others:
                    playerName = data.others[ID][0]
                    data.others[ID] = (playerName, playerState)
        except:
            print ("failed")
        serverMsg.task_done()

def makeDeckfromString(deckstring):
    c1 = deckstring[0]
    c1 = c1[1:]
    deckstring[0] = c1
    decklist = stringToCards(deckstring)
    return decklist

def makeShowHandfromString(handstring):
    c1 = handstring[0]
    c1 = c1[1:]
    handstring[0] = c1
    handlist = stringToCards(handstring)
    hand = set(handlist)
    return hand

def makeNewHandsfromString(handstring):
    c1 = handstring[0]
    c1 = c1[1:]
    handstring[0] = c1
    ce = handstring[-1]
    ce = ce[:-1]
    handstring[-1] = ce
    final = []
    for i in range(0, len(handstring), 3):
        hand = handstring[i:i+3]
        a = hand[0]
        if a[0] == "{":
            a = a[1:]
        hand[0] = a
        b = hand[-1]
        if b[-1] == ",":
            b = b[:-1]
        hand[-1] = b
        handlist = stringToCards(hand)
        handset = set(handlist)
        final.append(handset)
    return final

def stringToCards(deckstring):
    final = []
    for c in deckstring:
        c = c[:-1]
        if c == "AceofSpades":
            r = 1
            s = 1
        elif c == "AceofHearts":
            r = 1
            s = 2
        elif c == "AceofDiamonds":
            r = 1
            s = 3
        elif c == "AceofClubs":
            r = 1
            s = 4
        elif c == "2ofSpades":
            r = 2
            s = 1
        elif c == "2ofHearts":
            r = 2
            s = 2
        elif c == "2ofDiamonds":
            r = 2
            s = 3
        elif c == "2ofClubs":
            r = 2
            s = 4
        elif c == "3ofSpades":
            r = 3
            s = 1
        elif c == "3ofHearts":
            r = 3
            s = 2
        elif c == "3ofDiamonds":
            r = 3
            s = 3
        elif c == "3ofClubs":
            r = 3
            s = 4
        elif c == "4ofSpades":
            r = 4
            s = 1
        elif c == "4ofHearts":
            r = 4
            s = 2
        elif c == "4ofDiamonds":
            r = 4
            s = 3
        elif c == "4ofClubs":
            r = 4
            s = 4
        elif c == "5ofSpades":
            r = 5
            s = 1
        elif c == "5ofHearts":
            r = 5
            s = 2
        elif c == "5ofDiamonds":
            r = 5
            s = 3
        elif c == "5ofClubs":
            r = 5
            s = 4
        elif c == "6ofSpades":
            r = 6
            s = 1
        elif c == "6ofHearts":
            r = 6
            s = 2
        elif c == "6ofDiamonds":
            r = 6
            s = 3
        elif c == "6ofClubs":
            r = 6
            s = 4
        elif c == "7ofSpades":
            r = 7
            s = 1
        elif c == "7ofHearts":
            r = 7
            s = 2
        elif c == "7ofDiamonds":
            r = 7
            s = 3
        elif c == "7ofClubs":
            r = 7
            s = 4
        elif c == "8ofSpades":
            r = 8
            s = 1
        elif c == "8ofHearts":
            r = 8
            s = 2
        elif c == "8ofDiamonds":
            r = 8
            s = 3
        elif c == "8ofClubs":
            r = 8
            s = 4
        elif c == "9ofSpades":
            r = 9
            s = 1
        elif c == "9ofHearts":
            r = 9
            s = 2
        elif c == "9ofDiamonds":
            r = 9
            s = 3
        elif c == "9ofClubs":
            r = 9
            s = 4
        elif c == "10ofSpades":
            r = 10
            s = 1
        elif c == "10ofHearts":
            r = 10
            s = 2
        elif c == "10ofDiamonds":
            r = 10
            s = 3
        elif c == "10ofClubs":
            r = 10
            s = 4
        elif c == "JackofSpades":
            r = 11
            s = 1
        elif c == "JackofHearts":
            r = 11
            s = 2
        elif c == "JackofDiamonds":
            r = 11
            s = 3
        elif c == "JackofClubs":
            r = 11
            s = 4
        elif c == "QueenofSpades":
            r = 12
            s = 1
        elif c == "QueenofHearts":
            r = 12
            s = 2
        elif c == "QueenofDiamonds":
            r = 12
            s = 3
        elif c == "QueenofClubs":
            r = 12
            s = 4
        elif c == "KingofSpades":
            r = 13
            s = 1
        elif c == "KingofHearts":
            r = 13
            s = 2
        elif c == "KingofDiamonds":
            r = 13
            s = 3
        elif c == "KingofClubs":
            r = 13
            s = 4
        a = PlayingCard(r, s)
        final.append(a)
    return final

def checkTurn(data, playerID):
    mynum = int(data.myID[-1])
    pID = int(playerID[-1])
    if pID == data.players and mynum == 1:
        return True
    if mynum == pID + 1:
        return True
    return False

#CITED -- "http://whitelabel.marketjs.com"
def drawBoard(canvas, data):
    canvas.create_rectangle((0,0), (data.width, data.height), fill = "black")
    canvas.create_image(data.width/2, data.height/2, image = data.board)
    pottext = "Pot: " + str(data.pot)
    canvas.create_text(data.width/2, data.height/2, text = pottext,
                            font = ("Times" + " 40 " + "bold"))

def drawMyhand(canvas, data):
    xc = data.width/2
    yc = 2*data.height/3
    size = 30
    if data.blind:
        c1, c2, c3 = data.cardBack, data.cardBack, data.cardBack
    else:
        c1, c2, c3 = data.handsImgs
        drawmyHandValue(canvas, data)
    canvas.create_image(xc - size, yc, image = c1)
    canvas.create_image(xc, yc, image = c2)
    canvas.create_image(xc + size, yc, image = c3)

def drawTopText(canvas, data):
    if data.myturn:
        txt = "It's Your Turn"
    else:
        txt = ""
    canvas.create_text(data.width/2, data.height/14, text = txt,
                        font = ("ComicSansMS" + " 40 " + "bold"), fill = "gold")

def drawPlayerInfo(canvas, data):
    if data.name != None:
        txt1 = "Name: " + data.name
    else:
        txt1 = "Name: " + " "
    canvas.create_text(5*data.width/6, data.height/14, text = txt1, anchor = NW,
                        font = ("Times" + " 15 " + "bold"), fill = "white")
    txt2 = "Chips: " + str(data.chips)
    canvas.create_text(5*data.width/6, data.height/7, text = txt2, anchor = NW,
                        font = ("Times" + " 15 " + "bold"), fill = "white")
    txt3 = "Buy-In: " + str(data.buyin)
    canvas.create_text(5*data.width/6,3*data.height/14,text = txt3, anchor = NW,
                        font = ("Times" + " 15 " + "bold"), fill = "white")
    txt4 = "Wins: " + str(data.wins)
    canvas.create_text(data.width/6, data.height/7, text = txt4, anchor = NE,
                        font = ("Times" + " 25 " + "bold"), fill = "white")

def drawmyHandValue(canvas, data):
    userhand = data.hands
    value = handValue(userhand)[0]
    txt = "You have a " + value
    canvas.create_text(data.width/2, data.height/7, text = txt,
                        font = ("ComicSansMS" + " 30 " + "bold"), fill = "gold")

def drawWinner(canvas, data):
    canvas.create_rectangle((0, data.height/3), (data.width, 2*data.height/3),
                            fill = "black")
    txt = "We have a Winner!"
    canvas.create_text(data.width/2, 1.5*data.height/3, text = txt,
                        font = ("ComicSansMS" + " 40 " + "bold"), fill = "gold")
    texts = "Press Enter to continue"
    canvas.create_text(data.width/2, 2*data.height/3 - 30, text = texts,
                        font = ("ComicSansMS" + " 25 " + "bold"), fill = "gold")

def drawSideShow(canvas, data):
    canvas.create_rectangle((0, data.height/3), (data.width, 2*data.height/3),
                            fill = "black")
    txt = data.sideShowWinner + " has won the sideshow with " + \
                                                        data.sideShowLoser
    canvas.create_text(data.width/2, 1.5*data.height/3, text = txt,
                        font = ("ComicSansMS" + " 40 " + "bold"), fill = "gold")
    texts = "Press Enter and then Space to continue"
    canvas.create_text(data.width/2, 2*data.height/3 - 30, text = texts,
                        font = ("ComicSansMS" + " 25 " + "bold"), fill = "gold")

def drawOthersHands(canvas, data):
    if data.players == 2:
        c1, c2, c3 = data.cardBack, data.cardBack, data.cardBack
        xc = data.width/2
        yc = data.height/3
        size = 30
        canvas.create_image(xc - size, yc, image = c1)
        canvas.create_image(xc, yc, image = c2)
        canvas.create_image(xc + size, yc, image = c3)
    if data.players == 3:
        c1, c2, c3 = data.cardBack, data.cardBack, data.cardBack
        xc = data.width/3
        yc = data.height/3
        size = 30
        canvas.create_image(xc - size, yc, image = c1)
        canvas.create_image(xc, yc, image = c2)
        canvas.create_image(xc + size, yc, image = c3)
        Xc = 2*xc
        canvas.create_image(Xc - size, yc, image = c1)
        canvas.create_image(Xc, yc, image = c2)
        canvas.create_image(Xc + size, yc, image = c3)
    if data.players == 4:
        c1, c2, c3 = data.cardBack, data.cardBack, data.cardBack
        xc = data.width/2
        yc = data.height/3
        size = 30
        canvas.create_image(xc - size, yc, image = c1)
        canvas.create_image(xc, yc, image = c2)
        canvas.create_image(xc + size, yc, image = c3)
        c4, c5, c6 = data.backflat, data.backflat, data.backflat
        Xc = data.width/6
        Yc = data.height/2
        canvas.create_image(Xc, Yc - size, image = c4)
        canvas.create_image(Xc, Yc, image = c5)
        canvas.create_image(Xc, Yc + size, image = c6)
        XC = 5*Xc
        canvas.create_image(XC, Yc - size, image = c4)
        canvas.create_image(XC, Yc, image = c5)
        canvas.create_image(XC, Yc + size, image = c6)
    if data.players == 5:
        c1, c2, c3 = data.cardBack, data.cardBack, data.cardBack
        xc = data.width/3
        yc = data.height/3
        size = 30
        canvas.create_image(xc - size, yc, image = c1)
        canvas.create_image(xc, yc, image = c2)
        canvas.create_image(xc + size, yc, image = c3)
        Xc = 2*xc
        canvas.create_image(Xc - size, yc, image = c1)
        canvas.create_image(Xc, yc, image = c2)
        canvas.create_image(Xc + size, yc, image = c3)
        c4, c5, c6 = data.backflat, data.backflat, data.backflat
        Xc = data.width/6
        Yc = data.height/2
        canvas.create_image(Xc, Yc - size, image = c4)
        canvas.create_image(Xc, Yc, image = c5)
        canvas.create_image(Xc, Yc + size, image = c6)
        XC = 5*Xc
        canvas.create_image(XC, Yc - size, image = c4)
        canvas.create_image(XC, Yc, image = c5)
        canvas.create_image(XC, Yc + size, image = c6)

def drawWinScreen(canvas, data):
    colors = ["yellow", "pink", "hot pink", "white", "cyan", "bisque", "azure"]
    index = random.randint(0, 6)
    color = colors[index]
    canvas.create_rectangle((0,0), (data.width, data.height), fill = color)
    if data.winner == data.myID:
        if data.name == None:
            name = ""
        else:
            name = data.name
    else:
        name = data.others[data.winner][0]
    txt = "Winner is " + data.winner + "(" + name + ")"
    canvas.create_text(data.width/2, data.height/2, text = txt,
                    font = ("ComicSansMS" + " 60 " + "bold"), fill = "black")

def drawHomeScreen(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image = data.redback)
    canvas.create_image(data.width/2, 3*data.height/8, image = data.home)
    canvas.create_image(data.width/4, 7*data.height/8, image = data.play)
    canvas.create_image(3*data.width/4, 7*data.height/8, image = data.instrct)

def createSampleHands(data):
    final = []
    c1, c2, c3 = PlayingCard(1,1), PlayingCard(1,2), PlayingCard(1,3)
    a1 = c1.drawMe()
    a2 = c2.drawMe()
    a3 = c3.drawMe()
    final.append((a1, a2, a3))
    c4, c5, c6 = PlayingCard(1,1), PlayingCard(13,1), PlayingCard(12,1)
    a4, a5, a6 = c4.drawMe(), c5.drawMe(), c6.drawMe()
    final.append((a4, a5, a6))
    d1, d2, d3 = PlayingCard(5,2), PlayingCard(6,1), PlayingCard(7,4)
    e1, e2, e3 = d1.drawMe(), d2.drawMe(), d3.drawMe()
    final.append((e1, e2, e3))
    c1, c2, c3 = PlayingCard(2,4), PlayingCard(7,4), PlayingCard(11,4)
    e1, e2, e3 = c1.drawMe(), c2.drawMe(), c3.drawMe()
    final.append((e1, e2, e3))
    c1, c2, c3 = PlayingCard(10,3), PlayingCard(10,2), PlayingCard(2,1)
    e1, e2, e3 = c1.drawMe(), c2.drawMe(), c3.drawMe()
    final.append((e1, e2, e3))
    c1, c2, c3 = PlayingCard(1,3), PlayingCard(13,2), PlayingCard(2,1)
    e1, e2, e3 = c1.drawMe(), c2.drawMe(), c3.drawMe()
    final.append((e1, e2, e3))
    return final

def drawInstruction(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image = data.redback)
    canvas.create_image(data.width/2, data.height/8, image = data.intro)
    a1, a2, a3 = data.samplehands[0]
    size = 30
    y1 = 2.5*data.height/8
    canvas.create_image(data.width/4 - size, y1, image = a3)
    canvas.create_image(data.width/4, y1, image = a2)
    canvas.create_image(data.width/4 + size, y1, image = a1)
    canvas.create_image(data.width/4, 3*data.height/8 + 40,
                                                        image = data.trailimg)
    b1, b2, b3 = data.samplehands[1]
    canvas.create_image(data.width/2 - size, y1, image = b1)
    canvas.create_image(data.width/2, y1, image = b2)
    canvas.create_image(data.width/2 + size, y1, image = b3)
    canvas.create_image(data.width/2 + 15, 3*data.height/8 + 40,
                                                        image = data.pureseqimg)
    c1, c2, c3 = data.samplehands[2]
    canvas.create_image(3*data.width/4 - size, y1, image = c1)
    canvas.create_image(3*data.width/4, y1, image = c2)
    canvas.create_image(3*data.width/4 + size, y1, image = c3)
    canvas.create_image(3*data.width/4, 3*data.height/8 + 40,
                                                        image = data.seqimg)
    q1, q2, q3 = data.samplehands[3]
    x1 = data.width/4
    y2 = 5*data.height/8
    canvas.create_image(x1 - size, y2, image = q1)
    canvas.create_image(x1, y2, image = q2)
    canvas.create_image(x1 + size, y2, image = q3)
    canvas.create_image(x1 + 15, 5*data.height/8 + 80, image = data.colorimg)
    s1, s2, s3 = data.samplehands[4]
    x2 = 2*x1
    canvas.create_image(x2 - size, y2, image = s1)
    canvas.create_image(x2, y2, image = s2)
    canvas.create_image(x2 + size, y2, image = s3)
    canvas.create_image(x2 + 15, 5*data.height/8 + 80, image = data.pairimg)
    x3 = 3*x1
    r1, r2, r3 = data.samplehands[5]
    canvas.create_image(x3 - size, y2, image = r1)
    canvas.create_image(x3, y2, image = r2)
    canvas.create_image(x3 + size, y2, image = r3)
    canvas.create_image(x3 + 15, 5*data.height/8 + 80, image = data.highimg)
    canvas.create_image(data.width/2, 7*data.height/8, image = data.bestxt)

def drawOptionsPage(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image = data.redback)
    canvas.create_image(data.width/2, data.height/2, image = data.aceback)
    canvas.create_image(data.width/2, data.height/4, image = data.nameImg)
    if data.clickName:
        x0, x1 = data.width/2 - 292/2, data.width/2 + 292/2
        y0, y1 = data.height/4 - 81/2, data.height/4 + 81/2
        canvas.create_rectangle((x0,y0), (x1,y1), fill = "white", outline =
                                                                        "black")
        canvas.create_text(data.width/2, data.height/4, text = data.name,
                            font = ("ComicSansMS" + " 50 " + "bold"))
    canvas.create_image(data.width/2, data.height/2, image = data.multi)
    canvas.create_image(data.width/2, 3*data.height/4, image = data.mufflis)

def drawPossibleMoves(canvas, data):
    if not data.fold:
        y = 7*data.height/8
        x = data.width/5
        canvas.create_image(x, y, image = data.foldImg)
        canvas.create_image(2*x, y, image = data.betImg)
        canvas.create_image(3*x, y, image = data.raiseImg)
        if data.blind:
            canvas.create_image(4*x, 5*data.height/6, image = data.seecards)
        else:
            typeShow = checkTypeShow(data)
            if typeShow != None:
                if typeShow[0] == "show":
                    img = data.showImg
                    canvas.create_image(4*x, 5.5*data.height/6, image = img)
                elif typeShow[0] == "sideShow":
                    img = data.sideshowImg
                    canvas.create_image(4*x, 5.5*data.height/6, image = img)

def checkTypeShow(data):
    playerRemain = 0
    allSeen = True
    num = int(data.myID[-1])
    for ID in data.others:
        info = data.others[ID]
        state = info[1]
        if state == "F":
            continue
        elif state == "B":
            allSeen = False
        playerRemain += 1
    if playerRemain == 1 and allSeen:
        for ID in data.others:
            info = data.others[ID]
            state = info[1]
            if state == "S":
                return ("show", ID)
    if playerRemain > 1 and allSeen:
        for ID in data.others:
            info = data.others[ID]
            state = info[1]
            if state == "F" or state == "B":
                continue
            elif state == "S":
                return ("sideShow", ID)
    return None




def redrawAll(canvas, data):
    if data.state == 0:
        drawHomeScreen(canvas, data)


    if data.state == 1:
        drawBoard(canvas, data)
        drawMyhand(canvas, data)
        drawTopText(canvas, data)
        drawOthersHands(canvas, data)
        drawPlayerInfo(canvas, data)
        if data.winner == None:
            drawPossibleMoves(canvas, data)
        else:
            drawWinner(canvas, data)
        if data.sideShowWinner != None:
            drawSideShow(canvas, data)

    if data.state == 2:
        drawInstruction(canvas, data)

    if data.state == 3:
        drawOptionsPage(canvas, data)

    if data.state == 5:
        drawWinScreen(canvas, data)






#CITED -- 112 website
def run(width=300, height=300, serverMsg=None, server=None):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        # canvas.create_rectangle(0, 0, data.width, data.height,
        #                         fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.server = s
    data.serverMsg = serverMsg
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

playTeenPatti()
