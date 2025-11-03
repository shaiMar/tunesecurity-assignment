import argparse
import json
import os
import ssl
import urllib.request
import urllib.error

from config import DEFAULT_TERMINAL_WIDTH
from questions_manager import QuestionsManager, convert_web_question
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
        questions_file = "questions.json"

    if not os.path.exists(questions_file):
        raise FileNotFoundError(f"Questions file not found: {questions_file}")

    with open(questions_file, "r", encoding="utf-8") as f:
        questions_data = json.load(f)

    return QuestionsManager(questions_data)


def get_questions_from_web(num_questions):
    """
    Fetch questions from the web using Open Trivia Database API.

    Args:
        num_questions: Number of questions to fetch from the web

    Returns:
        QuestionsManager: An instance of QuestionsManager with fetched questions

    Raises:
        Exception: If unable to fetch questions from the web
    """
    url = f"https://opentdb.com/api.php?amount={num_questions}"

    try:
        # Create an SSL context that doesn't verify certificates
        ssl_context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, timeout=10, context=ssl_context) as response:
            data = json.loads(response.read().decode())

            if data["response_code"] != 0:
                raise Exception(f"API returned error code: {data['response_code']}")

            # Convert the API format to our internal format
            questions_data = []
            for item in data["results"]:
                question = convert_web_question(item)
                questions_data.append(question)

            return QuestionsManager(questions_data)

    except urllib.error.URLError as e:
        raise Exception(f"Network error while fetching questions: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON response from API: {e}")
    except Exception as e:
        raise Exception(f"Error fetching questions from web: {e}")


def parse_arguments():
    """
    Parse command line arguments for the trivia game.

    Required arguments:
    - players: Names of players (at least 2 players required)

    Optional arguments:
    - questions_file: Path to questions file (default: 'questions.json')
    - web_questions: Number of questions to fetch from the web

    Note: -w and -f cannot be used together
    """
    parser = argparse.ArgumentParser(
        description="Trivia Game - Multiple Players Support",
        epilog="Example: python run_game.py -p Alice -p Bob -p Charlie -f questions.json\n"
        "         python run_game.py -p Alice -p Bob -w 10",
    )

    # Multiple players as optional arguments with -p flag
    parser.add_argument(
        "-p",
        "--player",
        type=str,
        action="append",
        dest="players",
        help="Add a player to the game (use -p multiple times for each player). Example: -p Alice -p Bob",
    )

    parser.add_argument(
        "-f",
        "--questions_file",
        type=str,
        default=None,
        help="Path to questions file (default: questions.json)",
    )

    parser.add_argument(
        "-w",
        "--web",
        type=int,
        default=None,
        dest="web_questions",
        help="Fetch this many questions from the web (Open Trivia Database API)",
    )

    args = parser.parse_args()

    # Validate that -w and -f are not used together
    if args.web_questions is not None and args.questions_file is not None:
        parser.error(
            "Cannot use -w (web questions) and -f (questions file) together. Choose one option."
        )

    # Interactively ask for players if not provided via command line
    if not args.players:  # This handles both None and empty list
        print("\nWelcome to Trivia Game!")
        print("Please enter player names (at least 2 players required)")
        print("=" * 50)

        players = []
        player_num = 1

        while len(players) < 2:
            player_name = input(
                f"Enter name for Player {player_num} (or press Enter when done): "
            ).strip()

            if player_name:
                if player_name in players:
                    print(
                        f"'{player_name}' is already in the game! Please use a different name."
                    )
                else:
                    players.append(player_name)
                    player_num += 1
            elif len(players) >= 2:
                # User pressed Enter and we have at least 2 players
                break
            else:
                print(
                    f"At least 2 players are required! You have {len(players)} player(s)."
                )

        # Allow adding more players
        while True:
            player_name = input(
                f"Enter name for Player {player_num} (or press Enter to start): "
            ).strip()
            if not player_name:
                break
            if player_name in players:
                print(
                    f"'{player_name}' is already in the game! Please use a different name."
                )
            else:
                players.append(player_name)
                player_num += 1

        args.players = players

    # Validate minimum number of players
    if len(args.players) < 2:
        parser.error("At least 2 players are required to play the game!")

    # Print parsed parameters
    print("\n" + "=" * DEFAULT_TERMINAL_WIDTH)
    print("Game Configuration:")
    print("=" * DEFAULT_TERMINAL_WIDTH)
    print(f"Players ({len(args.players)}): {', '.join(args.players)}")
    if args.web_questions:
        print(f"Questions Source: Web (fetching {args.web_questions} questions)")
    else:
        print(f"Questions File: {args.questions_file or 'questions.json (default)'}")
    print("=" * DEFAULT_TERMINAL_WIDTH + "\n")

    return args


def start():
    """
    Main orchestration function to start the trivia game.

    This function:
    1. Parses command-line arguments (player names, number of turns, questions file)
    2. Loads questions from the specified file or web
    3. Initializes and starts the game with all players
    """
    # Parse command-line arguments
    args = parse_arguments()

    # Load questions from file or web
    try:
        if args.web_questions:
            print(f"Fetching {args.web_questions} questions from the web...")
            questions = get_questions_from_web(args.web_questions)
            print(f"Fetched {len(questions.all_questions)} questions successfully!\n")
        else:
            questions = get_questions(args.questions_file)
            print(f"Loaded {len(questions.all_questions)} questions successfully!\n")
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
    total_questions_needed = len(args.players)
    if len(questions.all_questions) < total_questions_needed:
        print(
            f"Warning: You have {len(questions.all_questions)} questions but got {len(args.players)} players."
        )
        print("Game cancelled.")
        return

    # Start the trivia game with all players and questions
    try:
        trivia.start(args.players, questions=questions)
        print("\nGame ended successfully!")
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user!")
    except Exception as e:
        print(f"\nError during game: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    start()
