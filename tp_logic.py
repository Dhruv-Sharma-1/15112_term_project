import math
from tp_cards import *


def handValue(hand):
    c1, c2, c3 = hand
    if checkTrail(c1, c2, c3):
        return ("Trail", 5)
    elif checkPureSequence(c1, c2, c3):
        return ("Pure Sequence", 4)
    elif checkSequence(c1, c2, c3):
        return ("Sequence", 3)
    elif checkColor(c1, c2, c3):
        return ("Color", 2)
    elif checkPair(c1, c2, c3):
        return ("Pair", 1)
    else:
        return ("High Card", 0)

def compareHands(h1, h2):
    value1 = handValue(h1)[1]
    value2 = handValue(h2)[1]
    if value1 > value2:
        return h1
    elif value2 > value1:
        return h2
    elif value1 == 5 and h1.pop().value == 14:
        return 0
    else:
        return compareHighCards(h1, h2)

def compareMufflis(h1, h2):
    value1 = handValue(h1)[1]
    value2 = handValue(h2)[1]
    if value2 < value1:
        return h2
    elif value1 < value2:
        return h2
    elif value1 == 5 and h1.pop().value == 14:
        return 0
    else:
        f = compareHighCards(h1, h2)
        if f == h2:
            return h1
        else:
            return h2

def compareHighCards(h1, h2):
    hi1 = highestCard(h1)
    hi2 = highestCard(h2)
    if hi1 > hi2:
        return h1
    elif hi2 > hi1:
        return h2
    else:
        lo1 = lowestCard(h1)
        lo2 = lowestCard(h2)
        for c in h1:
            if c.rank != hi1 and c.rank != lo1:
                mid1 = c.rank
        for c in h2:
            if c.rank != hi2 and c.rank != lo2:
                mid2 = c.rank
        if mid1 > mid2:
            return h1
        elif mid2 > mid1:
            return h2
        else:
            if lo1 > lo2:
                return h1
            elif lo2 > lo1:
                return h2
            else:
                return h2

def highestCard(hand):
    c1, c2, c3 = hand
    max1 = max(c1.value, c2.value)
    return max(max1, c3.value)

def lowestCard(hand):
    c1, c2, c3 = hand
    min1 = min(c1.value, c2.value)
    return min(min1, c3.value)

def checkPair(c1, c2, c3):
    if c1.rank == c2.rank == c3.rank:
        return False
    elif c1.rank != c2.rank and c1.rank != c3.rank and c2.rank != c3.rank:
        return False
    return True

def checkColor(c1, c2, c3):
    if c1.suit == c2.suit == c3.suit:
        return True
    return False

def checkTrail(c1, c2, c3):
    if c1.rank == c2.rank == c3.rank:
        return True
    else:
        return False

def checkSequence(c1, c2, c3):
    low = lowestCard((c1, c2, c3))
    hi = highestCard((c1, c2, c3))
    if hi == 14 and low == 2:
        if c1.rank == 3 or c2.rank == 3 or c3.rank == 3:
            return True
    if low == hi or low + 1 != hi - 1:
        return False
    mid = low + 1
    if c1.value == mid or c2.value == mid or c3.value == mid:
        return True
    return False

def checkPureSequence(c1, c2, c3):
    if checkColor(c1, c2, c3) and checkSequence(c1, c2, c3):
        return True
    return False



# deck = createDeck()
# hands = dealCards(deck, 2, 3)
# h1, h2 = hands[0], hands[1]
# print (h1, h2)
# winner = compareHands(h1, h2)
# print (handValue(winner)[0], winner)
