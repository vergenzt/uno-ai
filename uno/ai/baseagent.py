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


class UserAgentProxy(UnoAgent):
    ''' A user-controlled agent that asks what to do on the command line. '''

    def __init__(self, name):
        self._name = name

    def decide_turn(self, game, hand, hand_counts):
        print "********************"
        print "%s's turn" % self._name
        print "    Current color: %s" % game.color
        print "    Top card:      %s" % str(game.play_pile.top_card())
        print "    Hand:"
        print "      0: [Draw from deck]"
        for i, card in enumerate(hand):
            print "      %d: %s" % (i + 1, str(card))

        card = None
        while True:
            index = int(raw_input("Your choice? "))
            if index == 0:
                return None
            else:
                card = hand[index - 1]
                if card.is_play_allowed(game):
                    break
                else:
                    print "  You can't play that card! Pick again."

        return card

    def decide_extra(self, game, extra, hand, hand_counts):
        return True
