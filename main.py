import random
from Game import Game
from Cards import cards
from TreeBuilder import TreeBuilder, FILENAME

if __name__ == '__main__':
    game = Game(3)
    print ("Middle: " + str(game.middle))
    print ("Players cards: " + str(game.players) + "\n\n")

    # print ("['Scarlet', 'Knife', 'Conservatory']")
    # tree = TreeBuilder(cards, 3, ['White', 'Green', 'Lounge', 'Dumbbell'], 0)
    # tree = TreeBuilder(cards, 3, ['Ballroom', 'Plum', 'Lounge', 'Billiard Room'], 0) # -- This one failed with 0, test with stuff in temp
    tree = TreeBuilder(cards, game.numberOfPlayers, game.players[0], 0)

    file = open(FILENAME,"a") 
    file.writelines("Middle: " + str(game.middle) + "\n")
    file.writelines("Players cards: " + str(game.players) + "\n\n\n")
    file.close()

    tree.buildTree()

    # game.makeGuess(0,cards["people"][0], cards["weapons"][0], cards["rooms"][0])
    # game.play()

    # Sets the first guess before the for loop can start
    (aiGuessForCenter, aiPerson, aiWeapon, aiRoom) = tree.makeGuess()
    game.setNextGuess(aiGuessForCenter, aiPerson, aiWeapon, aiRoom)

    print ("AI guess" + str((aiPerson, aiWeapon, aiRoom)))

    # For loop that runn everytime game.play() yields a (opponent, item) back to main
    for (player, opponent, item) in game.play():

        if player is 0: 
            file = open(FILENAME,"a") 
            file.writelines("\n\nAI:\n")
            file.writelines("\tGuess: " + str((aiPerson, aiWeapon, aiRoom)) + "\n")
            file.writelines("\tResponse: " + str((opponent, item)) + "\n\n")
            file.close()

            if (opponent != None and item != None):
                tree.addConstraint(opponent, item, True)

                if (opponent > 1):
                    # Adds known unpossessed cards for players 1 to the opponent that possessed
                    for player in range(1, opponent):
                        tree.addConstraint(player, aiPerson, False)
                        tree.addConstraint(player, aiWeapon, False)
                        tree.addConstraint(player, aiRoom, False)

            else:
                # Add known unpossessed cards for all players
                for player in range(1, game.numberOfPlayers):
                    tree.addConstraint(player, aiPerson, False)
                    tree.addConstraint(player, aiWeapon, False)
                    tree.addConstraint(player, aiRoom, False)

            print("Opponent: " + str(opponent))
            print("Item: " + str(item))
        
        else:
            playerIndex = player + 1
            playerId = playerIndex % game.numberOfPlayers

            (person, weapon, room) = item

            print ((player, opponent, item))

            print ("Players", end=" ")
            while(playerId != player and playerId != opponent):
                print (playerId, end=" ")
                tree.addConstraint(playerId, person, False)
                tree.addConstraint(playerId, weapon, False)
                tree.addConstraint(playerId, room, False)
                playerIndex += 1
                playerId = playerIndex % game.numberOfPlayers

            if (player == (game.numberOfPlayers - 1)):
                tree.buildTree()
                (aiGuessForCenter, aiPerson, aiWeapon, aiRoom) = tree.makeGuess()
                game.setNextGuess(aiGuessForCenter, aiPerson, aiWeapon, aiRoom)
                input()
            