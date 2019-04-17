from Agent import *
from statistics import median
from Trust import *

'''
This agent is identical to the Generic except that they will play liberals
if the fascists are ahead

'''
class PassiveFascistAgent(GenericFascistAgent):
    # a generic fascist agent might always play fascists when they can
    def chancellor_pick(self,hand):
        #if the fascists are ahead and playing a fascist won't win us the game, it can
        # be worthwile to try to build trust
        if self.game.lib_policy < self.game.fas_policy and self.game.fas_policy!=5:
            if 0 in hand: return 0
        if 1 in hand: return 1
        return 0
    
    #play a fascist when possible and claim to get two, otherwise report truthfully
    def chanc_claim(self,hand):
        #if we played a liberal, we should also tell the truth
        if self.game.lib_policy < self.game.fas_policy and self.game.fas_policy!=5:
            return sum(hand)        
        if 1 in hand: return 2
        return sum(hand)    
    