import random

'''
An agent is a player in a Secret Hitler game.
We expect a 'good' agent to successfully deduce
the roles of the other agents
'''
class Agent:
    def __init__(self,role,game):
        self.index = None #integer indicating index in SH_game.agents
        self.role = role # 'L': liberal, 'F': fascist, 'H': hitler
        self.is_dead = False
        self.game = game
    
    def get_role(self):
        return self.role
    
    # returns 1 if the agent approves of this pres/chanc pair (ja)
    # returns 0 if the agent disapproves of the pair (nein)
    def vote(self,president,chancellor):
        pass
    
    # this returns the available agent that this agent prefers when they are president
    def select_chancellor(self,options):
        pass
    
    # when this agent is president and gets the given hand (legislation),
    # this function returns which card the president would discard
    def pres_discard(self,chancellor,hand):
        pass
    
    # when this agent is president and gets the given hand,
    # this function the number of fascists they claimed to get
    def pres_claim(self,chancellor,hand):
        pass
    
    # when this agent is chancellor and gets the given hand (legislation),
    # this function returns which card the chancellor chooses to play
    def chancellor_pick(self,hand):
        pass
    
    # when this agent is chancellor and gets the given hand,
    # this function returns the number of fascists they claimed to get
    def chanc_claim(self,hand):
        pass
    
    # when veto power is unlocked and this agent is the president/chancellor,
    # this function returns True if they want to veto the hand, and False otherwise
    def veto(self,hand,is_pres):
        pass
    
    # when this player is president and a fascist is played so that they must kill someone,
    # this function returns which agent they choose to kill
    def kill(self,options):
        pass
    
    # when this player is president and unlocks the special election,
    # this function returns which agent they choose to be president
    def pres_special(self,options):
        pass
    
    # when this player is president and unlocks investigation,
    # this function returns which agent they choose to investigate (can't investigate self)
    # returns a tuple: integer 0 <= i < len(self.agents), and reported role of said agent
    def investigation(self,options):
        pass
    
    # president sees the top three cards
    # function returns what they report to have seen (list of 3 bits)
    def top_three(self,top):
        pass
    

#import extensions of agent
from RandomAgent import *
from GenericLiberalAgent import *
from GenericFascistAgent import *
from GenericHitlerAgent import *
from PassiveFascistAgent import *
from RiskLiberalAgent import *
from MixedLiberalAgent import *