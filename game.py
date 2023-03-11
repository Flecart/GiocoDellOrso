import pickle
from player import AbstractPlayer
from board import Board, HUNTER, BEAR

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
        with open('bear_policy.pickle', 'wb') as handle:
            pickle.dump(data_bear, handle)

        with open('hunter_policy.pickle', 'wb') as handle:
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