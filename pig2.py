__author__ = 'T Jeremiah October 2015 - Assignment 8'

import random,time,argparse

parser = argparse.ArgumentParser(description='Play Pig - 1 Player or 2 Player')
parser.add_argument("--player1", type=str, help="Player1 'human' or 'computer'?")
parser.add_argument("--player2", type=str, help="Player2 'human' or 'computer'?")
parser.add_argument("--timed", help="Timed Game?")
args = parser.parse_args()

if not args.player1:
    player1type = 'human'
else:
    player1type = args.player1

if not args.player2:
    player2type = 'human'
else:
    player2type = args.player2


class Player():
    def __init__(self):
        self.turn = False
        self.roll = True
        self.hold = False
        self.score = 0
        self.turn_score = 0

    def decide(self):
        decision = raw_input('%s: Hold (h) or Roll (r)?' % self.name)
        decision = str(decision)
        if decision == 'h':
            self.hold = True
            self.roll = False
        elif decision == 'r':
            self.hold = False
            self.roll = True
        else:
            print('Wrong input.  Please enter h or r')
            self.decide()


class ComputerPlayer(Player):
    def decide(self):
        limit1 = 25
        limit2 = 100 - self.score
        if (limit1 < limit2):
            holdlimit = limit1
        else:
            holdlimit = limit2

        if (self.turn_score < holdlimit):
            print "Computer Rolling"
            self.hold = False
            self.roll = True
        else:
            print "Computer Holding"
            self.hold = True
            self.roll = False


class PlayerFactory():
    def __init__(self):
        return None

    def makeplayer(self, playertype):
        if playertype == 'human':
            return Player()
        elif playertype == 'computer':
            return ComputerPlayer()
        else:
            print "Unknown Player Type"


class Die():
    def __init__(self):
        self.value = int()
        seed = 0

    def roll(self):
        self.value = random.randint(1, 6)


class Game():
    def __init__(self, player1, player2, die):
        self.turn_score = 0
        self.die = die
        self.player1 = player1
        self.player2 = player2
        self.player1.score = 0
        self.player2.score = 0
        self.player1.turn_score = self.turn_score
        self.player2.turn_score = self.turn_score
        self.player1.name = "Player 1"
        self.player2.name = "Player 2"

        coin_flip = random.randint(1, 2)
        if coin_flip == 1:
            self.current_player = player1
            print "Player one has won. Will start first"
        elif coin_flip == 2:
            self.current_player = player2
            print "Player two has won. Will start first"
        else:
            print "Coin Flip Error. TRY AGAIN"
        self.turn()

    def turn(self):
        print "Player 1 Score:", self.player1.score
        print "Player 2 Score:", self.player2.score
        self.die.roll()
        if (self.die.value == 1):
            print "You Rolled a 1! No Points for You!"
            self.next_turn()
        else:
            self.turn_score = self.turn_score + self.die.value
            self.player1.turn_score = self.turn_score
            self.player2.turn_score = self.turn_score
            print "You rolled a:", self.die.value
            print "Current Value is:", self.turn_score
            self.current_player.decide()
            if (self.current_player.hold == True and self.current_player.roll == False):
                self.current_player.score = self.current_player.score + self.turn_score
                self.next_turn()
            elif (self.current_player.hold == False and self.current_player.roll == True):
                self.turn()

    def next_turn(self):
        self.turn_score = 0

        if self.player1.score >= 100:
            print "Player 1 has won the game!"
            print "Score:", self.player1.score
            self.endgame()
            startNewGame()
        elif self.player2.score >= 100:
            print "Player 2 has won the game!"
            print "Score:", self.player2.score
            self.endgame()
            startNewGame()
        else:
            if self.current_player == self.player1:
                self.current_player = self.player2
            elif self.current_player == self.player2:
                self.current_player = self.player1
            else:
                print "Next Turn Error, current_player neither Player 1 or Player 2"

            print "New Turn, player is now:", self.current_player.name
            self.turn()

    def endgame(self):
        self.player1 = None
        self.player2 = None
        self.die = None
        self.turn_score = None


class TimedGameProxy(Game):
    def __init__(self, player1, player2, die):
        self.start_time = time.time()
        self.turn_score = 0
        self.die = die
        self.player1 = player1
        self.player2 = player2
        self.player1.score = 0
        self.player2.score = 0
        self.player1.turn_score = self.turn_score
        self.player2.turn_score = self.turn_score
        self.player1.name = "Player 1"
        self.player2.name = "Player 2"

        coin_flip = random.randint(1, 2)
        if coin_flip == 1:
            self.current_player = player1
            print "Player 1 has won the Coin Flip, will start first"
        elif coin_flip == 2:
            self.current_player = player2
            print "Player 2 has won the Coin Flip, will start first"
        else:
            print "Coin Flip Error, not heads or tails"
        self.turn()

    def next_turn(self):

        self.turn_score = 0

        if self.player1.score >= 100:
            print "Player 1 has won the game!"
            print "Score:", self.player1.score
            self.endgame()
            startNewGame()
        elif self.player2.score >= 100:
            print "Player 2 has won the game!"
            print "Score:", self.player2.score
            self.endgame()
            startNewGame()
        else:
            if self.current_player == self.player1:
                self.current_player = self.player2
            elif self.current_player == self.player2:
                self.current_player = self.player1
            else:
                print "Next Turn Error, current_player neither Player 1 or Player 2"

            print "New Turn, player is now:", self.current_player.name
            self.turn()

    def declareEnd(self):
        print "Time is Up!"
        print "Player 1 Score:", self.player1.score
        print "Player 2 Score:", self.player2.score
        if self.player1.score > self.player2.score:
            print "Player 1 Wins!"
            self.endgame()
        elif self.player2.score > self.player1.score:
            print "Player 2 Wins!"
            self.endgame()
            startNewGame()
        else:
            print "Tie Game!"
            self.endgame()
            startNewGame()

    def turn(self):
        self.current_time = time.time()
        if (self.current_time - self.start_time >= 60):
            self.declareEnd()
        else:
            print "Player 1 Score:", self.player1.score
            print "Player 2 Score:", self.player2.score
            self.die.roll()
            if (self.die.value == 1):
                print "You Rolled a 1! No Points for You!"
                # self.turn_score = 0
                # self.player1.turn_score = self.turn_score
                # self.player2.turn_score = self.turn_score
                self.next_turn()
            else:
                self.turn_score = self.turn_score + self.die.value
                self.player1.turn_score = self.turn_score
                self.player2.turn_score = self.turn_score
                print "You rolled a:", self.die.value
                print "Current Value is:", self.turn_score
                self.current_player.decide()
                if (self.current_player.hold == True and self.current_player.roll == False):
                    self.current_player.score = self.current_player.score + self.turn_score
                    self.next_turn()
                elif (self.current_player.hold == False and self.current_player.roll == True):
                    self.turn()


def startNewGame():
    start = raw_input("Start New Game? Y/N")

    if start == 'Y' or start == 'y':
        playerFactory = PlayerFactory()
        player1 = playerFactory.makeplayer(player1type)
        player2 = playerFactory.makeplayer(player2type)
        die = Die()

        if not args.timed:
            newgame = Game(player1, player2, die)
        else:
            newgame = TimedGameProxy(player1, player2, die)


startNewGame()
