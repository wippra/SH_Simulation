'''
This class is what all players use to evaluate the 'trustworthiness'
 of other players. Ideally, Liberals would hope that this system 
 allows them to have a good estimate of which players are on which
 team, but this is not always the case.
'''

class Trust():

    # Weights assigned to the president's result
    PresidentPlaysFascist = -3
    PresidentPlaysLiberal = 2
    
    # Weights assigned to the chancellor's result
    ChancellorPlaysFascist = -1
    ChancellorPlaysLiberal = 1
    
    # Weights assigned to agreeing or disagreeing on an election vote
    SameVote = 1
    DifferentVote = -1
    
    # Weights assigned to the investigated player, and the role the president claims they are
    InvestigateClaimedLiberal = 2
    InvestigateClaimedFascist = -2
    
    # The 'Certain' trust values indicate that a player has complete
    # information about another player. Examples include:
    #   - A president knows that their chancellor played a fascist when given a liberal,
    #       indicating they are a fascist (since they are not a rational liberal)
    #   - A president investigates another player and sees they are fascist
    CertainFascist = -2**31
    CertainLiberal =  2**31
    
    # These weights can be assigned to put more emphasis on cards played later in the game
    # For example, a fascist may avoid playing the 4th liberal policy, therefore playing
    # the 4th liberal policy is a good indication of trustworthiness
    nthLiberaltWeight = [1, 1, 1, 1, 1, 1]
    nthFascistWeight = [1, 1, 1, 1, 1, 1, 1]
    
    def __init__(self):
        self.Trust = 0
        
    def __iadd__(self, other):
        self.Trust += other
        return self
        
    def get_value(self):
        return self.Trust
    
    def __str__(self):
        return str(self.Trust)