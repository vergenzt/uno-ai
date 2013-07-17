'''
Created on Jul 10, 2013

@author: Tim Vergenz
'''

import random

class UnoDeck(object):
    ''' Represent a deck of Uno cards. '''

    def __init__(self, empty=False, shuffled=True):
        ''' Initialize the deck. '''
        self._deck = list()
        if not empty:
            self._fill_with_cards()
            if shuffled:
                random.shuffle(self._deck)

    def _fill_with_cards(self):
        ''' Add the default Uno card set to this deck. '''
        for color in 'RGBY':
            self._deck.append(Num(0, color))
            for num in 2 * range(1, 10):
                self._deck.append(Num(num, color))
            for special_class in 2 * (Skip, Reverse, DrawTwo):
                self._deck.append(special_class(color))
        # add_to_top wilds

    def draw(self):
        ''' Draw a single card from the deck. '''
        return self.draw_multiple(1)[0]

    def draw_multiple(self, n):
        ''' Draw `n` cards from the deck and return them as a sequence. '''
        assert n <= len(self._deck)
        cards = self._deck[-n:]
        self._deck[-n:] = []
        return cards

class UnoPile(list):
    ''' Represent a face-up pile of Uno cards. '''

    def add(self, card):
        ''' Add a card to the pile, and change the state accordingly. '''
        self.append(card)

    def top_card(self):
        return self[-1]

    def top_cards(self, n):
        return self[-n:]

class UnoCard(object):
    ''' Represent a single card and its effects on the game. '''

    def __init__(self):
        ''' Initialize the Uno card. '''
        raise NotImplementedError()

    def is_play_allowed(self, game):
        ''' Return whether the card can be played on the current game state. '''
        raise NotImplementedError()

    def do_effects(self, player, game):
        '''
        Play the card in the game, given the player that played it and the
        current state of the game.
        '''
        raise NotImplementedError()


########################
# Card definitions
########################

class Num(UnoCard):
    def __init__(self, num, color):
        self.num = num
        self.color = color
    def is_play_allowed(self, game):
        if self.color == game.color:
            return True
        top = game.play_pile.top_card()
        if isinstance(top, Num) and top.num == self.num:
            return True
    def do_effects(self, player, game):
        game.color = self.color
    def __str__(self):
        return '%s %s' % (self.color, self.num)

class Special(UnoCard):
    def __init__(self, color):
        self.color = color
    def is_play_allowed(self, game):
        if self.color == game.color:
            return True
        top = game.play_pile.top_card()
        if self.__class__ == top.__class__:
            return True
    def do_effects(self, player, game):
        game.color = self.color

class Skip(Special):
    def do_effects(self, player, game):
        Special.do_effects(self, player, game)
        game._turn_iter.next()
    def __str__(self):
        return '%s Skip' % self.color

class Reverse(Special):
    def do_effects(self, player, game):
        Special.do_effects(self, player, game)
        game.reverse()
    def __str__(self):
        return '%s Reverse' % self.color

class DrawTwo(Special):
    def do_effects(self, player, game):
        Special.do_effects(self, player, game)
        def draw_hook(_player, _game):
            _game._hands[_player] += _game.deck.draw_multiple(2)
            _game.end_turn()
        game.add_turn_hook(draw_hook)
    def __str__(self):
        return '%s DrawTwo' % self.color
