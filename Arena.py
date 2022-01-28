from sapai import Player, Battle

import GameState
from GameState import *

from random import shuffle


class Arena:

    def __init__(self, num_players_per_ai: int, ai_list):
        self.num_players_per_ai = num_players_per_ai
        self.ai_list = ai_list
        self.active_game_states = dict()
        self.winners = dict()
        self.losers = dict()

        # Map an int (number to keep track of games) to a tuple of GameState and which AI is controlling it
        all_ais = ai_list * num_players_per_ai
        for i in range(len(all_ais)):
            new_gs = GameState(player=Player())
            self.active_game_states[i] = (new_gs, all_ais[i])

        turn_count = 1
        while len(self.active_game_states) > 3:
            print(f"Turn {turn_count}")
            print(f"Active: {len(self.active_game_states)}\nWinners: {len(self.winners)}\nLosers:{len(self.losers)}")
            self.store_phase_all_players()
            self.battle_phase_all_players()
            turn_count += 1

    def update_winners_and_losers(self, game_state_id):
        gs, ai = self.active_game_states[game_state_id]
        if gs.player.lives <= 0:
            self.active_game_states.pop(game_state_id)
            self.losers[game_state_id] = (gs, ai)
        elif gs.player.wins >= 10:
            self.active_game_states.pop(game_state_id)
            self.winners[game_state_id] = (gs, ai)

    # TODO : This method should be added to the Player class
    @staticmethod
    def player_fight_outcome(player: Player, outcome: str):
        if outcome == "win":
            player.lf_winner = True
        elif outcome == "draw":
            player.lf_winner = False
        elif outcome == "loss":
            player.lf_winner = False
            if player.turn <= 2:
                player.lives -= 1
            elif player.turn <= 4:
                player.lives -= 2
            else:
                player.lives -= 3

    @staticmethod
    def do_store_phase(gs: GameState, ai):
        gs.player.start_turn()

        while True:
            actions = gs.avail_actions()
            chosen_action = ai(gs, actions)
            gs.perform_action(chosen_action)

            if GameState.get_action_name(chosen_action) == "end_turn":
                return

    def do_battle_phase(self, game_state_id_1: int, game_state_id_2):
        player1 = self.active_game_states[game_state_id_1][0].player
        player2 = self.active_game_states[game_state_id_2][0].player

        battle = Battle(player1.team, player2.team)

        # TODO : FIND EXCEPTION BEING RAISED IN BATTLES
        winner = battle.battle()

        if winner == -1:
            raise RuntimeError("Battle did not complete")
        elif winner == 0:
            self.player_fight_outcome(player1, "win")
            self.player_fight_outcome(player2, "loss")
        elif winner == 1:
            self.player_fight_outcome(player1, "loss")
            self.player_fight_outcome(player2, "win")
        elif winner == 2:
            self.player_fight_outcome(player1, "draw")
            self.player_fight_outcome(player2, "draw")
        else:
            raise RuntimeError("Unknown battle outcome")

        self.update_winners_and_losers(game_state_id_1)
        self.update_winners_and_losers(game_state_id_2)

    def store_phase_all_players(self):
        for game_state, ai in self.active_game_states.values():
            self.do_store_phase(game_state, ai)

    def battle_phase_all_players(self):
        all_ids = [x for x in self.active_game_states.keys()]
        shuffle(all_ids)

        # Splits list into pairs
        # https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
        pairs = [all_ids[i:i + 2] for i in range(0, len(all_ids), 2)]

        for pair in pairs:
            # One team gets a bye if there's an odd number of teams
            if len(pair) == 1:
                continue
            game_state_id_1 = pair[0]
            game_state_id_2 = pair[1]
            self.do_battle_phase(game_state_id_1, game_state_id_2)

