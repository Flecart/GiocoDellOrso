"""
Implements logic for the player.
"""
import pickle
import time
import numpy as np
import random

INFINITY = 1000000


class AbstractPlayer:
    """
    Abstract player class
    """
    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    def choose_action(self, state: str, actions: list[tuple[int, int]]) -> tuple[int, int]:
        """
        Choose an action
        """
        raise NotImplementedError


class AIPlayer(AbstractPlayer):
    """
    AI player class
    Uses some default values for the hyperparameters
    The values are

    exp_rate: float = 0.3
    alpha: float = 0.2
    gamma: float = 0.9
    training: bool = True

    If you want to modify it, pass the values as keyword arguments
    e.g. AIPlayer(name, exp_rate=0.5, alpha=0.5, gamma=0.5)
    """

    def __init__(self,
                 name: str,
                 maximize: bool,
                 **kwargs):
        super().__init__(name)
        self.states: list[str] = []  # record all positions taken
        self.exp_rate: float = (
            kwargs['exp_rate'] if kwargs.get('exp_rate') is not None else 0.3
        )
        self.alpha: float = (
            kwargs['alpha'] if kwargs.get('alpha') is not None else 0.2
        )
        self.gamma: float = (
            kwargs['gamma'] if kwargs.get('gamma') is not None else 0.9
        )

        self.training = kwargs['training'] if kwargs.get('training') is not None else True
        self.states_value: dict[str, int] = {}  # state -> value
        self.maximize = maximize

        self.old_times_trained = []
        self.old_exp_rate = []
        self.old_alpha = []
        self.old_gamma = []
        self.old_loss_reward = []
        self.old_win_reward = []
        self.old_opponent = []
        self.old_max_turns = []
        self.old_maximize = []

    def get_state_info(self, times_trained):
        data = dict()
        data['times_trained'] = self.old_times_trained + [times_trained]
        data['exp_rate'] = self.old_exp_rate + [self.exp_rate]
        data['alpha'] = self.old_alpha + [self.alpha]
        data['gamma'] = self.old_gamma + [self.gamma]
        data['maximize'] = self.old_maximize + [self.maximize]

        return data

    def save_policy(self, times_trained, max_turns, opponent):
        """
        Save the policy
        """

        curr_time = int(time.time())
        data = self.get_state_info(times_trained)
        data['opponent'] = self.old_opponent + [opponent]
        data['max_turns'] = self.old_max_turns + [max_turns]
        data['states_value'] = self.states_value.copy()

        with open(f'{str(self._name)}_{curr_time}.policy', 'wb') as file_write:
            pickle.dump(data, file_write)

    def load_policy(self, file):
        """Load the policy"""
        with open(file, 'rb') as file_read:
            data = pickle.load(file_read)
        self.states_value = data['states_value']
        self.old_times_trained = data['times_trained'] if 'times_trained' in data and data['times_trained'] is not None else []
        self.old_exp_rate = data['exp_rate'] if 'exp_rate' in data and data['exp_rate'] is not None else []
        self.old_alpha = data['alpha'] if 'alpha' in data and data['alpha'] is not None else []
        self.old_gamma = data['gamma'] if 'gamma' in data and data['gamma'] is not None else []
        self.old_opponent = data['opponent'] if 'opponent' in data and data['opponent'] is not None else []
        self.old_maximize = data['maximize'] if 'maximize' in data and data['maximize'] is not None else []
        self.old_max_turns = data['max_turns'] if 'max_turns' in data and data['max_turns'] is not None else []

    def choose_action(self, reachable_states: list[int], actions) -> int:
        """ Get the action to be taken """
        values = [(self.states_value[state], i) for i, state in enumerate(reachable_states)
            if self.states_value.get((state)) is not None]

        get_best_value = (lambda x: max(x, key=lambda x: x[0])[0]) \
            if self.maximize \
            else (lambda x: min(x, key=lambda x: x[0])[0])

        valid_actions = [idx for value, idx in values
            if value == get_best_value(values)]

        if len(valid_actions) == 0:
            best_choice = random.choice(np.arange(len(reachable_states)))
        else:
            best_choice = random.choice(valid_actions)

        print(best_choice)
        print(reachable_states, values)
        print(actions)
        print(f'AIPlayer {self._name} chose {actions[best_choice]}, state is {reachable_states[best_choice]} with value \
            {self.states_value[reachable_states[best_choice]] if self.states_value.get((reachable_states[best_choice])) is not None else 0}')
        return best_choice  

    def feed_reward(self,
        state:str,
        next_state: str,
        action_taken: tuple[int, int],
        actions: list[tuple[int, int]],
        reward: int):
        if self.states_value.get((state, action_taken)) is None:
            self.states_value[state, action_taken] = 0
        
        get_best_value = (lambda x: np.max(x)) \
            if self.maximize else (lambda x: np.min(x))
        try:
            old_max_value = get_best_value([
                self.states_value[next_state, action]
                for action in actions
                if self.states_value.get((next_state, action)) is not None
            ])
        except ValueError:  # probably empty array
            old_max_value = 0

        self.states_value[state, action_taken] += self.alpha * (
            reward + self.gamma * old_max_value -
            self.states_value[state, action_taken]
        )

class HumanPlayer(AbstractPlayer):
    """
    Human player class
    Represents a player controlled by a human
    """

    def choose_action(self, state: str, actions: tuple[int, int]):
        """ Get the action to be taken """
        while True:
            print('Available actions: ', actions)
            try:
                start = int(input('Enter the starting position: '))
                target = int(input('Enter the target position: '))
                action = (start, target)
                if action in actions:
                    return actions.index(action)
                else:
                    print('Invalid action, input a valid action')
            except ValueError:
                print('Invalid action')
