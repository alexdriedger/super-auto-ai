from sapai import Player, Food
from sapai.data import data
from Action import *

import itertools


# TODO : RESOLVE ACTION HELPER METHOD


def get_possible_actions(player: Player) -> set[Action]:
    team = player.team
    shop = player.shop

    possible_actions = set()

    # This action is considered the effective end of buying things from the shop and can be considered equivalent to end
    # turn. Multiple rearrangements are not allowed to prevent infinite loops
    possible_actions.add(Action(Action.ACTION_GO_TO_ARRANGE_TEAM_STEP))

    # Freezing & Unfreezing actions are not implemented yet to prevent infinite loops in agents
    if player.gold < 0:
        raise RuntimeError("Getting possible actions with negative money")

    if player.gold == 0:
        return possible_actions

    # Re-roll
    possible_actions.add(Action(Action.ACTION_REROLL_SHOP))

    for slot in shop.shop_slots:
        if slot.cost > player.gold:
            continue

        # Feed animals
        if slot.slot_type == "food":
            food_to_buy = slot.item
            if is_food_multi_target(food_to_buy):
                possible_actions.add(Action(Action.ACTION_FEED_ANIMAL, None, food_to_buy))
            else:
                for ts in team:
                    possible_actions.add(Action(Action.ACTION_FEED_ANIMAL, ts.pet, food_to_buy))

        # Buy animals
        if slot.slot_type == "pet" or slot.slot_type == "levelup":
            shop_pet = slot.item
            if len(team) < team.max_slots:
                possible_actions.add(Action(Action.ACTION_BUY_PET_INTO_EMPTY_SLOT, None, shop_pet))
            for ts in team:
                if ts.pet.name == shop_pet.name:
                    possible_actions.add(Action(Action.ACTION_UPGRADE_ANIMAL, ts.pet, shop_pet, pet_is_from_shop=True))

    # Upgrade animals on team (not from shop)
    for index, ts in enumerate(team):
        cur_pet = ts.pet.name
        for inner_index, inner_ts in enumerate(team, start=index + 1):
            other_pet = inner_ts.pet.name
            if cur_pet == other_pet:
                possible_actions.add(Action(Action.ACTION_UPGRADE_ANIMAL, cur_pet, other_pet, pet_is_from_shop=False))

    return possible_actions


def is_food_multi_target(food: Food) -> bool:
    fd = data["foods"][food.name]["ability"]["effect"]["target"]
    return "n" in fd


def get_all_reorders(length: int) -> list[tuple]:
    if length < 0:
        raise RuntimeError("Getting reorderings with negative length of team")

    if length == 0:
        return list()

    base = list(range(length))
    return list(itertools.permutations(base, length))
