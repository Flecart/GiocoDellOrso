"""
This module handles all the logic to start the game
"""
import argparse
import random
from board import Board, Game
from player import AIPlayer, HumanPlayer, AbstractPlayer

DEFAULT_NO_PLAYER = 'random'

def _parse_arguments():
    parser = argparse.ArgumentParser(description="\
        This program is a interface used to train the players for the\
        bear game, it offers features as loading of previous trained policies\
        human play (in terminal visuals), number of training games (games to play)\
    ")
    parser.add_argument('--hunter_ai_file',
        type=str, 
        help='Path to the hunter AI policy file',
        default=DEFAULT_NO_PLAYER)

    parser.add_argument('--bear_ai_file',
        type=str, 
        help='Path to the bear AI policy file',
        default=DEFAULT_NO_PLAYER)

    parser.add_argument('--bear_human',
        action='store_true',
        help='Set this flag if you want bear to be human player',
        default=False)

    parser.add_argument('--hunter_human',
        action='store_true',
        help='Set this flag if you want hunter to be human player',
        default=False)

    parser.add_argument('--display_board',
        action='store_true',
        help='Set this flag if you want to display the board',
        default=False)

    parser.add_argument('--n_games',
        type=int, 
        help='Number of games to play (useful for training phase)',
        default=1)

    parser.add_argument('--disable_training',
        action='store_true',
        help='Set this flag if you don´t  want the bot to make exploratory moves, won´t save the policy',
        default=False)

    parser.add_argument('--seed',
        type=int,
        help='Seed for the random generator (None for random seed)',
        default=None)
    return parser.parse_args()

def initialize_players() -> tuple[AbstractPlayer, AbstractPlayer]:
    """
    Initialize the players
    """
    if args.hunter_human:
        hunter_ai = HumanPlayer(name='hunter')
    else:
        hunter_ai = AIPlayer(name='hunter',training=not args.disable_training)
        if args.hunter_ai_file != DEFAULT_NO_PLAYER:
            hunter_ai.load_policy(args.hunter_ai_file)

    if args.bear_human:
        bear_ai = HumanPlayer(name='bear')
    else:
        bear_ai = AIPlayer(name='bear', training=not args.disable_training)
        if (args.bear_ai_file != DEFAULT_NO_PLAYER):
            bear_ai.load_policy(args.bear_ai_file)

    return hunter_ai, bear_ai

if __name__ == '__main__':
    args = _parse_arguments()

    if args.seed is not None:
        random.seed(args.seed)

    hunter_player, bear_player = initialize_players()

    board = Board()
    game = Game(board, hunter_player, bear_player, args.display_board)

    if not args.disable_training:
        game.train(args.n_games)
    else:
        for _ in range(args.n_games):
            game.play()
            game.print_winner()
            game.reset()
