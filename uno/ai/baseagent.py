'''
Created on Jul 17, 2013

@author: Tim Vergenz
'''

class UnoAgent(object):
    ''' A superclass to represent an agent in a game of Uno. '''

    def decide_turn(self, game, hand, hand_counts):
        '''
        Decide what card to play given the `game`, a list of the cards in the
        player's hand (`hand`), and a list of tuples `(player,num)` for the
        number of cards remaining in each of the other players' hands.

        Should return:
            An UnoCard from the hand, if the decision is to play that card.
            None, if the decision is to draw from the deck.  `decide_extra`
                will then be called if this card is playable.
        '''
        raise NotImplementedError()

    def decide_extra(self, game, extra, hand, hand_counts):
        '''
        Decide whether to play a playable card drawn from the deck at the end
        of a turn.  Parameters the same as `decide_turn`, where `hand` does not
        include the new card, and `extra` is the new card. Return True or False.
        '''
        raise NotImplementedError()
