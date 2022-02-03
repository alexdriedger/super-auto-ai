# Super Auto AI

This project is for creating AIs for Super Auto Pets. It uses [sapai](https://github.com/manny405/sapai) to run
simulations of Super Auto Pets.

## Installation

Install the dependencies `pip install -r requirements.txt`. It is recommended to use an environment (eg. venv or conda)

To refresh the installation when there's been an update to `sapai` use `pip install -I requirement.txt`

### Advanced Installation

To use a specific branch of `sapai` update the git requirement in `requirements.txt`

```
git+https://github.com/manny405/sapai.git@branch-name
```

## Arena

The `Arena` is a way to test different AI implementations against each other. It's arguments are the number of players
to create per AI, and list of AI functions.
An AI function will take in the `GameState` and the possible actions and returns the action which it chooses to play.

The simplest AI is the `random_agent` which randomly selects which actions to perform.

`main.py` is ready for testing and exploration. After installing dependencies, it can be run with `python main.py`

```py
# This will create and run an Arena with 50 random_agents and 50 random_agent_max_spend
# This will run until there are less than 3 players remaining
arena = Arena(50, [random_agent, random_agent_max_spend])
```
