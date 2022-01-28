import GameState
from random import choice


def random_agent(game_state: GameState, actions):
    return choice(actions)


def random_agent_max_spend(game_state: GameState, actions):
    if len(actions) == 1:
        return actions[0]
    return choice(actions[1:])


