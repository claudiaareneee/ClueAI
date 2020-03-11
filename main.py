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

    # Would require game.setNextGuess to be called first before starting
    for (opponent, item) in game.play():
        if (opponent != None and item != None):
            tree.addConstraint(opponent, item, True)

            if (opponent > 1):
                for player in range(1, opponent):
                    # This may also want to note the other cards guessed
                    tree.addConstraint(player, item, False)

            tree.buildTree()

        else:
            for player in range(1, game.numberOfPlayers):
                # This needs the input of the original guess since item = None
                tree.addConstraint(player, item, False)

        print(opponent)
        print(item)

        # Functions that don't exist yet, but may be needed.
        # (person, weapon, room) = tree.NextGuess()
        # game.setNextGuess(person, weapon, room)