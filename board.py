"""
This module is used as board abstraction for the game.
"""
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

    def get_encoding(self) -> str:
        val = 0
        for i in self._hunters:
            val += (HUNTER + 1) * 3 ** i
        for i in self._bear:
            val += (BEAR + 1) * 3 ** i

        return val

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
                            states.add(self.get_encoding())
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