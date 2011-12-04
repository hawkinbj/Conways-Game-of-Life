#-------------------------------------------------------------------------------
# Student Name: Brandon Hawkins/ Assignment: PP #1 / Date: 10/06/2011               
#-------------------------------------------------------------------------------
# Honor Code Statement: I received no assistance on this assignment that         
# violates the ethical guidelines set forth by professor and class syllabus.     
#-------------------------------------------------------------------------------
# References: (list of all resources used)                                       
#-------------------------------------------------------------------------------
# Comments: (a note to the grader as to any problems or uncompleted aspects of   
#            of the assignment)                                                  
#-------------------------------------------------------------------------------
# Pseudocode: (pseudocode representation of implementation algorithm/process) 
# 3 Classes: Deck(object), Hand(Deck), Card(object), DiscardPile(Deck), 
#            and CardGame(object).
#
# Deck needs the following functions:
#    deal()
#    shuffle()
#    add()/remove() cards
#    isEmpty or not()
#
# Card class:
#    need to assign ranks, suits, and point values, can use a map or just lists
#    override __cmp__ to compare by value and (later) suit
#
# Hand class extends Deck:
#    need these additional functions:
#        sum of hand()
#        determine if 3 of a kind()
#        draw()
#        discard()
#        a way to value only same suits() 
#        override __cmp__ to compare by sum of hand()
#
# Game class:
#    maintain current players/hands, games played, turn count
#    various menus (main, stats, inputting player names, winners presentation)
#    play() method - maybe another method for each player to take turns until
#                    winning conditions are satisfied...
#    method to check if anyone has won
#    
# clear_screen()
#-------------------------------------------------------------------------------
# NOTE: width of source code should be < 80 characters to facilitate printing    
#-------------------------------------------------------------------------------

import os
import copy
import random

# Tuples for possible menu raw_input choices
a1 = ("One", "one", "1", 1)
a2 = ("Two", "two", "2", 2)
a3 = ("Three", "three", "3", 3)
a4 = ("Four", "four", "4", 4)

class Card(object):
    """Represents a playing card."""
    RANKS = ["zero", "A", "2", "3", "4", "5", "6", "7", "8",
             "9", "10", "J", "Q", "K"]
    SUITS = ["Diamonds", "Clubs", "Hearts", "Spades"]
 
    def __init__(self, suit=0, rank=0):
        """Initialize Card object"""
        self.rank = rank
        self.suit = suit
        self.value = 0
        # Assign point values.
        if (self.rank == 11 or self.rank == 12 or self.rank == 13):
            self.value = 10
        elif (self.rank == 1):
            self.value = 11
        else:
            self.value = int(self.rank)
          
    def __str__(self):
        """Return string representation of a Card"""
        return (self.RANKS[self.rank] + " of " + self.SUITS[self.suit])
    
    def __cmp__(self, other):
        """Compare to another Card"""
        if self.value < other.value:
            return -1
        if self.value > other.value:
            return 1
        # If values are same, sort by suit
        else:
            if self.suit < other.suit:
                return -1
            if self.suit > other.suit:
                return 1
            return 0

class Deck(object):    
    """Represents a deck of cards."""
    def __init__(self, numOfDecks=1):
        self.cards = []
        self.numOfDecks = numOfDecks
        for numOfDecks in range(self.numOfDecks):
            for i in range(4):
                for j in range(1, 14):
                    self.cards.append(Card(i, j))
            
    def __str__(self):
        """Return a string representation of Deck."""
        result = ""
        for i in range(len(self.cards)):
            result = result + " " + str(self.cards[i]) + "\n"
        return result
    
    def add(self, card):
        """Add a Card to the deck."""
        self.cards.append(card)
                    
    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)
        
    def pop(self):
        """Remove card from top of deck."""
        return self.cards.pop()
          
    def is_empty(self):
        """Return true if deck is empty"""
        if not self.cards:
            return True
        
    def deal(self, numOfCards, game):
        """Deal the number of cards"""
        self.numOfCards = numOfCards
        self.game = game
        # Exit method if all cards are dealt
        if self.is_empty(): 
            return   
        # Deal the specified # of cards 1 at a time to each player
        for i in range(self.numOfCards):
            for player in self.game.players:
                card = self.pop()
                player.add(card)        
        
