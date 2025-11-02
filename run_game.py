import argparse
import json
import os
from config import DEFAULT_NUM_TURNS
from questions_manager import QuestionsManager


def get_questions(questions_file=None):
    """
    Read questions from a JSON file.
    
    Args:
        questions_file: Path to the questions file. If None, defaults to 'questions.json'
    
    Returns:
        QuestionsManager: An instance of QuestionsManager with loaded questions
    
    Raises:
        FileNotFoundError: If the questions file is not found
        json.JSONDecodeError: If the file contains invalid JSON
    """
    if questions_file is None:
        questions_file = 'questions.json'
    
    if not os.path.exists(questions_file):
        raise FileNotFoundError(f"Questions file not found: {questions_file}")
    
    with open(questions_file, 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    
    return QuestionsManager(questions_data)


def parse_arguments():
    """
    Parse command line arguments for the trivia game.

    Required arguments:
    - player1: Name of player 1
    - player2: Name of player 2

    Optional arguments:
    - num_questions: Number of questions (default: 10)
    - questions_file: Path to questions file (default: None)
    """
    parser = argparse.ArgumentParser(
        description='Trivia Game - Command Line Arguments Parser'
    )

    # Make arguments optional so we can handle them interactively
    parser.add_argument(
        'player1',
        type=str,
        nargs='?',
        default=None,
        help='Name of player 1'
    )

    parser.add_argument(
        'player2',
        type=str,
        nargs='?',
        default=None,
        help='Name of player 2'
    )

    # Optional arguments
    parser.add_argument(
        '-n', '--num_questions',
        type=int,
        default=DEFAULT_NUM_TURNS,
        help=f'Number of questions (default: {DEFAULT_NUM_TURNS})'
    )

    parser.add_argument(
        '-f', '--questions_file',
        type=str,
        default=None,
        help='Path to questions file (default: None)'
    )

    args = parser.parse_args()

    # Interactively ask for mandatory parameters if not provided
    if args.player1 is None:
        args.player1 = input("Enter name of player 1: ").strip()
        while not args.player1:
            print("Player 1 name cannot be empty!")
            args.player1 = input("Enter name of player 1: ").strip()

    if args.player2 is None:
        args.player2 = input("Enter name of player 2: ").strip()
        while not args.player2:
            print("Player 2 name cannot be empty!")
            args.player2 = input("Enter name of player 2: ").strip()

    # Print parsed parameters
    print("=" * 50)
    print("Parsed Command Line Arguments:")
    print("=" * 50)
    print(f"Player 1: {args.player1}")
    print(f"Player 2: {args.player2}")
    print(f"Number of Questions: {args.num_questions}")
    print(f"Questions File: {args.questions_file}")
    print("=" * 50)

    return args


if __name__ == "__main__":
    #args = parse_arguments()
    questions = get_questions()
    print(questions.get_next_question())
    print(questions.get_next_question())
    print(questions.get_next_question())
