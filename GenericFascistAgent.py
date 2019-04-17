from Agent import *
from statistics import median
from Trust import *

#implementation of Agent with some generic fascist playstyles
class GenericFascistAgent(Agent):
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
        #if the chancellor is Hitler vote yes
        if chancellor.role=='H': return 1
        # Get the trust of all agents
        trust_list = list(map(self.trust,self.game.agents))
        
        # Get the median
        med = median(trust_list)
        
        # Vote yes if both players are strictly in the top half of trust among all players
        if self.trust(president) >= med and self.trust(chancellor) >= med:
            return 1
        return 0
    
    # this returns the available agent that this agent prefers when they are president
    def select_chancellor(self,options):
        #randomly pick amongst the top trusted players
        random.shuffle(options)
        tmp = options[0]
        # Get the trust of all agents
        trust_list = list(map(self.trust,self.game.agents))
        
        # Get the median
        med = median(trust_list)
        
        for op in options:
            if self.trust(op) < med:
                options.remove(op)
        
        random.shuffle(options)
        if len(options)==0: return tmp
        return options[0]
    
    # a generic fascist agent may always discard liberals when they can
    def pres_discard(self,chancellor,hand):
        if 0 in hand: return 0
        return 1
    
    # either say 3 fascists or gave a choice
    def pres_claim(self,chancellor,hand):
        f = sum(hand)
        #if the chancellor is fascist, try to cover
        if chancellor.get_role()=='F':
            # I got three fascists!
            if f >= 2:
                return 3
            return 1
        #try to make it seems like there are less fascists in the deck than actually
        if f<=2:
            return 2
        if f==1:
            return 2
        return 1
    
    # a generic fascist agent might always play fascists when they can
    def chancellor_pick(self,hand):
        if 1 in hand: return 1
        return 0
    
    #play a fascist when possible and claim to get two, otherwise report truthfully
    def chanc_claim(self,hand):
        if 1 in hand: return 2
        return sum(hand)
    
    # if the president is the fascist, he only agrees to a veto if it contains a liberal
    # if the chancellor is the fascist, he only agrees to a veto if it only contains liberals
    def veto(self,hand,is_pres):
        if is_pres:
            return 0 in hand
        else:
            return 1 not in hand
        
    
    # when this player is president and a fascist is played so that they must kill someone,
    # this function returns which agent they choose to kill
    def kill(self,options):
        # fascists should only kill liberals
        for op in options:
            if op.role!='L':
                options.remove(op)
                # A player should not be allowed to kill themselves
                if self.index in options:
                    options.remove(self.index)
         
        # now, we kill the most trusted liberal player    
        random.shuffle(options)
        best = options[0]
                
        t = self.trust(best)
        for o in options:
            nt = self.trust(o)
            if nt > t:
                best = o
                t = nt
        return best        
    
    # when this player is president and unlocks the special election,
    # this function returns which agent they choose to be president
    def pres_special(self,options):
        #don't pick Hitler
        random.shuffle(options)
        for op in options:
            if op.role=='H': continue
            return op
    
    def investigation(self,options):
        #randomly pick someone then lie about what their role is
        random.shuffle(options)
        return options[0], 'F' if options[0].role=='L' else 'L'
    
    def top_three(self,top):
        return top
        
    
    #use the history of the game to come up with a guess for the role of this player
    # as a fascist, we need to use this to gauge how much trust the liberals have of a player
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