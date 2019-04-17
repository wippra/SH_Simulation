from Agent import *
from statistics import median
from Trust import *

#implementation of Agent with some generic fascist playstyles
class GenericHitlerAgent(Agent):
    def __init__(self,role,game):
        self.index = None #integer indicating index in SH_game.agents
        self.role = role # 'L': liberal, 'F': fascist, 'H': hitler
        self.is_dead=False
        self.game=game
    
    # returns the policy alignment card (so Hitler isn't completely exposed)
    def get_role(self):
        return self.role if self.role!='H' else 'F'
    
    # returns 1 if the agent approves of this pres/chanc pair (ja)
    # returns 0 if the agent disapproves of the pair (nein)
    def vote(self,president,chancellor):
        # Get the trust of all agents
        trust_list = list(map(self.trust,self.game.agents))
        
        # Get the median
        med = median(trust_list)
        
        # Vote yes if both players are strictly in the top half of trust among all players
        if self.trust(president) >= med and self.trust(chancellor) >= med:
            return 1
        return 0
    
    # pick the most trusted available player
    def select_chancellor(self,options):
        random.shuffle(options)
        best = options[0]
        t = self.trust(best)
        for o in options:
            nt = self.trust(o)
            if nt > t:
                best = o
                t = nt
        return best
    
    # liberal agents always discard fascists when they can
    # but hitler will force a fascist if it wins the game
    def pres_discard(self,chancellor,hand):
        if self.game.fas_policy==5:
            if 0 in hand: return 0
        if 1 in hand: return 1
        return 0
    
    # tell the truth
    def pres_claim(self,chancellor,hand):
        return sum(hand)
    
    # liberal agents always play liberals when they can
    # Hitler will play a fascist if a liberal is game over
    def chancellor_pick(self,hand):
        if self.game.lib_policy==4:
            if 1 in hand: return 1
        if 0 in hand: return 0
        return 1
    
    #tell the truth, except for the edge case
    def chanc_claim(self,hand):
        if self.game.lib_policy==4:
            return 2
        return sum(hand)
    
    # a liberal agent wants to veto the two facsist case
    # Hitler only vetoes as president in certain edge cases
    def veto(self,hand,is_pres):
        if sum(hand)==2:
            return False #force a fascist to win the game
        #try to stop a liberal from being played
        return True
        
    # pick the least trusted player
    def kill(self,options):
        # A player should not be allowed to kill themselves
        if self.index in options:
            options.remove(self.index)
            
        random.shuffle(options)
        worst = options[0]
        
        t = self.trust(worst)
        for o in options:
            nt = self.trust(o)
            if nt < t:
                worst = o
                t = nt
        return worst
    
    # when this player is president and unlocks the special election,
    # this function returns which agent they choose to be president
    def pres_special(self,options):
        random.shuffle(options)
        best = options[0]
        t = self.trust(best)
        for o in options:
            nt = self.trust(o)
            if nt > t:
                best = o
                t = nt
        return best
    
    #pick someone and tell the truth
    def investigation(self,options):
        random.shuffle(options)
        return options[0],options[0].get_role()
    
    #tell the truth about the top three cards
    def top_three(self,top):
        return top
    
    #use the history of the game to come up with a guess for the role of this player
    def trust(self, agent, stop=False, stopNum=0):
        L = 0
        F = 0
        trust = Trust()
        index = agent.index
        if not stop:
            stopNum = len(self.game.history)
        for round_num, e in enumerate(self.game.history[0:stopNum]):
                
            #see participation in government
            if e['event']=='election':
                #compare their vote to my vote
                votes = e['votes']
                if votes[self.index]==votes[index]:
                    trust += Trust.SameVote
                else:
                    trust += Trust.DifferentVote
                if e['president']!=index and e['chancellor']!=index: continue
                if e['result']!=0 and e['result']!=1: 
                    continue
                #presidents are mostly responsible for results of play
                
                if e['result']==1:
                    if e['president']==index:
                        trust += Trust.PresidentPlaysFascist * Trust.nthFascistWeight[F]
                    else:
                        trust += Trust.ChancellorPlaysFascist * Trust.nthFascistWeight[F]
                        #If I was the president and they played a fascist, and I know I gave then a liberal, they must be fascist
                        if e['president']==self.index:
                            if 0 in e['chanc_hand']:
                                trust += Trust.CertainFascist
                    F += 1
                else:
                    if e['president']==index:
                        trust += Trust.PresidentPlaysLiberal * Trust.nthLiberaltWeight[L]
                    else:
                        trust += Trust.ChancellorPlaysLiberal * Trust.nthLiberaltWeight[L]
                    L += 1   
 
                
            #see special events
            #investigation
            if e['event']=='investigation':
                if e['invest']==index:
                    if e['pres_claim']=='L': 
                        trust += Trust.InvestigateClaimedLiberal
                        #if I am the president, I know that they are liberal
                        if e['president']==self.index:
                            trust += Trust.CertainLiberal
                    else: 
                        trust += Trust.InvestigateClaimedFascist
                        #if I am the president, I know that they are fascist
                        if e['president']==self.index:
                            trust += Trust.CertainFascist
            
            # we add to the killer the negative trust of the person that was killed
            if ['event']=='kill':
                if e['pres']==index:
                    trust += -self.trust(self.game.agents[e['kill']],True,round_num)
                      
        return trust.get_value()