class Hand(Deck):
    """Represents a hand of cards"""
    def __init__(self, playerName="Default"):
        self.cards = []
        self.name = playerName
        self.gamesWon = 0.0
        self.gamesPlayed = 0.0 
               
    def sum_hand(self):
        """Get current point value of hand"""
        self.sum = 0
        self.values = []
        self.suits = []
        # Non-Ace, 3-of-a-kind = 30 points
        if self.three_of_kind(self.cards):
            return 30
        else: 
            for i in range (len(self.cards)):
                self.values.append(self.cards[i].value)
                # Will get the most common suit if one exists
                self.suit = self.common_suit(self.cards)
                # Get the values of same-suit cards
                if self.cards[i].suit == self.suit:
                    self.suits.append(self.cards[i].value) 
            # Sum values of same suit cards if any cards in suits list  
            if (len(self.suits) > 0):
                return sum(self.suits)
            else:
                # No most common suit so return highest single value
                return max(self.values)        
        
    def common_suit(self, cards):
        """Return most frequent suit if one exists"""
        for i in range(len(cards)):
            for j in range (i + 1, len(cards)):
                if cards[i].suit == cards[j].suit:
                    # There is, tell us which suit
                    return cards[i].suit
        # There isn't. Return empty string
        return ""
    
    def three_of_kind(self, cards):
        """If all cards are equal, three of a kind"""
        if (cards[0].rank == cards[1].rank and cards[1].rank == cards[2].rank
            and cards[0].value != 11):
            return True
        else:
            return False        
    
    def draw(self, game, flag=False):
        """This is the draw phase of a 2-part turn. The other is discard."""
        if not flag:
            clear_screen()
        print("It is " + str(self.name) + 
               "'s " + str(self.get_ordinal(game.count)) + " turn.\n" + 
               "\nYour hand: " + str(self) + "\nHand value: " + 
                str(self.sum_hand()))
        choice = raw_input("\nDiscard pile: [" + 
                            str(game.discard.cards[len(game.discard.cards) - 1]) + 
                            "]\n1) Take from discard\n2) Draw from deck\nEnter " + 
                            "Option: ")
        if choice in a1:
            self.add(game.discard.pop())
        elif choice in a2:
            self.add(game.deck.pop())
        else:
            print ("Please enter a valid selection: ")
            self.draw(game, True)    
    
    def discard(self, game, flag=False):
        """This is the discard phase of a 2-part turn. The other is draw."""
        if not flag:
            clear_screen()
        print("It is still " + str(self.name) + 
              "'s " + str(self.get_ordinal(game.count)) + "  turn.\n\nYour " + 
              "hand:\n" + self.choice_str())
        choice = raw_input("Choose card to discard: ")
        if choice in a1:
            choice = 1
            game.discard.add(self.cards.pop(choice - 1))
        elif choice in a2:
            choice = 2
            game.discard.add(self.cards.pop(choice - 1))
        elif choice in a3:
            choice = 3
            game.discard.add(self.cards.pop(choice - 1))
        elif choice in a4:
            choice = 4
            game.discard.add(self.cards.pop(choice - 1))
        else:
            print ("Please enter a valid selection: ")
            self.discard(game, True)
    
    def win_percent(self):
        """Return this player's winning percentage."""
        if (self.gamesPlayed == 0.0):
            return
        else:
            return ((self.gamesWon / self.gamesPlayed) * 100) 
    
    def get_ordinal(self, num=5):
        """Return ordinal representation of passed int through 4."""
        if num == 1:
            return "1st"  
        elif num == 2:
            return "2nd"
        elif num == 3:
            return "3rd"
        elif num == 4:
            return "4th"
        else:
            return "something's wrong"     
    
    def __str__(self):
        """Return string representation of Hand."""
        result = ""
        for card in self.cards:
            result = result + " [" + str(card) + "]"
        return result
    
    def choice_str(self):
        """Return a different string representation during discard phase."""
        result = ""
        for i in range(1, len(self.cards) + 1):
            result = result + str(i) + ") [" + str(self.cards[i - 1]) + "]\n"
        return result
    
    def __cmp__(self, other):
        """Compare Hand to another Hand."""
        if self.sum_hand() < other.sum_hand():
            return -1
        if self.sum_hand() > other.sum_hand():
            return 1
        else:
            return 0

class DiscardPile(Deck):
    """Represents discard pile."""
    def __init__(self):
        """Initialize DiscardPile"""        
        self.cards = []
        
