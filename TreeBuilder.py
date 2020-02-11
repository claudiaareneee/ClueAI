from anytree import NodeMixin, RenderTree
import copy

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
            self.players.append({'knownCards' : [], 'numberOfCards' : 0})

        for card in playerCards:
            if card in self.remainingDeck['people']:
                self.remainingDeck['people'].remove(card)
            
            elif card in self.remainingDeck['weapons']:
                self.remainingDeck['weapons'].remove(card)

            elif card in self.remainingDeck['rooms']: 
                self.remainingDeck['rooms'].remove(card)
            
            else:
                print("card " + card + " wasn't in deck")

        playerIndex = 0
        numberOfCardsInDeck = len(deck["people"]) + len(deck["weapons"]) + len(deck["rooms"]) - 3
        
        while (numberOfCardsInDeck > 0):
            self.players[playerIndex % self.numberOfPlayers]['numberOfCards'] += 1
            playerIndex += 1
            numberOfCardsInDeck -= 1

        self.players[playerNumberInOrder]['knownCards'] = playerCards
        self.players[numberOfPlayers]['numberOfCards'] = 3

        self.buildTree()

    def buildTree(self):
        self.root = Item('root', None, None, parent=None, children=None)

        deck = []

        for item in self.remainingDeck['people']:
            deck.append({'name': item, 'cardType': 'person'})
        for item in self.remainingDeck['weapons']:
            deck.append({'name': item, 'cardType': 'weapon'})
        for item in self.remainingDeck['rooms']:
            deck.append({'name': item, 'cardType': 'room'})

        # print(deck)

        self.addItemToTree(self.root, [], deck)        
        
        self.printTree()

        self.checkForWinners()
        print("wow done")

    def addItemToTree(self, node, visited, deck):
        self.checkConstraints(node, deck)

        if (len(node.children) == 0 and node.shouldHaveChildren):
            for player in range(self.numberOfPlayers):
                # if player != self.playerNumberInOrder:
                child = Item(deck[node.depth - 1]['name'], player, deck[node.depth - 1]['cardType'], parent=node, children=None)
                visited.append(node)
                self.addItemToTree(child, visited, deck)

        if node in visited:
            pass

    def checkConstraints(self, node, deck):
        shouldHaveChildren = True
        parent = node
        cardCount = []
        # center = {'hasPerson': False, 'hasWeapon': False, 'hasRoom': False}

        for item in range(self.numberOfPlayers):
            cardCount.append(item)

        while parent is not self.root:
            cardCount[parent.holder] += 1
            
            if cardCount[parent.holder] > self.players[parent.holder]['numberOfCards']:
                # print ( str(parent.holder) + "  " + parent.name + " count " + str(cardCount[parent.holder]) + "  number " + str(self.players[parent.holder]['numberOfCards']))
                node.constraintViolated = True
                break

            parent = parent.parent

        if (node.depth >= len(deck) or node.constraintViolated):
            shouldHaveChildren = False

        node.shouldHaveChildren = shouldHaveChildren

    def printTree(self):
        for pre, fill, node in RenderTree(self.root):
            treestr = u"%s%s" % (pre, node.name)
    
            print(treestr.ljust(8), "   cardType: " + str(node.cardType), "   Player: " + str(node.holder), "   Constraint violated: " + str(node.constraintViolated))
        
        print("\n\n\n")

    def checkForWinners(self):
        solutions = []
        for leaf in self.root.leaves:
            if (not leaf.constraintViolated):
                solutions.append(leaf)
                print(RenderTree(leaf))
        


