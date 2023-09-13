
#hello this is a game, gamers
import random
'''

game info -> bot -> turn


'''
class Game:
    #keeps track of the state of the game
    hands = [] #every person's hand, array of arrays
    turn = 0 #who's turn is it, players 0,1,2,3
    first_turn = True #is this the first turn
    current_play = None #quantity,card
    current_leader = None # the last person who played a card
    ranking = []

    def __init__(self):
        deck = [*range(52)] #create array with 4 sets of 12 cards
        random.shuffle(deck) #shuffles array
        self.hands.append(deck[:13])
        self.hands.append(deck[13:26])
        self.hands.append(deck[26:39])
        self.hands.append(deck[39:])

        #check who has 0 AKA 3 of clubs and assign the first player
        for player in range(len(self.hands)):
            if self.hands[player].count(0) > 0:
                self.turn = player
            self.hands[player] = [card % 13 for card in self.hands[player]] #turning all the card values readable
            self.hands[player].sort()

        print(f'\nIt\'s player {self.turn}\'s turn!')
        self.print_hand()
        
        
    def take_turn(self,quantity,card): #take a turn, for one player. returns (valid move, game over)
        if not self.validate_turn(quantity, card):
            return (False, False)
        #quantity is number of cards and cards is the value, so two kings would be (2,10)
        if quantity != 0:
            self.current_play = (quantity,card)
            for x in range(quantity): 
                self.hands[self.turn].remove(card)
            if len(self.hands[self.turn]) == 0:
                self.ranking.append(self.turn)
            self.current_leader = self.turn
        self.turn = (self.turn + 1)%4

        if self.turn == self.current_leader:
            self.current_play = None
            self.current_leader = None
        i = 0
        while len(self.hands[self.turn]) == 0:
            self.turn = (self.turn + 1)%4
            if self.turn == self.current_leader:
                self.current_play = None
                self.current_leader = None
            i += 1 
            if i > 3:
                print(f'\nGame over!\n The rankings are {self.ranking}')
                return (True, True)
        self.first_turn = False
        print(f'\nIt\'s player {self.turn}\'s turn!')
        self.print_hand()
        print(self.current_play)
        return (True, False)
    
    def validate_turn(self,quantity,card):
        #bot puts in a turn and then we check it is valid. return true or false
        if quantity == 0:
            return (not self.first_turn)
        if self.first_turn and card != 0:
            return False #you have to play 3 on the first turn
        if self.hands[self.turn].count(card) < quantity:
            return False #you have to have enough cards in your deck!
        if self.current_play != None and quantity != self.current_play[0]:
            return False #you have to play the same quantity as the previous player
        if self.current_play != None and card <= self.current_play[1]:
            return False #your card must be higher than the previous turn
        return True

    def random_move(self):
        (valid, _) = self.take_turn(1, self.hands[self.turn][0])
        if not valid:
            self.take_turn(0,0)

    def print_hand(self):
        output = []
        for card in self.hands[self.turn]:
            if card < 8:
                output.append(str(card+3))
            elif card == 8:
                output.append('J')
            elif card == 9:
                output.append('Q')
            elif card == 10:
                output.append('K')
            elif card == 11:
                output.append('A')
            elif card == 12:
                output.append('2')
        print(output)

    def generate_backup_move(self):
        if self.first_turn:
            return (1,0)
        return (0,0)
