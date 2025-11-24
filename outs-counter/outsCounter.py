
from ast import keyword
import random

class Game:
    def __init__(self) -> None:
        self.nPlayers = None
        self.dealtHands = []
        self.communityCards = []
        self.createDeck()

    def getSymbol(self,value):
        value = value%13
        match value:
            case 0:
                return 'A'
            
            case 10:
                return 'J'
            case 11:
                return 'Q'
            case 12:
                return 'K'
            
            case _:
                return str(value+1)

    def createDeck(self):
        suits = ['H','D','C','S']
        self.deck = {}

        for suit in suits:
            cards = []
            for value in range(13):
                cards.append(self.getSymbol(value))
            self.deck[suit] = cards

    def printDeck(self):
        for s in self.deck:
            print(f'{s} > {self.deck[s]}')

    def pickCard(self):
        suit = random.choice(list(self.deck.keys()))
        
        while all(item == -1 for item in self.deck[suit]):
            suit = random.choice(list(self.deck.keys()))

        value = -1
        while value==-1:
            value = random.choice(self.deck[suit])
        #remove the chosen card from the game deck
        for k in range(len(self.deck[suit])):
            if self.deck[suit][k] == value:
                self.deck[suit][k] = -1
        card = str(suit)+str(value)
        return card

    def dealHands(self,nPlayers):
        self.nPlayers = nPlayers
        for i in range(nPlayers):
            hand = []
            for j in range(2):
                hand.append(self.pickCard())
            self.dealtHands.append(hand)


    def dealFlop(self):
        for i in range(3):
            self.communityCards.append(self.pickCard())

    def progressGame(self):
        if len(self.communityCards)<3:
            self.dealFlop()

        else:
            self.communityCards.append(self.pickCard())

class handMatcher():
    def __init__(self,flop=None) -> None:
        if flop is not None:
            self.flop = flop
        else:
            self.flop = []


    def fuzzyMatch(self,hand):
        print(f'flop > {self.flop} hand > {hand}')
        self.rankMatch(hand)
        self.suitMatch(hand)

    def rankMatch(self,hand):
    # just setup a simple counter to track the number of similar suits for the flop and the deck
        tracker_dict = {
            'H':0,
            'D':0,
            'S':0,
            'C':0
        }
        for card in (hand+self.flop):
            tracker_dict[card[0]] +=1
        
        

    def suitMatch(self,hand):
        pass


if __name__ == '__main__':
    game = Game()
    matcher = handMatcher()
    game.dealHands(5)
    print(game.dealtHands)
    game.progressGame()
    matcher.flop = game.communityCards[:3]
    matcher.fuzzyMatch(game.dealtHands[0])






    