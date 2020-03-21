import random
import sys
from Cards import cards


class Game():
    def __init__(self, numberOfPlayers):
        self.numberOfPlayers = numberOfPlayers
        self.players = []
        self.middle = []

        self.middle.append(random.choice(cards["people"]))
        self.middle.append(random.choice(cards["weapons"]))
        self.middle.append(random.choice(cards["rooms"]))

        self.nextPerson = ""
        self.nextWeapon = ""
        self.nextRoom = ""

        remainingCards = cards["people"] + cards["weapons"] + cards["rooms"]
        remainingCards = [card for card in remainingCards if card not in self.middle]

        for _ in range(0, self.numberOfPlayers):
            self.players.append([])

        playerIndex = 0
        while (len(remainingCards) > 0):
            card = random.choice(remainingCards)
            self.players[playerIndex % self.numberOfPlayers].append(card)
            playerIndex += 1
            remainingCards.remove(card)

        self.winner = None

    def makeGuess(self, playerId, person, weapon, room):
        playerIndex = playerId + 1
        opponentId = playerIndex % self.numberOfPlayers

        while(opponentId != playerId):
            player = self.players[opponentId]
            hasPerson = person in player
            hasWeapon = weapon in player
            hasRoom = room in player

            if (hasPerson):
                return (opponentId, person)
            elif (hasWeapon):
                return (opponentId, weapon)
            elif (hasRoom):
                return (opponentId, room)

            playerIndex += 1
            opponentId = playerIndex % self.numberOfPlayers

        return (None, None)

    def makeGuessForMiddle(self, person, weapon, room):
        if(person in self.middle and weapon in self.middle and room in self.middle):
            return True
        else:
            return False

    def setNextGuess(self, person, weapon, room):
        self.nextPerson = person
        self.nextWeapon = weapon
        self.nextRoom = room

    def getChoice(self, type):
        return cards[type][0]
        for item in range(0,len(cards[type])):
            print(str(item + 1) + ". " + cards[type][item], end =" ")
        
        choice  = input()
        if (choice == "exit"):
            print("exit")
            sys.exit()
            return
        
        try: 
            return cards[type][int(choice) - 1]
        except:
            return self.getChoice(type)

    def play(self):
        playerIndex = 0
        playerId = playerIndex % self.numberOfPlayers

        while(self.winner == None):
            print ("Player " + str(playerId) + ", make a guess")
            
            # Request choices from non-AI players
            if (playerId != 0):
                print ("\nPick a person: ", end=" ")
                person = self.getChoice("people")

                print ("\nPick a weapon: ", end=" ")
                weapon = self.getChoice("weapons")

                print ("\nPick a room:   ", end=" ")
                room = self.getChoice("rooms")

                (opponent, item) = self.makeGuess(playerIndex, person, weapon, room)
                print("Guess: " + person + ", " + weapon + ", " + room)
                yield (playerId, opponent, (person, weapon, room))
            
            # Send guess for AI player and yield result to main
            else:
                (opponent, item) = self.makeGuess(0, self.nextPerson, self.nextWeapon, self.nextRoom)
                print("Guess: " + self.nextPerson + ", " + self.nextWeapon + ", " + self.nextRoom)
                yield (playerId, opponent, item) # Function pauses here until main completes one iteration of the for loop
            
            try:
                print(item + " shown by Player " + str(opponent))
            except:
                print("No one showed")

            playerIndex += 1
            playerId = playerIndex % self.numberOfPlayers

            print("\n\n\n\n")