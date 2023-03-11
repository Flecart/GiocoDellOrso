"""
This module is used as board abstraction for the game.
"""

from player import AbstractPlayer, AIPlayer
from tqdm import tqdm
import pickle

# The values encode the character string for these
# players in the game board
# DO NOT CHANGE THESE VALUES ~~~~> THEY ARE USED IN THE GAME LOGIC (Many assumptions on these values)
HUNTER = 0
BEAR = 1


DEFAULT_HUNTER_POSITION = [0, 1, 2]
DEFAULT_BEAR_POSITION = [20]
BOARD_SIZE = 21

class Board:
    """
    Board abstraction, represents a board in the bear game
    The default char should not be equal to the char of Hunter or Bear
    """
    adjacent = [[1, 2, 3],  # 0
                [0, 3, 4],
                [0, 3, 6],  # 2
                [0, 1, 2, 5],
                [1, 7, 8],  # 4
                [3, 9, 10, 11],
                [2, 12, 13],  # 6
                [4, 8, 14],
                [7, 4, 14, 9],  # 8
                [8, 10, 5, 15],
                [5, 9, 11, 15],  # 10
                [5, 10, 15, 12],
                [11, 6, 16, 13],  # 12
                [6, 12, 16],
                [7, 8, 18],  # 14
                [9, 10, 11, 17],
                [12, 13, 19],  # 16
                [15, 18, 19, 20],
                [14, 17, 20],  # 18
                [16, 17, 20],
                [18, 17, 19]]

    def __init__(self, default_char='_'):
        self._default_char = default_char
        self._hunters = [0, 1, 2]
        self._bear = [20]
        self._last_action = []

    def __str__(self):
        string_rep = [self._default_char] * 21
        for i in self._hunters:
            string_rep[i] = "0"
        for i in self._bear:
            string_rep[i] = "1"

        return "".join(string_rep)

    def get_hash(self) -> str:
        """ 
        get hash of the board, this is not a proper hash, as
        it's easy to convert it back to the board, just an encoding, but
        i want to keep this name.
        """
        val = 0
        for i in self._hunters:
            val += (HUNTER + 1) * 3 ** i
        for i in self._bear:
            val += (BEAR + 1) * 3 ** i

        return val

    @staticmethod
    def str_from_hash(hash: int) -> str:
        """ get string from hash """
        def get_char(val: int):
            if val == 0:
                return '_'
            elif val == HUNTER + 1:
                return '0'
            elif val == BEAR + 1:
                return '1'
            else:
                raise ValueError("Invalid value")

        str = ""
        for _ in range(21):
            str += get_char(hash % 3)
            hash = hash // 3

        return str

    def get_all_states(self) -> list[int]:
        """ get all possible states """
        states = set()

        original_hunter = self._hunters
        original_bear = self._bear

        for hunter_0 in range(19):
            for hunter_1 in range(hunter_0 + 1, 20):
                for hunter_2 in range(hunter_1 + 1, 21):
                    for bear in range(21):
                        if bear not in [hunter_0, hunter_1, hunter_2]:
                            self._hunters = [hunter_0, hunter_1, hunter_2]
                            self._bear = [bear]
                            states.add(self.get_hash())
        self._hunters = original_hunter
        self._bear = original_bear

        return list(states)

    @staticmethod
    def reachable_states(state, actions: list[tuple[int, int]]) -> list[int]:
        """ get reachable states from a state """
        states = []
        for action in actions:
            states.append(Board.apply_action_state(state, action))

        return states

    def reset(self) -> None:
        self._hunters = [0, 1, 2]
        self._bear = [20]
        self._last_action = []

    def apply_action(self, action: tuple[int, int]):
        """ apply action to the board 
            Represents a move from action[0] to action[1]
            from a player.
        """
        print(action, self._hunters, self._bear)
        for i, val in enumerate(self._hunters):
            if val == action[0]:
                self._hunters[i] = action[1]
                break
        
        for i, val in enumerate(self._bear):
            if val == action[0]:
                self._bear[i] = action[1]
                break
        print(action, self._hunters, self._bear)

        self._last_action += [action]
    
    @staticmethod
    def apply_action_state(state: int, action: tuple[int, int]) -> int:
        start, end = action
        copy_state = state
        if start > 0:
            copy_state = copy_state // (3 ** (start))

        value = copy_state % 3
        return state - value * (3 ** start) + value * (3 ** end)
    
    def undo_action(self):
        """ undo last action """
        action = self._last_action[-1]

        for i, val in enumerate(self._hunters):
            if val == action[1]:
                self._hunters[i] = action[0]
                break
        
        for i, val in enumerate(self._bear):
            if val == action[1]:
                self._bear[i] = action[0]
                break
        self._last_action = self._last_action[:-1]

    @staticmethod
    def get_actions_state(state, is_hunter: bool) -> list[tuple[int, int]]:
        hunters = []
        bear = []
        for i in range(0, 21):
            val = state % 3
            if val == HUNTER + 1:
                hunters.append(i)
            elif val == BEAR + 1:
                bear.append(i)
            state = state // 3

        actions = []
        
        if is_hunter:
            it_vector = hunters
        else:
            it_vector = bear

        for i in it_vector:
            for target in Board.adjacent[i]:
                if target not in bear and target not in hunters:
                    actions.append((i, target))

        return actions


    def get_actions(self, player_val: int) -> list[tuple[int, int]]:
        """ 
        Returns list of available actions (starting_position, target_position) 
        We are sure that the end location is empty
        """
        actions = []
        
        if player_val == HUNTER:
            it_vector = self._hunters
        elif player_val == BEAR:
            it_vector = self._bear
        else:
            raise ValueError("Invalid player value")        

        for i in it_vector:
            for target in self.adjacent[i]:
                if target not in self._bear and target not in self._hunters:
                    actions.append((i, target))

        return actions

    def get_default_char(self) -> str:
        """ get default character """
        return self._default_char

    def display(self, cells=None):
        if cells is None:
            cells = str(self)
        print("            "+cells[0]+"            ","             "+"0"+"            ")
        print("        "+cells[1]+"       "+cells[2]+"        ","         "+"1"+"       "+"2"+"        ")
        print("            "+cells[3]+"            ","             "+"3"+"            ")
        print("  "+cells[4]+"         "+cells[5]+"         "+cells[6]+"  ","   "+"4"+"         "+"5"+"         "+"6"+"  ")
        print(""+cells[7]+"   "+cells[8]+"   "+cells[9]+"   "+cells[10]+"   "+cells[11]+"   "+cells[12]+"   "+cells[13]+"",
              " "+"7"+"   "+"8"+"   "+"9"+"  "+"10"+"  "+"11"+"  "+"12"+"  "+"13"+"")
        print("  "+cells[14]+"         "+cells[15]+"         "+cells[16]+"  ","  "+"14"+"        "+"15"+"        "+"16"+"")
        print("            "+cells[17]+"            ","            "+"17"+"            ")
        print("        "+cells[18]+"       "+cells[19]+"        ","        "+"18"+"      "+"19"+"        ")
        print("            "+cells[20]+"            ","            "+"20"+"            ")


