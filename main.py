import random
from Game import Game
from Cards import cards
from TreeBuilder import TreeBuilder

if __name__ == '__main__':
    game = Game(3)
    print(game.middle)
    print (game.players)

    # print ("['Scarlet', 'Knife', 'Conservatory']")
    # tree = TreeBuilder(cards, 3, ['White', 'Green', 'Lounge', 'Dumbell'], 0)
    tree = TreeBuilder(cards, game.numberOfPlayers, game.players[0], 0)

    # game.makeGuess(0,cards["people"][0], cards["weapons"][0], cards["rooms"][0])
    # game.play()

    # Testing: This may or may not work
    for (opponent, item) in game.play():
        if (opponent != None && item != None):
            tree.addConstraint(opponent, item, true)

            if (opponent > 1):
                for player in range(1, opponent):
                    tree.addConstraint(player, person, false)
                    tree.addConstraint(player, weapon, false)
                    tree.addConstraint(player, room, false)

        else:
            for player in range(1, game.numberOfPlayers):
                tree.addConstraint(player, person, false)
                tree.addConstraint(player, weapon, false)
                tree.addConstraint(player, room, false)

        # Functions that don't exist yet, but may be needed.
        (person, weapon, room) = tree.NextGuess()
        game.setNextGuess(person, weapon, room)