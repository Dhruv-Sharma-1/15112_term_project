"""
    Term Project: Teen Patti
    Dhruv Sharma
    ds1
    Section G
                """

from tkinter import *
import string
import copy
import random
import math
import time


class PlayingCard():
    valuesSuits = {1: "Spades", 2: "Hearts", 3: "Diamonds", 4: "Clubs"}
    valuesRanks = {1: "Ace", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
    8: "8", 9: "9", 10: "10", 11: "Jack", 12: "Queen", 13: "King"}

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        if rank == 1:
            self.value = 14
        else:
            self.value = rank

    def __repr__(self):
        reprMessage = self.valuesRanks[self.rank] + "of" + \
                                                    self.valuesSuits[self.suit]
        return reprMessage

    def __eq__(self, other):
        if isinstance(other, PlayingCard):
            return (self.rank == other.rank and self.suit == other.suit)

    def __hash__(self):
        return hash((self.rank, self.suit))

    #CITED -- "http://acbl.mybigcommerce.com/52-playing-cards/"
    def drawMe(self):
        cardPath = "term_project/Images/" + \
                        self.__repr__() + ".gif"
        cardImg = PhotoImage(file = cardPath)
        return cardImg

def createDeck():
    deck = [ ]
    for rank in range(13):
        for suit in range(4):
            deck.append(PlayingCard(rank + 1, suit + 1))
    return deck

def shuffleDeck(deck = None):
    if deck == None:
        deck = createDeck()
    return random.shuffle(deck)

def drawCard(deck):
    return deck.pop()

def dealCards(deck, players, numCards):
    playerHand = [ ]
    for i in range(players):
        hand = set()
        for number in range(numCards):
            shuffleDeck(deck)
            card = drawCard(deck)
            hand.add(card)
        playerHand.append(hand)
    return playerHand


c1 = PlayingCard(2, 3)
deck = createDeck()
shuffleDeck(deck)
hands = dealCards(deck, 2, 3)

count = 0
start = time.time()
while True:
    deck = createDeck()
    shuffleDeck(deck)
    hands = dealCards(deck, 2, 3)
    c1, c2, c3 = hands[0]
    if c1.rank == c2.rank == c3.rank:
        end = time.time()
        # print (count, hands, end - start)
        break
    count += 1
