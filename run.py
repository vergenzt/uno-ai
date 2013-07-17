
if __name__ == '__main__':
    from uno import ai, game
    tim = ai.UserAgent('Tim')
    bob = ai.UserAgent('Bob')
    uno = game.UnoGame([tim, bob])

    while True:
        uno.do_turn()