class CardGame(object):
    """Represents a game of 31"""
    def __init__(self):
        clear_screen()
        # List of current players
        self.players = []
        # List of current winners (if any)
        self.winners = []
        # Dict of past players (if any)
        self.history = {}
        self.discard = DiscardPile()
        self.totalGamesPlayed = 0
        self.count = 0
        self.main_menu()
    
    def main_menu(self, flag=False):
        """Present main menu."""
        if not self.history and flag != True:
            clear_screen()
        print(" == = \"31\" Main Menu ===\n\n" + "1) New Game\t2) " + 
              "Statistics\t3) Exit\n")
        choice = raw_input("Enter Option: ")
        if choice in a1:
            self.num_of_players()
            self.play()
        if choice in a2: 
            self.stats_menu()
        if choice in a3:
            exit
        else:
            print ("Please enter a valid selection: ")
            # Don't clear menu if incorrect user input
            self.main_menu(True)
    
    def num_of_players(self, flag=False):
        """Obtain number of players from user."""
        if not flag:
            clear_screen()
        # Clear list of current players  
        self.players = []  
        # Reset number of players 
        self.numOfPlayers = 0  
        choice = raw_input("How many players? (2 or 3): ")
        if choice in a2:
            self.numOfPlayers = 2
        if choice in a3:
            self.numOfPlayers = 3
        if (self.numOfPlayers == 2 or self.numOfPlayers == 3):
            for i in range(self.numOfPlayers):
                clear_screen()
                self.name = str(raw_input("Enter name of Player" + 
                                          str(i + 1) + ": "))
                # Check if player entered has played previously 
                if self.name in self.history:
                    # If so, put him back in the game...
                    self.players.append(self.history[self.name])
                    # ...and remove from dict (will re-add at end of game)
                    del self.history[self.name]
                # Otherwise create new player/hand w/collected name
                else: 
                    #new Hand object with user-specified name          
                    newHand = Hand(self.name)
                    # Add new player to current list of players
                    self.players.append(newHand)                 
        else:
            print("There can only be 2 or 3 players. Please re - enter")
            self.num_of_players(True)
        
    def play(self):
        """Play a game of 31."""
        # Clear/Reset attributes/values
        self.winners = []
        self.count = 0
        for player in self.players:
            # Reset hands
            del(player.cards[:])
            # Increment number of unique games played
            player.gamesPlayed += 1.0
        # Increment total number of games played
        self.totalGamesPlayed += 1.0
        # Prepare the deck, deal the cards
        self.deck = Deck()
        self.deck.shuffle()
        self.deck.deal(3, self)
        # Top card is placed onto discard pile
        self.discard.add(self.deck.pop())
        # While no one has satisfied winning conditions, take turns
        while not self.check_won():
            self.turn_seq()
        
    def turn_seq(self):
        """Sequence and order of turns"""
        # Increment turn count
        self.count += 1               
        for player in self.players:
            self.check_won(player)
            player.draw(self)
            player.discard(self)
            # Need to check if any player has >= 31
            self.check_won(player)

    def check_won(self, player=None):
        """Check for winner(s)"""
        # If player param was passed, check if anyone has >= 31
        if player:
            if (player.sum_hand() >= 31):
                # Player wins
                player.gamesWon += 1.0
                self.winners.append(player)
                self.present_winners()
        # Games ends after 4 turns
        elif (self.count == 4):
            # Deep copy list to manipulate elements and not disturb original
            self.winners = copy.deepcopy(self.players)
            self.winners.sort()
            self.winners.reverse()
            # Only one winner if >= 31, otherwise multiple winners
            if (self.winners[len(self.winners) - 1] < (self.winners[len(self.winners) - 2])):
                self.winners.pop()
            # Increment games won stat
            for player in self.players:
                if player in self.winners:
                    player.gamesWon += 1.0
            self.present_winners()               
        else:
            return False
    
    def present_winners(self):
        """Prints winners w/ formatting."""
        clear_screen()
        for player in self.players:
            self.history[player.name] = player 
        # Grammar reflects # of list element(s)
        if (len(self.winners) > 1):
            result = "The winners are: "
        else:
            result = "The winner is: "
        for winner in self.winners:
            # Don't append "&" to first printed winner (if more than one)
            if (winner == self.winners[(len(self.winners) - 1)]):
                result += (str(winner.name) + ", Score: " + 
                           str(winner.sum_hand()) + " " + str(winner) + " ")
            else:
                result += str(winner.name) + " & "
        print result             
        self.main_menu()
            
    def stats_menu(self):
        """Present stats menu."""
        clear_screen() 
        if (self.totalGamesPlayed == 0):
            print "There are no stats to show because no games have been played"
            self.main_menu()
        else:
            result = "Current Stats: \n\tWinning Percentages:"
            for i in self.history.iterkeys():
                result += ("\n\t\t" + str(self.history[i].name) + ": " + 
                           str(self.history[i].win_percent()))
            print result
            print ("\nTotal number of games played: " + str(self.totalGamesPlayed) + "\n")
            self.main_menu()

def clear_screen():
    """Clear the terminal."""
    if (os.name == "posix"):
        clear_cmd = "clear"
    elif (os.name == "nt"):
        clear_cmd = "cls"
    else:
        print "*** Unsupported System ***\nApplication Terminating !!!"
    os.system(clear_cmd)

    
newGame = CardGame()
