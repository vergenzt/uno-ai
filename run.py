
if __name__ == '__main__':
    from uno import ai, game
    tim = ai.UserAgentProxy('Tim')
    bob = ai.UserAgentProxy('Bob')
    uno = game.UnoGame([tim, bob])

    while True:
        uno.do_turn()
