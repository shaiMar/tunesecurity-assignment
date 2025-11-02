import argparse
import json
import os
from config import DEFAULT_NUM_TURNS
from questions_manager import QuestionsManager
import trivia


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
    - players: Names of players (at least 2 players required)

    Optional arguments:
    - num_questions: Number of questions (default: from config)
    - questions_file: Path to questions file (default: 'questions.json')
    """
    parser = argparse.ArgumentParser(
        description='Trivia Game - Multiple Players Support',
        epilog='Example: python run_game.py Alice Bob Charlie -n 5 -f questions.json'
    )

    # Multiple players as positional arguments
    parser.add_argument(
        'players',
        type=str,
        nargs='*',  # Accept zero or more players (we'll handle interactively if none provided)
        help='Names of players (at least 2 required). Example: Alice Bob Charlie'
    )

    # Optional arguments
    parser.add_argument(
        '-n', '--num_questions',
        type=int,
        default=DEFAULT_NUM_TURNS,
        help=f'Number of questions per player (default: {DEFAULT_NUM_TURNS})'
    )

    parser.add_argument(
        '-f', '--questions_file',
        type=str,
        default=None,
        help='Path to questions file (default: questions.json)'
    )

    args = parser.parse_args()

    # Interactively ask for players if not provided via command line
    if not args.players:
        print("\nWelcome to Trivia Game!")
        print("Please enter player names (at least 2 players required)")
        print("=" * 50)
        
        players = []
        player_num = 1
        
        while len(players) < 2:
            player_name = input(f"Enter name for Player {player_num} (or press Enter when done): ").strip()
            
            if player_name:
                if player_name in players:
                    print(f"'{player_name}' is already in the game! Please use a different name.")
                else:
                    players.append(player_name)
                    player_num += 1
            elif len(players) >= 2:
                # User pressed Enter and we have at least 2 players
                break
            else:
                print(f"At least 2 players are required! You have {len(players)} player(s).")
        
        # Allow adding more players
        while True:
            player_name = input(f"Enter name for Player {player_num} (or press Enter to start): ").strip()
            if not player_name:
                break
            if player_name in players:
                print(f"'{player_name}' is already in the game! Please use a different name.")
            else:
                players.append(player_name)
                player_num += 1
        
        args.players = players
    
    # Validate minimum number of players
    if len(args.players) < 2:
        parser.error("At least 2 players are required to play the game!")
    
    # Print parsed parameters
    print("\n" + "=" * 50)
    print("Game Configuration:")
    print("=" * 50)
    print(f"Players ({len(args.players)}): {', '.join(args.players)}")
    print(f"Number of Turns: {args.num_questions}")
    print(f"Questions File: {args.questions_file or 'questions.json (default)'}")
    print("=" * 50 + "\n")

    return args

def start():
    """
    Main orchestration function to start the trivia game.
    
    This function:
    1. Parses command-line arguments (player names, number of turns, questions file)
    2. Loads questions from the specified file
    3. Initializes and starts the game with all players
    """
    # Parse command-line arguments
    args = parse_arguments()
    
    # Load questions from file
    try:
        questions = get_questions(args.questions_file)
        print(f"Loaded {questions.available_questions_count} questions successfully!\n")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please provide a valid questions file using -f option.")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in questions file - {e}")
        return
    except Exception as e:
        print(f"Unexpected error loading questions: {e}")
        return
    
    # Check if we have enough questions for the game
    total_questions_needed = args.num_questions * len(args.players)
    if questions.available_questions_count < total_questions_needed:
        print(f"Warning: You have {questions.available_questions_count} questions but need {total_questions_needed} for this game.")
        print(f"   ({args.num_questions} turns x {len(args.players)} players)")
        
        # Ask user if they want to continue
        continue_game = input("Do you want to continue anyway? (y/n): ").strip().lower()
        if continue_game not in ['y', 'yes']:
            print("Game cancelled.")
            return
        print()
    
    # Start the trivia game with all players and questions
    try:
        trivia.start(*args.players, num_of_turns=args.num_questions, questions=questions)
        print("\nGame ended successfully!")
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user!")
    except Exception as e:
        print(f"\nError during game: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    start()

