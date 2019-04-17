# Secret Hitler Strategy Analysis

## Background

[Wikipedia](https://en.wikipedia.org/wiki/Secret_Hitler)

[Official Rules](https://secrethitler.com/assets/Secret_Hitler_Rules.pdf)

[Online Adaptation](https://secrethitler.io/) 

## Running the Simulation

`secret_hitler.py` This is the main file which runs the program, which takes the following *optional* arguments

- `-h` Provides a guide of commands

- `-l` or `--liberal` Selects the agent (set of strategies) that all liberal players will follow in any iteration of the game (*Defualt*: GenericLiberalAgent)

- `-f` or `--fascist` Selects the agent (set of strategies) that all fascist players will follow in any iteration of the game (*Defualt*: GenericFascistAgent)

- `-r` or `--hitler` Selects the agent (set of strategies) that Hitler will follow in any iteration of the game (*Defualt*: GenericHitlerAgent)

- `-p` or `--numPlayers` Selects the number of players in any iteration of the game (*Default*: 5, *Range*:{5,6,7,8,9,10}, *Note*: Overriden if the `--all` option is True)

- `-n` or `--numGames` Selects the number of iterations/games that the program will run for (*Default*: 1, *Note*: Running a single game will print out the event details of that game.)

- `-a` or `--all` Gives the option to run through all possible number of players in the game [5-10], as opposed to only a single number of players.

### Examples

`python secret_hitler.py -a True -n 100 -l MixedLiberalAgent -f PassiveFascistAgent -r GenericHitlerAgent`

Runs through 100 games for all number of players (total of 600 games, 100 for each number of players), and uses the MixedLiberalAgent as the liberal strategy, PassiveFascistAgent as the fascist strategy, and GenericHitlerAgent as the Hitler strategy

`python secret_hitler.py -n 1 -f PassiveFascistAgent`

Runs through a single game, with detailed output, using PassiveFascistAgent as the fascist strategy.

## Agents

Agents can be specified by the 12 actions they might be faced with during a game. They include voting, selecting discard pile cards, choosing their chancellor, and special abilities.

We have specified the following agents:

- `RandomAgent` Chooses randomly over all given options for each action.
- `GenericLiberalAgent` Uses a Trust system to try and make informed decisions. For example, this agent chooses the player with the highest trust value when selecting a chancellor.
	- `RiskLiberalAgent` Follows most TrustLiberalAgent strategies, except as a president given 2 Liberals and 1 Fascist, they will give the chancellor a choice. This might provide information about players that would otherwise go undiscovered.
	- `MixedLiberalAgent` Follows most TrustLiberalAgent strategies, except as a president given 2 Liberals and 1 Fascist, they will give the chancellor a choice as long as the liberals are winning and forcing a liberal would not win the game.
- `GenericFascistAgent` Makes intuitive fascist plays, such as playing fascist policies when available.
	- `PassiveFascistAgent` Follows most GenericFascistAgent strategies, except it tries to gain trust (by playing liberal policies) when the fascists are already ahead.
- `GenericHitlerAgent` Follows most GenericLiberalAgent strategies to avoid suspicision. However, in certain cases, making a fascist play would win the game, and this agent will take those actions.
