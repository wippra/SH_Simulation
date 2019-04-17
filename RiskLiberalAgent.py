from Agent import *
import random
from statistics import median
from Trust import *
'''
This agent is identical to the Generic except that
as president, when receiving 2L1F, they will always
opt to give the chancellor a choice (except when
forcing a liberal wins them the game)
'''
class RiskLiberalAgent(GenericLiberalAgent):
    # liberal agents always discard fascists when they can
    def pres_discard(self,chancellor,hand):
        #2L1F
        if sum(hand)==1:
            #if forcing a lib wins the game, we should do that
            if self.game.lib_policy!=4:
                return 0
        if 1 in hand: return 1
        return 0    