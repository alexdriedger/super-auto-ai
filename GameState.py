from sapai import Player
from sapai.agents import CombinatorialSearch


class GameState:

    def __init__(self, player: Player = None, just_froze: bool = False, just_reordered: bool = False):
        self.player = player
        self.just_froze = just_froze
        self.just_reordered = just_reordered

    @property
    def state(self):
        state_dict = {
            "type": "GameState",
            "player": self.player,
            "just_froze": self.just_froze,
            "just_reordered": self.just_reordered
        }
        return state_dict

    @classmethod
    def from_state(cls, state):
        player = Player.from_state(state["player"])
        just_froze = state["just_froze"]
        just_reordered = state["just_reordered"]
        return cls(player=player, just_froze=just_froze, just_reordered=just_reordered)

    @staticmethod
    def avail_roll(player_to_check: Player):
        action_list = []
        if player_to_check.gold > 1:
            action_list.append((player_to_check.roll,))
        return action_list

    @staticmethod
    def avail_end_turn(player_to_check: Player):
        return [(player_to_check.end_turn,)]

    @staticmethod
    def get_action_name(input_action):
        return str(input_action[0].__name__)

    def avail_actions(self):
        player = self.player
        cs = CombinatorialSearch()

        action_list = []
        action_list += self.avail_end_turn(player)
        action_list += CombinatorialSearch.avail_buy_pets(cs, player)
        action_list += CombinatorialSearch.avail_buy_food(cs, player)
        action_list += CombinatorialSearch.avail_buy_combine(cs, player)
        action_list += CombinatorialSearch.avail_team_combine(cs, player)
        action_list += CombinatorialSearch.avail_sell(cs, player)
        action_list += CombinatorialSearch.avail_sell_buy(cs, player)
        action_list += self.avail_roll(player)
        # if not self.just_reordered:
        #     action_list += CombinatorialSearch.avail_team_order(cs, player)
        # TODO : FREEZE LIST
        return action_list

    def perform_action(self, input_action):
        player_to_act = self.player
        action_name = self.get_action_name(input_action).split(".")[-1]
        action = getattr(player_to_act, action_name)
        try:
            action(*input_action[1:])
        except Exception as e:
            # if e.__str__().__contains__("Buy food must input food"):
            from pprint import pprint
            print("Found bad state")
            print(f"Bad action: {action_name}")
            print(action)
            print("State")
            pprint(self.player.state)
            import traceback
            tb = traceback.format_exc()
            print(tb)
            raise e
