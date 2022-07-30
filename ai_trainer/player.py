"""
Implements logic for the player.
"""
import pickle
import time
import random
import board as brd

INFINITY = 1000000

class AbstractPlayer:
    """
    Abstract player class
    """
    def __init__(self, positions: list[int], name: str, symbol: str):
        self._default_positions = positions.copy()
        self._positions = positions
        self._name = name
        self._symbol = symbol

    def get_name(self) -> str:
        """name getter"""
        return self._name

    def get_symbol(self) -> str:
        """symbol getter"""
        return self._symbol

    def get_actions(self, board: brd.Board) -> list[tuple[int, int]]:
        """
        Get the actions available to the player
        """
        actions = [] 
        for i in range(len(self._positions)):
            if board[self._positions[i]] == self._symbol:
                for j in brd.Board.adjacent[self._positions[i]]:
                    if board[j] == board.get_default_char():
                        actions.append((self._positions[i], j))
        return actions

    def get_action(self, actions: tuple[int, int], board: brd.Board) -> int:
        """
        Get the action to be performed by the player
        """
        raise NotImplementedError

    def reset(self) -> None:
        """
        Reset the player
        """
        self._positions = self._default_positions.copy()
        return

    def update_position(self, action: tuple[int, int]) -> None:
        """
        Update the position of the player
        """

        for i in range(len(self._positions)):
            if self._positions[i] == action[0]:
                self._positions[i] = action[1]
                break


    def move(self, board: brd.Board, action = None) -> tuple[int, int]:
        """
        Move the player
        action is a tuple of (starting_position, target_position)
        """
        if action is None:
            actions = self.get_actions(board)
            action = self.get_action(actions, board)
        board[action[1]] = self._symbol
        board[action[0]] = board.get_default_char()
        self.update_position(action)

        return action
class AIPlayer(AbstractPlayer):
    """
    AI player class
    """
    def __init__(self,
            positions: list[int],
            name: str,
            symbol: str,
            **kwargs):
        super().__init__(positions, name, symbol)

        self.states: list[str] = []  # record all positions taken
        self.exp_rate: float = kwargs['exp_rate'] if kwargs.get('exp_rate') is not None else 0.3
        self.alpha: float = kwargs['alpha'] if kwargs.get('alpha') is not None else 0.2
        self.gamma: float = kwargs['gamma'] if kwargs.get('gamma') is not None else 0.9
        self.states_value: dict[str, int] = {}  # state -> value

    def save_policy(self):
        """
        Save the policy
        """
        curr_time = int(time.time()) 
        with open(f'{str(self._name)}_{curr_time}.policy', 'wb') as file_write:
            pickle.dump(self.states_value, file_write)

    def load_policy(self, file):
        """Load the policy"""
        with open(file, 'rb') as file_read:
            self.states_value = pickle.load(file_read)

    def get_action(self, actions: tuple[int, int], board: brd.Board):
        """ Get the action to be taken """
        if random.uniform(0, 1) <= self.exp_rate:
            idx = random.randrange(0, len(actions))
            action = actions[idx]
        else:
            value_max = -INFINITY
            for act in actions:
                self.move(board, act)
                state_value = self.states_value.get(board.get_hash())
                if state_value is None:
                    value = 0
                else:
                    value = state_value

                if value >= value_max:
                    value_max = value
                    action = act

                self.move(board, (act[1], act[0]))

        return action

    # append a hash state
    def add_state(self, state: str):
        """Add a state to the list of states"""
        self.states.append(state)

    # at the end of game, backpropagate and update states value
    def feed_reward(self, reward: float):
        """ Feed the reward to the player """
        for state in reversed(self.states):
            if self.states_value.get(state) is None:
                self.states_value[state] = 0
            self.states_value[state] += self.alpha * (self.gamma * reward -
                self.states_value[state])
            reward = self.states_value[state]

    def reset(self):
        """ Reset the player """
        super().reset()
        self.states = []


class HumanPlayer(AbstractPlayer):
    """
    Human player class
    TODO: this is not tested yet
    """

    def get_action(self, actions: tuple[int, int], board: brd.Board):
        """ Get the action to be taken """
        while True:
            try:
                action = int(input('Enter your action: '))
                if action in actions:
                    return action
                else:
                    print('Invalid action')
            except ValueError:
                print('Invalid action')