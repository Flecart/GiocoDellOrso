BEAR_WINS = 1
HUNTER_WINS = 2

class Board():
    
    # distances generated and pasted here
    distances = [[0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6], [1, 0, 2, 1, 1, 2, 3, 2, 2, 3, 3, 3, 4, 4, 3, 4, 5, 5, 4, 6, 5], [1, 2, 0, 1, 3, 2, 1, 4, 4, 3, 3, 3, 2, 2, 5, 4, 3, 5, 6, 4, 5], [1, 1, 1, 0, 2, 1, 2, 3, 3, 2, 2, 2, 3, 3, 4, 3, 4, 4, 5, 5, 5], [2, 1, 3, 2, 0, 3, 4, 1, 1, 2, 3, 4, 5, 5, 2, 3, 6, 4, 3, 5, 4], [2, 2, 2, 1, 3, 0, 3, 3, 2, 1, 1, 1, 2, 3, 3, 2, 3, 3, 4, 4, 4], [2, 3, 1, 2, 
4, 3, 0, 5, 5, 4, 3, 2, 1, 1, 6, 3, 2, 4, 5, 3, 4], [3, 2, 4, 3, 1, 3, 5, 0, 1, 2, 3, 4, 5, 6, 1, 3, 5, 3, 2, 4, 3], [3, 2, 4, 3, 1, 2, 5, 1, 0, 1, 2, 3, 4, 5, 1, 2, 5, 3, 2, 4, 3], [3, 3, 3, 2, 2, 1, 4, 2, 1, 0, 1, 2, 3, 4, 2, 1, 4, 2, 3, 3, 3], [3, 3, 3, 2, 3, 1, 3, 3, 2, 1, 0, 1, 2, 3, 3, 1, 3, 2, 3, 3, 3], [3, 3, 3, 2, 4, 1, 2, 4, 3, 2, 1, 0, 1, 2, 4, 1, 2, 2, 3, 3, 3], [3, 4, 2, 3, 5, 2, 1, 5, 4, 3, 2, 1, 0, 1, 5, 2, 1, 3, 4, 2, 3], [3, 4, 2, 3, 5, 3, 1, 6, 5, 4, 3, 2, 1, 0, 5, 3, 1, 3, 4, 2, 3], [4, 3, 5, 4, 2, 3, 6, 1, 1, 2, 3, 4, 5, 5, 0, 3, 4, 2, 1, 3, 2], [4, 4, 4, 3, 3, 2, 3, 3, 2, 1, 1, 
1, 2, 3, 3, 0, 3, 1, 2, 2, 2], [4, 5, 3, 4, 6, 3, 2, 5, 5, 4, 3, 2, 1, 1, 4, 3, 0, 2, 3, 1, 2], [5, 5, 5, 4, 4, 3, 4, 3, 3, 2, 2, 2, 3, 3, 2, 1, 2, 0, 1, 1, 1], [5, 4, 6, 5, 3, 4, 5, 2, 2, 3, 3, 3, 4, 4, 1, 2, 3, 1, 0, 2, 1], [5, 6, 4, 5, 5, 4, 3, 4, 4, 3, 3, 3, 2, 2, 3, 2, 1, 1, 2, 0, 1], [6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0]]

    
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
        self.__cells = ['_'] * 21
        self.__cells[0] = self.__cells[1] = self.__cells[2] = '1'
        # init bear position
        self.__bear_position = 20
        self.__max_bear_moves = 40
        self.__cells[self.__bear_position] = '2'
        # Hunter starts
        self.__is_hunter_turn = True
        # Bear moves counter
        self.__bear_moves = 1
        # Combinations for bear to loose, one for each edge position
        # index ease                '0,','1', '2', '3', '4', '5', '6', '7', '8', '9', '10, '11, '12, '13  '14, '15, '16, '17, '18, '19, '20
        self.__bear_ko_positions = [['2', '1', '1', '1', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'], # Bear in 0
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
        
        self.__winner = None 

    #displays board in a presentable order
    def display(self):
        # print board
        print("            "+self.__cells[0]+"            ","             "+"0"+"            ")
        print("        "+self.__cells[1]+"       "+self.__cells[2]+"        ","         "+"1"+"       "+"2"+"        ")
        print("            "+self.__cells[3]+"            ","             "+"3"+"            ")
        print("  "+self.__cells[4]+"         "+self.__cells[5]+"         "+self.__cells[6]+"  ","   "+"4"+"         "+"5"+"         "+"6"+"  ")
        print(""+self.__cells[7]+"   "+self.__cells[8]+"   "+self.__cells[9]+"   "+self.__cells[10]+"   "+self.__cells[11]+"   "+self.__cells[12]+"   "+self.__cells[13]+"",
              " "+"7"+"   "+"8"+"   "+"9"+"  "+"10"+"  "+"11"+"  "+"12"+"  "+"13"+"")
        print("  "+self.__cells[14]+"         "+self.__cells[15]+"         "+self.__cells[16]+"  ","  "+"14"+"        "+"15"+"        "+"16"+"")
        print("            "+self.__cells[17]+"            ","            "+"17"+"            ")
        print("        "+self.__cells[18]+"       "+self.__cells[19]+"        ","        "+"18"+"      "+"19"+"        ")
        print("            "+self.__cells[20]+"            ","            "+"20"+"            ")

    #updates board
    def move_player(self, starting_position, target_position):
        self.__cells[starting_position] = '_'
        if self.__is_hunter_turn:
            self.__cells[target_position] = '1'
        else:
            self.__bear_moves += 1
            self.__bear_position = target_position
            self.__cells[target_position] = '2'
        # Change turn
        self.toggle_is_hunter_turn()
    
    # used to reset the bear moves
    def sub_bear_moves(self, value):
        self.__bear_moves -= value

    #checks all conditions for winner
    def has_ended(self):
        if (self.__cells in self.__bear_ko_positions):
            self.__winner = HUNTER_WINS
            return True
        elif (self.__bear_moves > self.__max_bear_moves):
            self.__winner = BEAR_WINS
            return True
        else:
            return False

    @staticmethod
    def get_distance(position1, position2):
        return Board.distances[position1][position2]

    #returns winner
    def get_winner(self):
        return self.__winner

    def set_winner(self, winner):
        self.__winner = winner

    def print_winner(self):
        if self.__winner == HUNTER_WINS:
            print("Hunter WINS; Bear's moves ",self.__bear_moves)
        elif self.__winner == BEAR_WINS:
            print("Bear WINS")            
        else:
            print("Tie") # non succede mai, ma ce lo voglio mettere :)

    def is_hunter_turn(self):
        return self.__is_hunter_turn
    
    def toggle_is_hunter_turn(self):
        self.__is_hunter_turn = not self.__is_hunter_turn

    def set_is_hunter_turn(self, is_hunter_turn):
        self.__is_hunter_turn = is_hunter_turn

    def get_bear_moves(self):
        return self.__bear_moves

    def get_hunter_positions(self) -> list[int]: 
        positions = [] 
        for i in range(len(self.__cells)):
            if self.__cells[i] == '1':
                positions.append(i)
        return positions

    def get_bear_position(self):
        return self.__bear_position
        
    def get_position(self, position):
        return self.__cells[position]

    def possible_moves(self, position):
        moves = []
        #Check free positions
        for x in Board.adjacent[position]:
            if self.__cells[x] == '_':
                moves.append(x)
        return moves

    @staticmethod
    def get_adiacent(position):
        return Board.adjacent[position]

##########################################################################################################
# The AI
##########################################################################################################
PLY_DEPTH_LIMIT = 8
INFINITY = 1000000
DEFAULT_DIST = [INFINITY] * 21
DEFAULT_VISITED = [False] * 21
from queue import Queue 

def evaluate_ending(game: Board):
    state_value = 0
    if game.get_winner() == HUNTER_WINS:
        state_value = INFINITY
    elif game.get_winner() == BEAR_WINS:
        state_value = -INFINITY

    game.set_winner(None)
    return state_value

def get_heuristic_value(bear_position: int, hunter_positions: list[int], n: int = 3):
    """ Numero di nodi raggiungibili in n mosse"""
    heuristic = 0

    visited = DEFAULT_VISITED.copy() # 21 è il numero di posizioni
    dist = DEFAULT_DIST.copy()
    # bfs to get reachable nodes 
    queue = Queue()
    queue.put(bear_position)
    visited[bear_position] = True
    dist[bear_position] = 0
    while not queue.empty():
        current = queue.get()
        heuristic += 1
        if dist[current] == 2:
            continue 

        for x in Board.get_adiacent(current):
            if not visited[x]:
                queue.put(x)
                dist[x] = dist[current] + 1
                visited[x] = True


    return heuristic

def sort_with_heuristic(moves: list[int]):
    moves_with_heuristic = []
    hunter_positions = game.get_hunter_positions()
    for move in moves:
        moves_with_heuristic.append((move, get_heuristic_value(move, hunter_positions)))
    moves_with_heuristic.sort(key=lambda x: x[1], reverse=True)
    return moves_with_heuristic

# bear player
def min_player(alpha: int, beta: int, depth: int = 0):
    global game 
    if game.has_ended(): 
        return evaluate_ending(game)
    if depth >= PLY_DEPTH_LIMIT:
        return -get_heuristic_value(game.get_bear_position(), game.get_hunter_positions()) # vuol dire che l'orso sta ancora vincendo!
    
    moves = game.possible_moves(game.get_bear_position())
    best_value = INFINITY
    last_bear_pos = game.get_bear_position()
    for move in moves:
        game.set_is_hunter_turn(False)
        game.move_player(last_bear_pos, move)
        value = max_player(alpha, beta, depth + 1)
        game.set_is_hunter_turn(False)
        game.move_player(game.get_bear_position(), last_bear_pos) 
        game.sub_bear_moves(2) 

        if value < best_value:
            best_value = value

        beta = min(beta, best_value)
        if alpha >= beta:
            return best_value

    return best_value

# hunter player
def max_player(alpha: int, beta: int, depth: int = 0):
    global game 
    if game.has_ended():
        return evaluate_ending(game)
    if depth >= PLY_DEPTH_LIMIT:
        return -get_heuristic_value(game.get_bear_position(), game.get_hunter_positions())
    
    hunter_positions = game.get_hunter_positions()
    best_value = -INFINITY
    for hunter_pos in hunter_positions:
        moves = game.possible_moves(hunter_pos)
        for move in moves:
            game.set_is_hunter_turn(True)
            game.move_player(hunter_pos, move)
            value = min_player(alpha, beta, depth + 1)
            game.set_is_hunter_turn(True)
            game.move_player(move, hunter_pos)

            if value > best_value:
                best_value = value

            alpha = max(alpha, best_value)
            if alpha >= beta:
                return best_value
    return best_value

##########################################################################################################
# The game
##########################################################################################################
#MODEL
# init board
game = Board()

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