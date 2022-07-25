import pickle 
import numpy as np 

BEAR_WINS = 1
HUNTER_WINS = 2

HUNTER_CHAR = '1'
BEAR_CHAR = '2'
class Board():
    #Adjacent locations
    adjacent = [[1,2,3], #0
            [0,3,4],
            [0,3,6], #2
            [0,1,2,5],
            [1,7,8], #4
            [3,9,10,11],
            [2,12,13], #6
            [4,8,14],
            [7,4,14,9], #8
            [8, 10,5,15],
            [5,9,11,15],#10
            [5,10,15,12],
            [11,6,16,13],#12
            [6,12,16],
            [7,8,18],#14
            [9,10,11,17],
            [12,13,19], #16
            [15,18,19,20],
            [14,17,20], #18
            [16, 17, 20],
            [18, 17, 19]]

    #init
    def __init__(self):
        self.set_default()

        # Combinations for bear to loose, one for each edge position
        # index ease                '0,','1', '2', '3', '4', '5', '6', '7', '8', '9', '10, '11, '12, '13  '14, '15, '16, '17, '18, '19, '20
        self._bear_ko_positions = [['2', '1', '1', '1', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'], # Bear in 0
                                    ['1', '_', '2', '1', '_', '_', '1', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'], # Bear in 2
                                    ['_', '_', '1', '_', '_', '_', '2', '_', '_', '_', '_', '_', '1', '1', '_', '_', '_', '_', '_', '_', '_'], # Bear in 6
                                    ['_', '_', '_', '_', '_', '_', '1', '_', '_', '_', '_', '_', '1', '2', '_', '_', '1', '_', '_', '_', '_'], # Bear in 13
                                    ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '1', '1', '_', '_', '2', '_', '_', '1', '_'], # Bear in 16
                                    ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '1', '1', '_', '2', '1'], # Bear in 19
                                    ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '1', '1', '1', '2'], # Bear in 20
                                    ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '1', '_', '_', '1', '2', '_', '1'], # Bear in 18
                                    ['_', '_', '_', '_', '_', '_', '_', '1', '1', '_', '_', '_', '_', '_', '2', '_', '_', '_', '1', '_', '_'], # Bear in 14
                                    ['_', '_', '_', '_', '1', '_', '_', '2', '1', '_', '_', '_', '_', '_', '1', '_', '_', '_', '_', '_', '_'], # Bear in 7
                                    ['_', '1', '_', '_', '2', '_', '_', '1', '1', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'], # Bear in 4
                                    ['1', '2', '_', '1', '1', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_']] # Bear in 1
        
        self._bear_player = Player("bear")
        self._hunter_player = Player("hunter")

    def set_default(self):
        self._cells = ['_'] * 21
        self._cells[0] = self._cells[1] = self._cells[2] = HUNTER_CHAR
        # init bear position
        self._bear_position = 20
        self._max_bear_moves = 30
        self._cells[self._bear_position] = BEAR_CHAR
        # Hunter starts
        self._is_hunter_turn = True
        # Bear moves counter
        self._bear_moves = 0

        self._winner = None 
        self._last_move = None

    def reset(self):
        self.set_default()
        self._bear_player.reset()
        self._hunter_player.reset()

    def get_bear_actions(self) -> list[(int, int)]:
        actions = [] 
        for adj in Board.adjacent[self._bear_position]:
            if self._cells[adj] == '_':
                actions.append((self._bear_position, adj))
        return actions

    def get_hunter_positions(self) -> list:
        return [i for i, x in enumerate(self._board) if x == HUNTER_CHAR]

    def get_hunter_actions(self) -> list[(int, int)]:
        actions = [] 
        for pos in self.get_hunter_positions():
            for adj in Board.adjacent[pos]:
                if self._cells[adj] == '_':
                    actions.append((pos, adj))
        return actions

    #displays board in a presentable order
    def display(self):
        # print board
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

    #updates board
    def move_player(self, starting_position, target_position):
        self._cells[starting_position] = '_'
        if self._is_hunter_turn:
            self._cells[target_position] = '1'
        else:
            self._bear_moves += 1
            self._bear_position = target_position
            self._cells[target_position] = '2'
        self._last_move = (starting_position, target_position)
        self.toggle_is_hunter_turn()
    
    def undo_move(self):
        self.toggle_is_hunter_turn()
        target_position, starting_position = self._last_move # contrario!
        self._cells[starting_position] = '_'
        if self._is_hunter_turn:
            self._cells[target_position] = '1'
        else:
            self._bear_moves -= 1
            self._bear_position = target_position
            self._cells[target_position] = '2'
        self._last_move = None 

    # used to reset the bear moves
    def sub_bear_moves(self, value):
        self._bear_moves -= value

    #checks all conditions for winner
    def has_ended(self):
        if (self._cells in self._bear_ko_positions):
            self._winner = HUNTER_WINS
            return True
        elif (self._bear_moves > self._max_bear_moves):
            self._winner = BEAR_WINS
            return True
        else:
            return False

    #returns winner
    def get_winner(self):
        return self._winner

    def set_winner(self, winner):
        self._winner = winner

    def print_winner(self):
        if self._winner == HUNTER_WINS:
            print("Hunter WINS; Bear's moves ",self._bear_moves)
        elif self._winner == BEAR_WINS:
            print("Bear WINS")            
        else:
            print("Tie") # non succede mai, ma ce lo voglio mettere :)

    def is_hunter_turn(self):
        return self._is_hunter_turn
    
    def toggle_is_hunter_turn(self):
        self._is_hunter_turn = not self._is_hunter_turn

    def set_is_hunter_turn(self, is_hunter_turn):
        self._is_hunter_turn = is_hunter_turn

    def get_bear_moves(self):
        return self._bear_moves

    def get_hunter_positions(self) -> list[int]: 
        positions = [] 
        for i in range(len(self._cells)):
            if self._cells[i] == '1':
                positions.append(i)
        return positions

    def get_bear_position(self):
        return self._bear_position
        
    def get_position(self, position):
        return self._cells[position]

    def possible_moves(self, position):
        moves = []
        #Check free positions
        for x in Board.adjacent[position]:
            if self._cells[x] == '_':
                moves.append(x)
        return moves

    def get_position(self, pos: int):
        return self._cells[pos]

    def get_hash(self):
        return hash(''.join(self._cells))

    def apply_reward(self):
        if self._winner == HUNTER_WINS:
            self._hunter_player.feed_reward(1)
            self._bear_player.feed_reward(0)
        elif self._winner == BEAR_WINS:
            self._hunter_player.feed_reward(0)
            self._bear_player.feed_reward(1)

    @staticmethod
    def get_adiacent(position):
        return Board.adjacent[position]

    def play_game(self):
        while not self.has_ended():
            if self.is_hunter_turn():
                action = self._hunter_player.get_action(self.get_hunter_actions(), self)
            else:
                action = self._bear_player.get_action(self.get_bear_actions(), self)
            self.move_player(action[0], action[1])

    def train(self, n_times = 100):
        for i in range(n_times):
            try:
                self.play_game()
                self.apply_reward()
                self.reset()
            except KeyboardInterrupt:
                import traceback 
                print(traceback.format_exc())
                print("got KeyboardInterrupt, this could potentially do some harm to the\
                    training process, if you interrupted the feed_reward process.")
                inp = str(input(f"Currently on iteration {i}: \
                    exit and save? ('y' for yes, everything else is no)"))
                if inp == 'y':
                    break 
                else:
                    self.reset()
                    continue


        self._bear_player.save_policy() 
        self._hunter_player.save_policy()

    def human_get_action(self, actions: list[(int, int)]) -> list[(int, int)]:
        while True:
            start_position = int(input("Start position: "))
            end_position = int(input("End position: "))

            if (start_position, end_position) not in actions:
                print("Invalid move")
                continue
            else:
                break
        return (start_position, end_position)

    def play_as_hunter(self, file: str) -> None:
        self._bear_player.load_policy(file)

        while not self.has_ended():
            self.display()
            if self.is_hunter_turn():
                action = self.human_get_action(self.get_hunter_actions())
            else:
                action = self._bear_player.get_action(self.get_bear_actions(), self)
            self.move_player(action[0], action[1])


    def play_as_bear(self, file: str) -> None:
        self.hunter_player.load_policy(file)

        while not self.has_ended():
            if self.is_hunter_turn():
                action = self._hunter_player.get_action(self.get_hunter_actions(), self)
            else:
                action = self.human_get_action(self.get_hunter_actions())
            self.move_player(action[0], action[1])

##########################################################################################################
# The AI 2
##########################################################################################################
INFINITY = 1000000

class Player:
    def __init__(self, name, exp_rate=0.3, alpha=0.2, gamma=0.9):
        self.name = name
        self.states = []  # record all positions taken
        self.alpha = alpha
        self.exp_rate = exp_rate
        self.decay_gamma = gamma
        self.states_value = {}  # state -> value

    def get_action(self, actions, current_board: Board):
        if np.random.uniform(0, 1) <= self.exp_rate:
            idx = np.random.choice(len(actions))
            action = actions[idx]
        else:
            value_max = -INFINITY
            for act in actions:
                current_board.move_player(act[0], act[1])
                state_value = self.states_value.get(current_board.get_hash())
                if (state_value is None):
                    value = 0
                else:
                    value = state_value

                if value >= value_max:
                    value_max = value
                    action = act

                current_board.undo_move()
        return action

    # append a hash state
    def add_state(self, state):
        self.states.append(state)

    # at the end of game, backpropagate and update states value
    def feed_reward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.alpha * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]

    def reset(self):
        self.states = []

    def save_policy(self):
        from time import time 
        curr_time = int(time()) 
        fw = open(f'{str(self.name)}_{curr_time}.policy', 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def load_policy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()


##########################################################################################################
# The game
##########################################################################################################
#MODEL
# init board

if __name__ == "__main__":
    game = Board()
    game.play_as_hunter("bear_1658733854.policy")
    game.print_winner()


"""
is_bear_ai = int(input("Do you want to play against the bear AI? (1/0)"))
# Game cycle
while not game.has_ended():

    game.display()
    # Starting position
    if game.is_hunter_turn():
        print("Hunter is playing")
        try:
            # Must be integer
            starting_pos = int(input(" Enter position you want to pick from (0-20): \n").strip())

            # Between 0 and 20
            if starting_pos < 0 or starting_pos > 20:
                print("Number out of range")
                raise ValueError
            # Belonging to hunter
            if (game.get_position(starting_pos) != '1'):
                print("Not your pawn")
                raise ValueError 
        except ValueError:
            print("Please enter only valid fields from board (0-20)")
            continue
        
    else:
        print("Bear is playing move n. ",game.get_bear_moves())
        starting_pos = game.get_bear_position()

    # Target position
    try:
        target_pos = int(input(" Enter target position you want to go to: \n").strip())

        if target_pos not in game.possible_moves(starting_pos):
            raise ValueError
    except ValueError:
        print("Please enter only valid fields from board (0-20)")
        continue
    # Make the move
    game.move_player(starting_pos, target_pos)

    if not game.is_hunter_turn() and is_bear_ai == 1:
        import time # too check how much time is used
        curr_time = time.time()
        # AI move, driver code
        alpha = -INFINITY
        beta = INFINITY

        best_move = None 
        best_value = -INFINITY
        bear_position = game.get_bear_position()
        moves = game.possible_moves(bear_position)
        moves = sort_with_heuristic(moves)
        print(f"the moves are : {moves}")
        for move, _ in moves:
            game.set_is_hunter_turn(False)
            game.move_player(bear_position, move)
            value = max_player(alpha, beta)
            game.set_is_hunter_turn(False)
            game.move_player(game.get_bear_position(), bear_position) 
            game.sub_bear_moves(2) 

            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
            if (alpha >= beta):
                break

        game.set_is_hunter_turn(False)
        if best_move != None:
            game.move_player(bear_position, best_move)
        print("moving the real player")
        print("time taken to take the move: ", time.time() - curr_time)
        game.display()
        
        # print euristics value 
        print(f"heuristics value is {get_heuristic_value(game.get_bear_position(), game.get_hunter_positions())}")

game.print_winner()
"""
