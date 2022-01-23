class Action:

    ACTION_UPGRADE_ANIMAL = "Upgrade Animal"
    ACTION_BUY_PET_INTO_EMPTY_SLOT = "Buy Pet into Empty Slot"
    ACTION_FEED_ANIMAL = "Feed Animal"
    ACTION_REROLL_SHOP = "Reroll"
    ACTION_GO_TO_ARRANGE_TEAM_STEP = "Go to Arrange Team Step"
    ACTION_ARRANGE_TREAM = "Arrange Team"
    ACTION_END_TURN = "End Turn"

    def __init__(self, name, target=None, *args, **kwargs):
        self.name = name
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return f"({self.name}, {self.target}, {str(self.args)})"

    def __eq__(self, other):
        return self.name == other.name and self.target == other.target and self.args == other.args
