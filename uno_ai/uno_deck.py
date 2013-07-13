'''
Created on Jul 10, 2013

@author: Tim Vergenz
'''

import random

class UnoDeck(list):
    ''' Represent a deck of Uno cards. '''

    def __init__(self, shuffled=True):
        ''' Initialize the deck, optionally shuffled (default: true) '''
        super.__init__(self)
        self._fill_with_cards()
        if shuffled:
            random.shuffle(self)

    def _fill_with_cards(self):
        ''' Add the default Uno card set to this deck. '''
        for color in 'rgby':
            self.append(Num(0, color))
            for num in 2 * range(1, 10):
                self.append(Num(num, color))
            for special_class in 2 * (Skip, Reverse, DrawTwo):
                self.append(special_class(color))
        # add wilds

class UnoCard(object):
    ''' Represent a single card and its effects on the game. '''

    def __init__(self):
        ''' Initialize the Uno card. '''
        raise NotImplementedError()

    def do_effect(self, player, game, **kwargs):
        ''' Handle any effects a card has outside of being added to the pile. '''
        pass

    def is_play_allowed(self, game):
        ''' Return True if card may be played given the previous game state. '''
        return True

########################
# Card definitions
########################

class Num(UnoCard):
    def __init__(self, val, color):
        self.num = val
        self.color = color
    def is_play_allowed(self, game):
        if self.color == game.play_color:
            return True
        last_card = game.play_pile[-1]
        if isinstance(last_card, Num) and self.num == last_card.num:
            return True

class Special(UnoCard):
    def __init__(self, color):
        self.color = color
    def is_play_allowed(self, game):
        if self.color == game.play_color:
            return True
        last_card = game.play_pile[-1]
        if self.__class__ == last_card.__class__:
            return True

class Skip(Special):
    def do_effect(self, player, game, **kwargs):
        game.players_iter.next()

class Reverse(Special):
    def do_effect(self, player, game, **kwargs):
        game.reverse()

class DrawTwo(Special):
    def do_effect(self, player, game, **kwargs):
        pass
