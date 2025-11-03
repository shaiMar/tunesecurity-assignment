# Trivia Game

A command-line multiplayer trivia game written in Python. Players take turns answering questions from various categories and compete to achieve the highest score!

## Features

- Multiple player support (minimum 2 players)
- Multiple question categories (history, music, science, geography, etc.)
- Player statistics tracking (correct/wrong answers, skips)
- Turn-based gameplay
- Interactive command-line interface
- Customizable question sets via JSON files

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Installation

1. Clone or download this repository
2. Navigate to the project directory:
```bash
cd tunesecurity
```

## How to Run

### Method 1: Interactive Mode (Recommended for Beginners)

Simply run the game without any arguments, and you'll be prompted to enter player names:

```bash
python run_game.py
```

The game will ask you to enter player names one by one. You need at least 2 players to start.

### Method 2: Command-Line Arguments

Specify players directly using the `-p` flag:

```bash
python run_game.py -p Alice -p Bob -p Charlie
```

### Command-Line Options

- `-p`, `--player`: Add a player to the game (use `-p` multiple times for each player)
  - Example: `-p Alice -p Bob`
- `-f`, `--questions_file`: Specify a custom questions file (default: `questions.json`)
  - Example: `-f my_questions.json`
- `-w`, `--web`: Fetch questions from the web (Open Trivia Database API)
  - Specify the number of questions to fetch
  - Example: `-w 10`
  - **Note:** Cannot be used together with `-f` option

### Examples

**Two players:**
```bash
python run_game.py -p Alice -p Bob
```

**Three players with custom questions file:**
```bash
python run_game.py -p Alice -p Bob -p Charlie -f questions_copy.json
```

**Fetch questions from the web (10 questions):**
```bash
python run_game.py -p Alice -p Bob -w 10
```

**Interactive mode (no arguments):**
```bash
python run_game.py
```

## Game Rules

1. Players take turns answering trivia questions
2. Each question belongs to a category (history, music, science, etc.)
3. Players can choose to answer or skip questions (limited skips available)
4. Correct answers earn points accroding to question difficulty
5. The game continues until all questions are answered or skipped
6. The player with the highest score wins!

## Question File Format

Questions are stored in JSON format. Each question has:
- `question`: The question text
- `right_answer`: The correct answer
- `wrong_answers`: Array of incorrect answers
- `category`: Question category
- `difficulty`: Difficulty level (1-3)

Example:
```json
[
  {
    "question": "What is the capital of France?",
    "right_answer": "Paris",
    "wrong_answers": ["London", "Berlin", "Madrid"],
    "category": "geography",
    "difficulty": 1
  }
]
```

## Project Structure

```
├── run_game.py           # Main entry point to start the game
├── trivia.py             # Core game logic
├── player.py             # Player management
├── questions_manager.py  # Question management
├── display.py            # Display and UI functions
├── config.py             # Configuration settings
├── questions.json        # Default question database
└── requirements.txt      # Project dependencies
```

## Troubleshooting

**"Questions file not found" error:**
- Make sure `questions.json` exists in the same directory as `run_game.py`
- Or specify a valid questions file using `-f` option

**"At least 2 players are required" error:**
- The game requires at least 2 players to start
- Add more players using `-p` flag or enter more names in interactive mode

## Contributing

Feel free to add your own questions to `questions.json` or create custom question files!

## License

This project is open source and available for educational purposes.

