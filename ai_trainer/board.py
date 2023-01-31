"""
This module is used as board abstraction for the game.
"""

from player import AbstractPlayer, AIPlayer
from tqdm import tqdm
import pickle

# The values encode the character string for these
# players in the game board
HUNTER = 0
BEAR = 1


DEFAULT_HUNTER_POSITION = [0, 1, 2]
DEFAULT_BEAR_POSITION = [20]
BOARD_SIZE = 21

class Board:
    """
    Board abstraction
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
        self._cells = [default_char] * BOARD_SIZE
        for hunter in DEFAULT_HUNTER_POSITION:
            self._cells[hunter] = str(HUNTER)

        for bear in DEFAULT_BEAR_POSITION:
            self._cells[bear] = str(BEAR)

        self._last_action = []

    def __str__(self):
        return ''.join(self._cells)

    def __getitem__(self, index):
        return self._cells[index]

    def __setitem__(self, index, value):
        self._cells[index] = value

    def get_hash(self) -> str:
        """ 
        get hash of the board, this is not a proper hash, as
        it's easy to convert it back to the board, just an encoding, but
        i want to keep this name.
        """

        def get_value(char: str):
            if char == '_':
                return 0
            elif char == '0':
                return 1
            elif char == '1':
                return 2
            else:
                raise ValueError("Invalid character")

        val = 0
        for i, ch in enumerate(str(self)):
            val += get_value(ch) * 3 ** i

        return val

    def str_from_hash(hash: int) -> str:
        """ get string from hash """
        def get_char(val: int):
            if val == 0:
                return '_'
            elif val == 1:
                return '0'
            elif val == 2:
                return '1'
            else:
                raise ValueError("Invalid character")

        str = ""
        for i in range(21):
            str += get_char(hash % 3)
            hash = hash // 3

        return str

    def reachable_states(self, actions: list[tuple[int, int]]) -> list[int]:
        """ get reachable states from a state """
        states = []
        for action in actions:
            self.apply_action(action)
            states.append(self.get_hash())
            self.undo_action()

        return states


    def get_cells(self) -> list[str]:
        """ get cells """
        return self._cells

    def set_cells(self, cells: list[str]) -> None:
        """ set cells """
        self._cells = cells

    def get_size(self) -> int:
        """ get size of the board """
        return len(self._cells)

    def apply_action(self, action: tuple[int, int]):
        """ apply action to the board 
            Represents a move from action[0] to action[1]
            from a player.
        """

        self._cells[action[1]] = self._cells[action[0]]
        self._cells[action[0]] = self._default_char
        self._last_action += [action]
    
    def undo_action(self):
        """ undo last action """
        action = self._last_action[-1]
        self._cells[action[0]] = self._cells[action[1]]
        self._cells[action[1]] = self._default_char
        self._last_action = self._last_action[:-1]

    def get_actions(self, player_val: int) -> list[tuple[int, int]]:
        """ 
        Returns list of available actions (starting_position, target_position) 
        We are sure that the end location is empty
        """
        actions = []
        player_symbol = str(player_val)
        for i, symbol in enumerate(self._cells):
            if symbol == player_symbol:
                for target in self.adjacent[i]:
                    if self._cells[target] == self._default_char:
                        actions.append((i, target))

        return actions

    def get_default_char(self) -> str:
        """ get default character """
        return self._default_char

    def display(self):
        print("            "+self._cells[0]+"            ","             "+"0"+"            ")
        print("        "+self._cells[1]+"       "+self._cells[2]+"        ","         "+"1"+"       "+"2"+"        ")
        print("            "+self._cells[3]+"            ","             "+"3"+"            ")
        print("  "+self._cells[4]+"         "+self._cells[5]+"         "+self._cells[6]+"  ","   "+"4"+"         "+"5"+"         "+"6"+"  ")
        print(""+self._cells[7]+"   "+self._cells[8]+"   "+self._cells[9]+"   "+self._cells[10]+"   "+self._cells[11]+"   "+self._cells[12]+"   "+self._cells[13]+"",
              " "+"7"+"   "+"8"+"   "+"9"+"  "+"10"+"  "+"11"+"  "+"12"+"  "+"13"+"")
        print("  "+self._cells[14]+"         "+self._cells[15]+"         "+self._cells[16]+"  ","  "+"14"+"        "+"15"+"        "+"16"+"")
        print("            "+self._cells[17]+"            ","            "+"17"+"            ")
        print("        "+self._cells[18]+"       "+self._cells[19]+"        ","        "+"18"+"      "+"19"+"        ")
        print("            "+self._cells[20]+"            ","            "+"20"+"            ")


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
        self._default_cells = board._cells.copy()
        self._board = board
        self._hunter_player: AbstractPlayer = player0
        self._bear_player: AbstractPlayer = player1
        self._display_board: bool = display_board
        self._turn: int = 0
        self._max_turns: int = max_turns
        self._winner: 0 | 1 | 2 = None
        self.visited_states = dict()


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

    def compute_reward(self, player_num: int) -> int:
        """
        Compute the reward for the given player

        Important observations:
        if the game has not ended we need to put the hunters in pain,
        so that they are more motivated to end the game, as quickly as possible

        For the bear, we want him to take as much time as possible to win, so we only
        penalize the defeat.

        hunter is Max-player, bear is Min-player
        """
        if player_num == HUNTER:
            if self._winner == HUNTER:
                return 0
            return -1
        elif player_num == BEAR:
            if self._winner == HUNTER:
                return 1
            return 0

        raise ValueError("Invalid player symbol")

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
                self._board.reachable_states(actions),
                actions
            )
            action = actions[action_idx]
            
            self._board.apply_action(action)
            if self.has_ended():
                if self._turn >= self._max_turns:
                    self._winner = BEAR
                else:
                    self._winner = HUNTER

            if False and isinstance(curr_player, AIPlayer):
                curr_player.feed_reward(
                    state=board_state,
                    next_state=self._board.get_hash(),
                    action_taken=action,
                    actions=self._board.get_actions(1 - player_num),
                    reward=self.compute_reward(player_num)
                )

            if self._winner is not None:
                break
            
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

    def calculate_mini_max(self) -> None:
        """
        In questo algoritmo consideriamo una minimax senza alpha-beta pruning
        dato che il numero di stati è molto piccolo. Consideriamo configurazioni
        di vittoria per l'hunter quelli codificati in end_states, mentre per il bear
        configurazioni che sono state già visitate (se l'orso è in grado di creare
        dei cicli, può continuare indefinitamente a giocare, quindi la sua vittoria
        è assicurata)
        """
        self.reset()

        # TODO vedere chi sia il player migliore a seconda di chi giocava prima
        self.hunter_play()

        print("Saving the states values")
        data = dict()
        data['states_value'] = self.visited_states.copy()
        with open(f'states_value.pickle', 'wb') as handle:
            pickle.dump(data, handle)
        print("Done, states saved")



    def hunter_play(self) -> int:
        """ I cacciatori """
        current_hash = self._board.get_hash()
        if current_hash in self.visited_states:
            if self.visited_states[current_hash] == self.VISITED:
                return self.BEAR_WIN
            return self.visited_states[current_hash]

        self.visited_states[current_hash] = self.VISITED
        hunter_win = False
        for action in self._board.get_actions(HUNTER):
            self._board.apply_action(action)
            state = self._board.get_hash()
            
            # nel caso in cui esista una azione che porta alla vittoria dell'hunter
            # la seguo subito e saprò che vincerò.
            if state in self.visited_states and self.visited_states[state] == self.HUNTER_WIN:
                self._board.undo_action()
                self.visited_states[current_hash] = self.HUNTER_WIN
                hunter_win = True # così esploro tutti gli stati
                continue

            res = self.bear_play()
            
            if res == self.HUNTER_WIN:
                self.visited_states[current_hash] = self.HUNTER_WIN
                self._board.undo_action()
                hunter_win = True
                continue

            self._board.undo_action()
        
        if hunter_win:
            return self.HUNTER_WIN

        self.visited_states[current_hash] = self.BEAR_WIN
        return self.BEAR_WIN

    def bear_play(self) -> int:
        """ Il orso """
        current_hash = self._board.get_hash()
        if current_hash in self.visited_states:
            if self.visited_states[current_hash] == self.VISITED:
                return self.BEAR_WIN
            return self.visited_states[current_hash]

        self.visited_states[current_hash] = self.VISITED
        bear_win = False
        for action in self._board.get_actions(BEAR):
            self._board.apply_action(action)
            state = self._board.get_hash()
            
            if state in self.visited_states and self.visited_states[state] == self.BEAR_WIN:
                self._board.undo_action()
                self.visited_states[current_hash] = self.BEAR_WIN
                bear_win = True
                continue
            
            res = self.hunter_play()
            
            if res == self.BEAR_WIN:
                self.visited_states[current_hash] = self.BEAR_WIN
                self._board.undo_action()
                bear_win = True
                continue

            self._board.undo_action()
        
        if bear_win:
            return self.BEAR_WIN
        self.visited_states[current_hash] = self.HUNTER_WIN
        return self.HUNTER_WIN

    def reset(self) -> None:
        """
        Reset the game variables to their default values
        """
        self._turn = 0
        self._board.set_cells(self._default_cells.copy())
        self._winner = None
        visited_states = dict()
        for end_state in self.end_states:
            self.visited_states[end_state] = self.HUNTER_WIN