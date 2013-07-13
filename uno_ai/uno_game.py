'''
Created on Jul 10, 2013

@author: Tim Vergenz
'''

import uno_deck
import itertools

class UnoGame(object):
    ''' A class to contain the state of the game. '''

    def __init__(self, players):
        ''' Initialize the game.  `players` is a sequence of UnoAgents. '''
        self.deck = uno_deck.UnoDeck()
        self.play_pile = list()

        # put the first card into play
        self.play_pile.append(self.deck.pop())
        while not isinstance(self.play_pile[-1], uno_deck.Num):
            self.play_pile.append(self.deck.pop())
        self.play_color = self.play_pile[-1].color

        assert len(players) > 1
        self.players = players
        self.players_iter = itertools.cycle(self.players)

    def do_turn(self):
        ''' Do one turn in the game. '''
        pass

    def reverse(self):
        ''' Reverse the order of turns. '''
        pass

class UnoAgent(object):
    ''' A superclass to represent an agent in a game of Uno. '''
    pass