class Game:
    """
    Game abstraction
    """

    # all ends states, base 3 encoded
    # 2 = bear, 1 = hunter, 0 = empty
    end_states = [41, 775, 2127231, 46767537, 
        1250480673, 5983494219, 8652390921, 
        4395548511, 396995175, 4793985, 8913, 115]

    VISITED = 0
    BEAR_WIN = 1
    HUNTER_WIN = 2

    def __init__(self,
            board: Board,
            player0: AbstractPlayer,
            player1: AbstractPlayer,
            display_board: bool = False,
            max_turns: int = 40):
        self._board = board
        self._hunter_player: AbstractPlayer = player0
        self._bear_player: AbstractPlayer = player1
        self._display_board: bool = display_board
        self._turn: int = 0
        self._max_turns: int = max_turns
        self._winner: 0 | 1 | 2 = None
        self.visited_states = [dict(), dict()]
        self.unexplored_states = [list(), list()]

        self.reset()

    def has_ended(self) -> bool:
        """
        Check if the game has ended
        """
        if self._board.get_hash() in self.end_states:
            return True
        elif self._turn >= self._max_turns:
            return True
        else:
            return False

    def print_winner(self) -> None:
        """
        Print the winner of the game
        """
        if not self.has_ended():
            print("The game has not ended yet")
            return

        if self._winner == HUNTER:
            print(f"The hunter won! turns to win -> {self._turn}")
        elif self._winner == BEAR:
            print("The bear won!")

    def play(self) -> int:
        """
        Main game loop, continues to play until the game has ended
        and gives the reward to the AI players
        """
        curr_player = self._hunter_player
        player_num = HUNTER

        while True:
            if self._display_board:
                self._board.display()

            board_state = self._board.get_hash()
            actions = self._board.get_actions(player_num)
            action_idx = curr_player.choose_action(
                Board.reachable_states(board_state, actions),
                actions
            )
            action = actions[action_idx]
            self._board.apply_action(action)

            if self.has_ended():
                if self._turn >= self._max_turns:
                    self._winner = BEAR
                else:
                    self._winner = HUNTER

            if self._winner is not None:
                break
            
            # update for next player
            player_num += 1
            if player_num == 2:
                self._turn += 1
                player_num = 0

            if player_num == 1:
                curr_player = self._bear_player
            else:
                curr_player = self._hunter_player

        return self._winner

    def train(self, n_times: int = 100) -> None:
        """
        Train the players and save the created policies
        into files
        """

        hunter_wins = 0
        for _ in tqdm(range(n_times)):
            self.play()
            if self._winner == HUNTER:
                hunter_wins += 1
            self.reset()

        self._hunter_player.save_policy(
            n_times,
            self._max_turns,
            self._bear_player.get_state_info(n_times)
        )
        self._bear_player.save_policy(
            n_times,
            self._max_turns,
            self._hunter_player.get_state_info(n_times)
        )
        print(f"Training done, saved policies, {n_times} games played \n \
            Number of hunter wins: {hunter_wins}")

    def calculate_deterministic_state_value(self) -> None:
        """
        This uses a recursive algoritmh to calculate how many moves are
        need for the Hunter to win, for the bear to lose, in a sure way.
        We define recursively two data structures:
        hunter(states) -> the number of moves needed for the hunter to win
        bear(states) -> the number of moves needed for the bear to lose

        bear(states for states in endstates): is initialized as 0 as
        the bear has already lost if it's in an end state.

        The recursively we define:
        for each state:
            if turn is hunter turn:
                if we can reach a state where the we know the bear will lose:
                    add this state to the hunter(states) data structure with current distance
            if turn is bear turn:
                if all reachable states are states where the bear will lose:
                    add this state to the bear(states) data structure with current distance

        This is a very easy to understand algorithm, but i haven't still analyzed it.
        We would need a theorem that states that all unexplored states will be marked.
        Assuming this, the algorithm works in O(n^2), with n the number of states.
        As the sweept through all non visited states, max nonvisited number of state times.
        """
        self.reset()

        curr_dist = 1
        has_changed = True
        while has_changed:
            if curr_dist % 2 == 1:  # hunter
                has_changed = self.find_hunter_states(curr_dist)
            else:
                has_changed = self.find_bear_states(curr_dist)
            print(f"""{curr_dist=}, bear: {len(self.visited_states[HUNTER])}, hunter: {len(self.visited_states[BEAR])}, has changed: {has_changed}""")
            curr_dist += 1

        print("Saving the states values")
        data_bear = dict()
        data_bear['states_value'] = self.visited_states[BEAR]

        data_hunter = dict()
        data_hunter['states_value'] = self.visited_states[HUNTER]
        with open(f'bear_policy.pickle', 'wb') as handle:
            pickle.dump(data_bear, handle)

        with open(f'hunter_policy.pickle', 'wb') as handle:
            pickle.dump(data_hunter, handle)
        print("Done, states saved")

    def find_bear_states(self, curr_dist: int) -> bool:
        state_to_add = []
        for state in self.unexplored_states[HUNTER]:
            reachable_states = Board.reachable_states(state, 
                Board.get_actions_state(state, is_hunter=False))
            
            is_new_state = all(curr_state in self.visited_states[BEAR] for curr_state in reachable_states)
            if is_new_state:
                state_to_add.append(state)

        if len(state_to_add) == 0:
            return False

        for state in state_to_add:
            self.visited_states[HUNTER][state] = curr_dist
            self.unexplored_states[HUNTER].remove(state)

        return True

    def find_hunter_states(self, curr_dist: int) -> bool:
        state_to_add = []
        for state in self.unexplored_states[BEAR]:
            reachable_states = Board.reachable_states(state, 
                Board.get_actions_state(state, is_hunter=True))

            is_new_state = any(curr_state in self.visited_states[HUNTER] for curr_state in reachable_states)
            if is_new_state:
                state_to_add.append(state)

        if len(state_to_add) == 0:
            return False

        for state in state_to_add:
            self.visited_states[BEAR][state] = curr_dist
            self.unexplored_states[BEAR].remove(state)

        return True

    def reset(self) -> None:
        """
        Reset the game variables to their default values
        """
        self._turn = 0
        self._board.reset()
        self._winner = None
        self.visited_states = [dict(), dict()]
        self.unexplored_states = [list(), list()]
        for end_state in self.end_states:
            self.visited_states[HUNTER][end_state] = 0

        self.unexplored_states[BEAR] = self._board.get_all_states()
        self.unexplored_states[HUNTER] = [x for x in self._board.get_all_states() if x not in self.end_states]
