import random
from Agent import *
from argparse import ArgumentParser
import sys, inspect
import importlib

'''
SH_Game is a class that step by step simulates the game of Secret Hitler
 - do_round() simulates one round of the game
 - records what happens during the game
 - supplies agents with appropriate info
'''
class SH_Game:
    #initialization
    def __init__(self):
        self.agents = []
        self.president = None
        self.last_candidate = None
        self.last_president = None
        self.last_chancellor = None
        self.election_tracker = 0
        self.deck = [] # liberal cards are 0, fascist cards are 1
        self.discard_pile = []
        self.lib_policy = 0  # counters for how many lib/fas policies have been played
        self.fas_policy = 0
        self.winner = None  # 'L' if liberals win and 'F' if fascists win
        self.win_method = None #report on how the winning team won
        self.can_veto = False
        self.special_election = False
        #this is a list of dictionaries that store info on all of the "game events"
        self.history=[]
    
    #called at the start of the game
    def new_game(self,player_count,lib_agnt,fas_agnt,hit_agnt):
        #general initialization
        self.__init__()
        #initialize the agents, with number of roles respective to game
        lib_count = 3 + int((player_count-4)/2)
        fas_count = 1 + int((player_count-5)/2)
        #liberals
        libs = [lib_agnt('L',self) for i in range(lib_count)]
        #fascists
        fasc = [fas_agnt('F',self) for i in range(fas_count)]
        #hitler
        self.agents = libs + fasc + [hit_agnt('H',self)]
        #have the agents sit in random order and update their indexes
        random.shuffle(self.agents)
        for i in range(player_count):
            self.agents[i].index = i
        #randomly select a first president
        self.president = self.agents[0]
        #put cards into the deck, no cards played yet; 6 liberal 11 fascist
        self.deck = [0 for _ in range(6)] + [1 for _ in range(11)]
        random.shuffle(self.deck)
        
    
    #getters
    #returns self.winner (None for in-progress game, L for libs, F for fascists)
    def win(self):
        return self.winner
    
    #returns a string explaining how the winners won: None if no winner
    def result(self):
        if self.winner==None: return None
        if self.lib_policy==5:
            return 'liberal cards'
        if self.fas_policy==6:
            return 'fascist cards'
        for agent in self.agents:
            if agent.role=='H' and agent.is_dead:
                return 'dead hitler'
        return 'elected hitler'
    
    #prints the history of the game in a readable format
    def print_game(self):
        #print the roles of every player
        for a in self.agents:
            if a.role=='F':
                print('*Player ' + str(a.index) + ' is a fascist.')
        for a in self.agents:
            if a.role=='H':
                print('*Player ' + str(a.index) + ' is Hitler.')
        print('')
        
        #print every sequential event in the game
        L = 0
        F = 0
        for event in self.history:
            e = event['event']
            p = None
            if 'president' in event: p=str(event['president'])
            if e=='election':
                print('There are ' + str(L) + ' liberal polcies and ' + str(F) + ' fascist policies that have been played.')
                print('Player '+p+' is the president and picks player '+str(event['chancellor'])+' for chancellorship.')
                print('Everyone votes on this pair: '+str(event['votes']))
                if event['result']!='failure':
                    print('The vote succeeds.')
                    if event['result']=='Hitler':
                        print('Hitler has been elected chancellor.')
                    else:
                        print('*The president picks up the cards: ' + str(event['pres_hand']))
                        print('*The chancellor receives the cards: ' + str(event['chanc_hand']))
                        if event['result']=='veto':
                            print('The president and chancellor agree to veto this hand.')
                        else:
                            print('A ' + ('fascist' if event['result']==1 else 'liberal') + ' policy is played by the chancellor.')
                            print('The president claims to have received: ' + str(event['pres_claim']))
                            print('The chancellor claims to have received: ' + str(event['chanc_claim']))
                            if event['result']==1: F += 1
                            else:                  L += 1                            
                else:
                    print('The vote fails.')
            if e=='breakfast':
                print('Three presidencies have failed in a row. The top card, a' + (' fascist' if event['card'] else ' liberal') + ', is played.')
                if event['card']: F += 1
                else:           L += 1
            if e=='reshuffle':
                print('The deck is reshuffled.')
            if e=='investigation':
                print('President ' + p + ' investigates player ' + str(event['invest']) + ' and claims they are ' + event['pres_claim']+'.')
            if e=='top three':
                print('President ' + p + ' looks at the top three cards and claims to see: ' + str(event['claim'])+'. *Actual: ' + str(event['cards']))
            if e=='special_election':
                print('Special Election: President ' + p + ' chooses player ' + str(event['new_pres']) + ' to be the next president.')
            if e=='kill':
                print('President ' + p + ' kills player ' + str(event['killed']) + '!')
            print('')#space between events
        
        #print the final game result
        print('Game Result: ' + game.result() + '\n')
        
    #setters
    #checks to see if we need to reshuffle the deck:
    # > when there are less than 3 cards available
    def reshuffle(self):
        #reshuffle check if need be
        if len(self.deck) < 3:       
            self.history += [{'event':'reshuffle'}]
            #combine discard pile into deck
            self.deck = self.deck + self.discard_pile
            self.discard_pile = []
            #shuffle deck
            random.shuffle(self.deck)
            return True
        return False
    
    #plays the given card
    def play_card(self,card):
        #if liberal card
        if card==0:
            self.lib_policy += 1
        #if fascist card
        else:
            self.fas_policy += 1
        #victory by cards played
        if self.lib_policy == 5:
            self.winner = 'L'
        if self.fas_policy == 6:
            self.winner = 'F'

    #called when an election fails or if veto power is used
    def increment_election_tracker(self):
        self.election_tracker += 1
        #third failed presidency
        if self.election_tracker==3:
            #randomly play top card, reset election traker, and reset 'term limits'
            card = self.deck.pop()
            self.history += [{'event':'breakfast','card':card}]
            self.play_card(card)
            self.election_tracker = 0  
            self.last_president = None
            self.last_chancellor = None
    
    #core game logic
    def do_round(self):
        N = len(self.agents)

        #assume this presidency will fail and then update otherwise        
        event= {'event':'election'}
        event['pres_hand']=event['pres_claim']=event['chanc_hand']=event['chanc_claim']=None
        event['result'] = 'failure'
        
		# if need be, reshuffle the deck before the round starts
        self.reshuffle()
        
		# the predetermined president selects a chancellor from the list of valid options,
        # and the whole group votes on this decision
        president = self.president
        event['president'] = president.index
        if not self.special_election:
            self.last_candidate = president
        #reset special election
        self.special_election = False
        #give the president his options for chancellor
        options = [a for a in self.agents]
        for a in self.agents:
            # NOTE: last elected president may be available depending on number of players
            if a.is_dead or a==president or a == self.last_chancellor or (sum([0 if agnt.is_dead else 1 for agnt in self.agents])>5 and a == self.last_president):
                options.remove(a)
        chancellor = president.select_chancellor(options)
        event['chancellor'] = chancellor.index
        votes = []
        for agent in self.agents:
            if not agent.is_dead:
                votes.append(agent.vote(president,chancellor))
            else:
                votes.append(0)
        event['votes'] = votes
        
        pick = None
        #successful presidency: most living people voted yes
        if sum(votes) > sum([0 if a.is_dead else 1 for a in self.agents])/2:
            #update last president/chancellor
            self.last_president = president
            self.last_chancellor = chancellor
            self.election_tracker = 0
            # when at least three fascist cards have been played,
            # fascists can win by electing hitler as chancellor
            if self.fas_policy >= 3 and chancellor.role=='H':
                #the chancellor is hiter -> fascists win
                self.winner = 'F'
                event['result'] = 'Hitler'
                self.history += [event]
            else:
                #do legislation: president gets top three cards
                hand = [self.deck.pop() for _ in range(3)]
                event['pres_hand'] = [x for x in hand] #copy list
                #store president's claim
                p_claim = president.pres_claim(chancellor,hand)
                event['pres_claim'] = p_claim
                #president discards one of these cards
                pick = president.pres_discard(chancellor,hand)
                hand.remove(pick)
                self.discard_pile.append(pick)
                event['chanc_hand'] = [x for x in hand] #copy list
                #store chancellor's claim
                c_claim = chancellor.chanc_claim(hand)
                event['chanc_claim'] = c_claim
                pick = None         
                #if veto power is unlocked then the chancellor and president
                #can agree to play neither of the policies: end of round
                if self.can_veto and president.veto(hand,True) and chancellor.veto(hand,False):
                    event['result'] = 'veto' #no card is played
                    self.discard_pile += hand
                    self.increment_election_tracker()
                else:
                    #chancellor picks one of the two remaining cards, discards the other
                    pick = chancellor.chancellor_pick(hand)
                    event['result'] = pick            
                    hand.remove(pick)
                    self.discard_pile += hand
                    self.play_card(pick)
                
                #add this election & legislation to the history of events
                self.history += [event]
                
                #if a fascist card is played, account for president powers
                if pick == 1:
                    #small game president powers
                    if N < 7:
                        self.reshuffle()
                        #look at top three cards
                        if self.fas_policy==3:
                            top = self.deck[-3:]
                            claim = president.top_three(top)
                            self.history += [{'event':'top three',
                                              'cards':[x for x in top],
                                              'president':president.index,
                                              'claim':claim}]
                    #large game president powers
                    else:
                        #investigation
                        #in very large game 9-10, first fascist played results in an investigation
                        if (N > 8 and self.fas_policy==1) or self.fas_policy==2:
                            ops = [a for a in self.agents]
                            ops.remove(president)
                            invest,claim = president.investigation(ops)
                            accusation = 0
                            if claim=='L': accusation = 1
                            if claim=='F': accusation = 2
                            actual = 1
                            if invest.get_role()=='L': actual = 0
                            self.history += [{'event':'investigation',
                                              'president':president.index,
                                              'invest':invest.index,
                                              'pres_claim':claim}]
                        #special election
                        if self.fas_policy==3:
                            #the president select another player to be president for the next round
                            ops = []
                            for agent in self.agents:
                                if agent.is_dead or agent==president: continue
                                ops.append(agent)
                            self.president = president.pres_special(ops)
                            self.special_election = True
                            # add special election to history of events
                            self.history += [{'event':'special_election',
                                              'president':president.index,
                                              'new_pres':self.president.index}]
                    #general game powers
                    #kill
                    if self.fas_policy==4 or self.fas_policy==5:
                        ops = []
                        for agent in self.agents:
                            if not agent.is_dead:
                                ops.append(agent)
                        kill = president.kill(ops)
                        kill.is_dead = True
                        self.history += [{'event':'kill',
                                          'president':president.index,
                                          'killed':kill.index}]
                        #if hitler is killed, liberals win
                        if kill.role=='H':
                            self.winner ='L'
                    #veto power unlocked
                    if self.fas_policy==5:
                        self.can_veto = True
        #failed presidency
        else:
            self.history += [event]
            self.increment_election_tracker()
        # shift presidency left of last candidate for presidency
        if not self.special_election:
            #dead people can't be president!
            index = (self.last_candidate.index - 1)%N
            while self.agents[index].is_dead:
                index = (index - 1)%N
            self.president = self.agents[index]
        return None
    
    #looping of core game logic until a victor is found
    def play_game(self):
        while not self.win():
            self.do_round()
        return self.win()

