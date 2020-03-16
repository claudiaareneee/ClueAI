(person, weapon, room) = tree.makeGuess()
tree.addConstraint(1, person, True)
tree.buildTree()
(person, weapon, room) = tree.makeGuess()
tree.addConstraint(1, weapon, True)
tree.buildTree()

(person, weapon, room) = tree.makeGuess()
tree.addConstraint(1, person, True)
tree.buildTree()

(person, weapon, room) = tree.makeGuess()
tree.addConstraint(2, room, True)

tree.addConstraint(1, person, False)
tree.addConstraint(1, weapon, False)
tree.addConstraint(1, room, False)
tree.buildTree()
(person, weapon, room) = tree.makeGuess()



Print Tree Starts here
root   cardType: None   Player: None   Constraint violated: False
└── Conservatory   cardType: room   Player: 2   Constraint violated: False
    └── White   cardType: person   Player: 3   Constraint violated: False
        └── Green   cardType: person   Player: 1   Constraint violated: False
            └── Scarlet   cardType: person   Player: 1   Constraint violated: False
                └── Rope   cardType: weapon   Player: 2   Constraint violated: False
                    └── Knife   cardType: weapon   Player: 2   Constraint violated: False
                        └── Dumbell   cardType: weapon   Player: 3   Constraint violated: False
                            └── Wrench   cardType: weapon   Player: 1   Constraint violated: Forward checking: Children will have too many cards, center already has weapon


Constraints: 
	{'knownCards': ['Ballroom', 'Plum', 'Lounge', 'Billiard Room'], 'knownUnpossessedCards': [], 'numberOfCards': 4}
	{'knownCards': ['Scarlet', 'Wrench', 'Green'], 'knownUnpossessedCards': ['White', 'Dumbell', 'Conservatory'], 'numberOfCards': 3}
	{'knownCards': ['Conservatory'], 'knownUnpossessedCards': [], 'numberOfCards': 3}
	{'knownCards': [], 'knownUnpossessedCards': [], 'numberOfCards': 3}

Middle: ['White', 'Dumbell', 'Study']
Players cards: [['Green', 'Scarlet', 'Wrench'], ['Rope', 'Conservatory', 'Knife']]