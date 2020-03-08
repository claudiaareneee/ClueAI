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