"""
This module handles all the logic to start the game
"""
import argparse
import sys
from board import Board
from game import Game
from player import AIPlayer, HumanPlayer, AbstractPlayer

sys.setrecursionlimit(30000)
DEFAULT_NO_PLAYER = 'random'

def _parse_arguments():
    parser = argparse.ArgumentParser(description="\
        This program is a interface used to train the players for the\
        bear game, it offers features as loading of previous trained policies\
        human play (in terminal visuals), number of training games (games to play)\
    ")
    parser.add_argument('--hunter-ai-file',
        type=str, 
        help='Path to the hunter AI policy file',
        default=DEFAULT_NO_PLAYER)

    parser.add_argument('--bear-ai-file',
        type=str, 
        help='Path to the bear AI policy file',
        default=DEFAULT_NO_PLAYER)

    parser.add_argument('--bear-human',
        action='store_true',
        help='Set this flag if you want bear to be human player',
        default=False)

    parser.add_argument('--hunter-human',
        action='store_true',
        help='Set this flag if you want hunter to be human player',
        default=False)

    parser.add_argument('--train',
        help='calculate the state value using deterministic algorithm, for further \
            information read the comments on the main function for this argument \
            the first function called, if this flag is set',
        action='store_true',
        default=False)

    return parser.parse_args()

def initialize_players() -> tuple[AbstractPlayer, AbstractPlayer]:
    """
    Initialize the players
    """
    if args.hunter_human:
        hunter_ai = HumanPlayer(name='hunter')
    else:
        hunter_ai = AIPlayer(name='hunter',
            maximize=False
        )
        if args.hunter_ai_file != DEFAULT_NO_PLAYER:
            hunter_ai.load_policy(args.hunter_ai_file)

    if args.bear_human:
        bear_ai = HumanPlayer(name='bear')
    else:
        bear_ai = AIPlayer(name='bear', 
            maximize=True
        )
        if (args.bear_ai_file != DEFAULT_NO_PLAYER):
            bear_ai.load_policy(args.bear_ai_file)

    return hunter_ai, bear_ai

if __name__ == '__main__':
    args = _parse_arguments()

    hunter_player, bear_player = initialize_players()
    board = Board()

    if args.train:
        game = Game(board, hunter_player, bear_player, display_board=False)
        game.calculate_deterministic_state_value()
    else:
        game = Game(board, hunter_player, bear_player, display_board=True)
        game.play()
        game.print_winner()
