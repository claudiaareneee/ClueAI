import random
from Game import Game
from Cards import cards
from TreeBuilder import TreeBuilder

if __name__ == '__main__':
    game = Game(3)
    print ("Middle: " + str(game.middle))
    print ("Players cards: " + str(game.players))

    # print ("['Scarlet', 'Knife', 'Conservatory']")
    # tree = TreeBuilder(cards, 3, ['White', 'Green', 'Lounge', 'Dumbell'], 0)
    tree = TreeBuilder(cards, game.numberOfPlayers, game.players[0], 0)

    # game.makeGuess(0,cards["people"][0], cards["weapons"][0], cards["rooms"][0])
    # game.play()

    # Sets the first guess before the for loop can start
    (person, weapon, room) = tree.makeGuess()
    game.setNextGuess(person, weapon, room)

    print ("AI guess" + str((person, weapon, room)))

    # For loop that runn everytime game.play() yields a (opponent, item) back to main
    for (opponent, item) in game.play():
        if (opponent != None and item != None):
            tree.addConstraint(opponent, item, True)

            if (opponent > 1):
                # Adds known unpossessed cards for players 1 to the opponent that possessed
                for player in range(1, opponent):
                    tree.addConstraint(player, person, False)
                    tree.addConstraint(player, weapon, False)
                    tree.addConstraint(player, room, False)

        else:
            # Add known unpossessed cards for all players
            for player in range(1, game.numberOfPlayers):
                tree.addConstraint(player, person, False)
                tree.addConstraint(player, weapon, False)
                tree.addConstraint(player, room, False)

        tree.buildTree()

        print("Opponent: " + str(opponent))
        print("Item: " + str(item))

        (person, weapon, room) = tree.makeGuess()
        game.setNextGuess(person, weapon, room)