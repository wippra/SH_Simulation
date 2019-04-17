from Agent import *
import random
from statistics import median
from Trust import *
'''
This agent is identical to the Generic except that
as president, when receiving 2L1F, they will sometimes
opt to give the chancellor a choice
'''
class MixedLiberalAgent(GenericLiberalAgent):
    # liberal agents always discard fascists when they can
    def pres_discard(self,chancellor,hand):
        #2L1F
        if sum(hand)==1:
            #if forcing a lib wins the game, we should do thats
            if self.game.lib_policy!=4:
                # otherwise, if the liberals are ahead, we can afford to risk a fascist play
                # to gather information
                if self.game.lib_policy > self.game.fas_policy:
                    return 0
        if 1 in hand: return 1
        return 0    