Project: Teen Patti (3-card Poker)

Teen Patti is a card game widely popular in India, and in casinos it’s called 3-card Poker. The game is based on a betting-based gameplay. My project will create a user interface, that will allow a player to play teen patti with other players. For this I will use the sockets module. I will also implement AI, so that the game can be played single player, or alongside a computer. The game is dependent on variations, without which the game becomes monotonous. And so once, the basic gameplay of standard teen patti is implemented, I will also add variations to it.

The Game:
•	Card game, 1 deck, multiplayer
•	Based on betting
•	3 cards (called a hand), best hand wins, or win if everyone else packs (folds)
•	No flop or common cards.
•	Bet increases only in doubles, for example If I bet $10, the next person can either bet $10, or min/max $20, nothing else is allowed.
•	Option of playing blind, so you don't see your cards, and you bet half the amount a seen player bets. (+EV in specific variations of the game, and sometimes if the hand began with a lot of people, and only 1 remains). Also responsible for causing some sick moments in the game.

To run the project, you need python3, with all the modules that should already
be there. We need tkinter, sockets, threading and queue.
First run the file tp_server.py, to estabilish the host and then run upto 5
version of tp_client.py on separate terminals.

There arent too many shortcuts, however, pressing "e", "b", or "backspace"/"delete"
will almost always take you back to the homescreen.  