if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument("-l", "--liberal", required=False, default='GenericLiberalAgent', help="The agent (strategies) to be used by all liberal players.")
    parser.add_argument("-f", "--fascist", required=False, default='GenericFascistAgent', help="The agent (strategies) to be used by all fascist players.")
    parser.add_argument("-r", "--hitler", required=False, default='GenericHitlerAgent', help="The agent (strategies) to be used by Hitler.")
    parser.add_argument("-p", "--numPlayers", required=False, default=5, help="The number of players in the game [5-10].", type=int, choices={5,6,7,8,9,10})
    parser.add_argument("-n", "--numGames", required=False, default=1, help="The number of games to run. Running a single game will print out the event details of that game.", type=int)
    parser.add_argument("-a", "--all", required=False, default='false', help="Iterates over all possible number of players [5-10], as opposed to just a specific number of players", choices={'true', 'false'})
    args = parser.parse_args()
    
    game = SH_Game()
    
    if(args.liberal != GenericLiberalAgent and args.liberal not in sys.modules.keys()):
        raise ValueError('The optional arugment [liberal] must be an already included module')
    if(args.fascist != GenericFascistAgent and args.fascist not in sys.modules.keys()):
        raise ValueError('The optional arugment [fascist] must be an already included module')
    if(args.hitler != GenericHitlerAgent and args.hitler not in sys.modules.keys()):
        raise ValueError('The optional arugment [hitler] must be an already included module')
    if(args.numGames < 1):
        raise ValueError('Cannot run a non-positive number of games')
    
    # Convert all the input strings into instances of that agent
    module = importlib.import_module(args.liberal)
    class_ = getattr(module, args.liberal)
    l_a = class_
    
    module = importlib.import_module(args.fascist)
    class_ = getattr(module, args.fascist)
    f_a = class_
    
    module = importlib.import_module(args.hitler)
    class_ = getattr(module, args.hitler)
    h_a = class_
    
    N = args.numGames #N=1 to view a game, N=10000 for testing

    P = args.numPlayers
    
    for p in range(5,11):
        if args.all == 'false':
            if p != P:
                continue
        records = []
        result = []        

        for i in range(N):
            game.new_game(p, l_a, f_a, h_a)
            records.append(game.play_game())
            result.append(game.result())            
        if N == 1 and args.all == 'false':
            game.print_game()
        if N>1 or (N==1 and args.all == 'true'):
            print('with '+str(p)+' players, fascists win: '+str(sum([1 if x=='F' else 0 for x in records])/N))
            print('percent of the time')
            print('liberals win with cards: ' + str(sum([1 if x=='liberal cards'  else 0 for x in result])/N))
            print('fascists win with cards: ' + str(sum([1 if x=='fascist cards'  else 0 for x in result])/N))
            print('liberals kill hitler:    ' + str(sum([1 if x=='dead hitler'    else 0 for x in result])/N))
            print('fascists elect hitler:   ' + str(sum([1 if x=='elected hitler' else 0 for x in result])/N))