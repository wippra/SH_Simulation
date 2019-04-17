from Agent import *

#implementation of agent that acts completely randomly whenever given a choice
class RandomAgent(Agent):
    
    def vote(self,president,chancellor):
        return 1 if random.random() < 0.5 else 0
    
    #pick the most trusted available player
    def select_chancellor(self,options):
        random.shuffle(options)
        return options[0]
    
    def pres_discard(self,chancellor,hand):
        random.shuffle(hand)
        return hand[0]
    
    def chancellor_pick(self,hand):
        random.shuffle(hand)
        return hand[0]
    
    def veto(self,hand,is_pres):
        return True if random.random() < 0.5 else False
    
    def kill(self,options):
        random.shuffle(options)
        return options[0]
    
    def pres_special(self,options):
        random.shuffle(options)
        return options[0]
    
    def investigation(self,options):
        random.shuffle(options)
        return options[0],'L' if random.random() < 0.5 else False
    
    def top_three(self,top):
        return None