'''
Created on Jul 10, 2013

@author: Tim Vergenz
'''

from uno.game import deck

class UnoGame(object):
    ''' A class to contain the state of the game. '''

    def __init__(self, players):
        ''' Initialize the game.  `players` is a sequence of UnoAgents. '''
        self.deck = deck.UnoDeck()
        self.play_pile = deck.UnoPile()

        self._turn_hook = None

        # initialize the players and turn iterator
        assert len(players) > 1
        self.players = players
        self._turn_iter = self._players_iterator()

        # deal the _hands
        self._hands = {}
        for player in self.players:
            self._hands[player] = self.deck.draw_multiple(7)

        # put the first card into play
        while True:
            card = self.deck.draw()
            self.play_pile.add(card)
            if isinstance(card, deck.Num):
                break
        self.color = self.play_pile.top_card().color

    def do_turn(self):
        ''' Do one turn in the game. '''
        player = self._turn_iter.next()

        if self._turn_hook is not None:
            self._turn_hook(player, self)
            if self._end_turn:
                self._end_turn = False
                return

        hand = self._hands[player]
        counts = [(p, len(self._hands[p])) for p in self.players]
        decision = player.decide_turn(self, hand, counts)

        if decision is not None:
            card = decision
            assert card in hand
            assert card.is_play_allowed(self)

            hand.remove(card)
            self.play_pile.add(card)
            card.do_effects(player, self)
        else:
            newcard = self.deck.draw()
            if newcard.is_play_allowed(self):
                if player.decide_extra(self, newcard, hand, counts):
                    self.play_deck.add(newcard)
            else:
                hand.append(newcard)

    def end_turn(self):
        ''' Used from within a turn hook.  Ends the current turn early. '''
        self._end_turn = True

    def add_turn_hook(self, hook):
        self._turn_hook = hook

    def _players_iterator(self):
        ''' An iterator that always returns the next player in the game. '''
        self._turn_index = 0
        self._direction = 1  # or -1
        while True:
            yield self.players[self._turn_index]
            self._turn_index += self._direction
            self._turn_index %= len(self.players)

    def reverse(self):
        ''' Reverse the order of turns. '''
        self._direction *= -1
