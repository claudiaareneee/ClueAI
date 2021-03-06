from anytree import NodeMixin, RenderTree
import copy
import operator
import time

FILENAME = 'tree.txt'
PERSON = 'person'
WEAPON = 'weapon'
ROOM = 'room'
KNOWNCARDS = 'knownCards'
KNOWNUNPOSSESSEDCARDS = 'knownUnpossessedCards'
NUMBEROFCARDS = 'numberOfCards'
NAME = 'name'
CARDTYPE = 'cardType'


class Item(NodeMixin):
    def __init__(self, name, holder, cardType, parent=None, children=None):
        super(Item, self).__init__()
        self.name = name
        self.holder = holder
        self.cardType = cardType
        self.parent = parent
        self.shouldHaveChildren = True
        self.constraintViolated = False

        if children:
            self.children = children

class TreeBuilder():
    def __init__(self, deck, numberOfPlayers, playerCards, playerNumberInOrder):
        self.deck = deck
        self.remainingDeck = copy.deepcopy(deck)
        self.numberOfPlayers = numberOfPlayers
        self.playerNumberInOrder = playerNumberInOrder
        self.players = []

        for _ in range(0, self.numberOfPlayers + 1): #  = 1 for center
            self.players.append({KNOWNCARDS : [], KNOWNUNPOSSESSEDCARDS:[], NUMBEROFCARDS : 0})

        for card in playerCards:
            if card in self.remainingDeck[PERSON]:
                self.remainingDeck[PERSON].remove(card)
            
            elif card in self.remainingDeck[WEAPON]:
                self.remainingDeck[WEAPON].remove(card)

            elif card in self.remainingDeck[ROOM]: 
                self.remainingDeck[ROOM].remove(card)
            
            else:
                print("card " + card + " wasn't in deck")

        playerIndex = 0

        self.numberOfCardsTypes = {PERSON: deck[PERSON], WEAPON: deck[WEAPON], ROOM: deck[ROOM]}
        numberOfCardsInDeck = len(deck[PERSON]) + len(deck[WEAPON]) + len(deck[ROOM]) - 3
        
        while (numberOfCardsInDeck > 0):
            self.players[playerIndex % self.numberOfPlayers][NUMBEROFCARDS] += 1
            playerIndex += 1
            numberOfCardsInDeck -= 1

        self.players[playerNumberInOrder][KNOWNCARDS] = playerCards
        self.players[numberOfPlayers][NUMBEROFCARDS] = 3

        self.file = open(FILENAME,"w") 
        self.file.writelines("Trees\n\n\n")
        self.file.close()

        # self.buildTree()

    def buildTree(self):
        initialTime = time.time()
        self.root = Item('root', None, None, parent=None, children=None)

        deck = []

        for item in self.remainingDeck[PERSON]:
            deck.append({NAME: item, CARDTYPE: PERSON})
        for item in self.remainingDeck[WEAPON]:
            deck.append({NAME: item, CARDTYPE: WEAPON})
        for item in self.remainingDeck[ROOM]:
            deck.append({NAME: item, CARDTYPE: ROOM})

        self.addItemToTree(self.root, deck)

        self.printTree()

        elapsedTime = time.time() - initialTime

        self.file = open(FILENAME,"a") 
        self.file.writelines("\nElapsed Time: " + str(elapsedTime) + " s\n")
        self.file.close()

        # self.checkForWinners()
        # self.makeGuess()
        # print("wow done")

    def addItemToTree(self, node, deck):
        self.checkConstraints(node, deck)

        if (len(node.children) == 0 and node.shouldHaveChildren):
            for player in range(self.numberOfPlayers + 1):
                # if len(self.root.descendants) > 500:
                #     return

                if player != self.playerNumberInOrder:
                    child = Item(deck[node.depth][NAME], player, deck[node.depth][CARDTYPE], parent=node, children=None)
                    self.addItemToTree(child, deck)

    def checkConstraints(self, node, deck):
        shouldHaveChildren = True
        parent = node
        cardCountPlayer = []
        cardCountType = {PERSON: 0, WEAPON: 0, ROOM: 0}
        center = {PERSON: None, WEAPON: None, ROOM: None}

        for _ in range(self.numberOfPlayers + 1):
            cardCountPlayer.append(0)

        while parent is not self.root:
            cardCountPlayer[parent.holder] += 1
            cardCountType[parent.cardType] += 1

            if (parent.holder == self.numberOfPlayers):
                if (center[parent.cardType] is None):
                    center[parent.cardType] = parent.name
                else:
                    node.constraintViolated = "Parent has more than one " + parent.cardType
                    break

            if (center[parent.cardType] is None and cardCountType[parent.cardType] is self.numberOfCardsTypes[parent.cardType]):
                    node.constraintViolated = "Center doesn't have a " + parent.cardType
                    break

            if cardCountPlayer[parent.holder] > self.players[parent.holder][NUMBEROFCARDS]:
                # print ( str(parent.holder) + "  " + parent.name + " count " + str(cardCountPlayer[parent.holder]) + "  number " + str(self.players[parent.holder][NUMBEROFCARDS]))
                node.constraintViolated = "Player " + str(parent.holder) + " has too many cards"
                break

            if parent.holder == self.playerNumberInOrder:
                node.constraintViolated = "Player " + str(self.playerNumberInOrder) + " already has this card"
                break

            for i in range(self.numberOfPlayers):
                if parent.name in self.players[i][KNOWNCARDS]:
                    if parent.holder is not i:
                        parent.constraintViolated = "Player " + str(i) + " should have " + parent.name
                        break
                
                elif parent.name in self.players[i][KNOWNUNPOSSESSEDCARDS]:
                    if parent.holder is i:
                        parent.constraintViolated = "Player " + str(i) + " should not have " + parent.name
                        break


            parent = parent.parent

        # TODO: look into this, it's giving errors
        if ((not node.constraintViolated) and (node.cardType in center) and (center[node.cardType] is not None)):
            constraintViolations = 0
            
            for player in range(1, self.numberOfPlayers):
                if (cardCountPlayer[player] > (self.players[player][NUMBEROFCARDS] -1)):
                    constraintViolations += 1

            if (node.depth < (len(deck)-1) and (constraintViolations == (self.numberOfPlayers - 1))):
                node.constraintViolated = "Forward checking: Children will have too many cards, center already has " + node.cardType

        if (node.depth >= len(deck) or node.constraintViolated):
            shouldHaveChildren = False

        if (node.depth >= len(deck) and not node.constraintViolated):
            node.constraintViolated = "False: Could be a winner"
        

        node.shouldHaveChildren = shouldHaveChildren


    def printTree(self):
        # TODO: Remove
        self.file = open(FILENAME,"a", encoding='utf-8') 
        self.file.writelines("Print Tree Starts here\n")

        for pre, _, node in RenderTree(self.root):
            treestr = u"%s%s" % (pre, node.name)

            # print(treestr.ljust(8), "   cardType: " + str(node.cardType), "   Player: " + str(node.holder), "   Constraint violated: " + str(node.constraintViolated))
            self.file.writelines(str(treestr) + "   cardType: " + str(node.cardType) + "   Player: " + str(node.holder) + "   Constraint violated: " + str(node.constraintViolated) + "\n")
        
        self.file.writelines("\n\nConstraints: ")
        for x in range (0, self.numberOfPlayers + 1):
            self.file.writelines("\n\t" + str(self.players[x]))
            

        # print("\n\n\n")
        self.file.writelines("\n\nNumber of decendants " + str(len(self.root.descendants)))
        self.file.writelines("\n\n\n")

        # TODO: remove
        self.file.close()
        

    def checkForWinners(self):
        self.file = open(FILENAME,"a") 
        self.file.writelines("\nSolutions start here: \n")
        
        solutions = []
        for leaf in self.root.leaves:
            if (leaf.constraintViolated == "False: Could be a winner"):
                playerCards = []

                for _ in range(self.numberOfPlayers + 1):
                    playerCards.append([])
                
                # solutions.append(leaf)

                parent = leaf
                leafpath = ""
                
                while parent is not self.root:
                    leafpath = parent.name + ", Player " + str(parent.holder) + ", " + parent.cardType + " \n" + leafpath
                    if(parent.holder is not None):
                        playerCards[parent.holder].append([parent.name, parent.cardType]) #{"name":parent.name, "type": parent.type}
                    parent = parent.parent

                self.file.writelines(str(playerCards) + '\n')
                solutions.append(playerCards)
                # print(leafpath + "\n\n")
                # print(leafpath)
        
        self.file.writelines("\n\n\n")

        print("Number of solutions: " + str(len(solutions)))
        self.file.writelines("Number of solutions: " + str(len(solutions)) + "\n")
        self.file.close()
        return(solutions)

    def addConstraint(self, player, cardName, possessed):
        if possessed:
            if (not cardName in self.players[player][KNOWNCARDS]):
                self.players[player][KNOWNCARDS].append(cardName)
        else: 
            if (not cardName in self.players[player][KNOWNUNPOSSESSEDCARDS]):
                self.players[player][KNOWNUNPOSSESSEDCARDS].append(cardName)

    def makeGuess(self):
        centerCards = {PERSON: {}, WEAPON: {}, ROOM: {}}

        solutions = self.checkForWinners()

        if len (solutions) is 0:
            return ("", "", "")

        for solution in solutions:
            center = solution[-1]
            for item in center:
                try:
                    centerCards[item[1]][item[0]] += 1
                except:
                    centerCards[item[1]][item[0]] =  1

        person = max(centerCards[PERSON].items(), key=operator.itemgetter(1))[0]
        weapon = max(centerCards[WEAPON].items(), key=operator.itemgetter(1))[0]
        room = max(centerCards[ROOM].items(), key=operator.itemgetter(1))[0]

        if (len(centerCards[PERSON]) == 1 and len(centerCards[WEAPON]) == 1 and len(centerCards[ROOM]) == 1):
            guess = (True, person, weapon, room)
        else:     
            guess = (False, person, weapon, room)

        return guess