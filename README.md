# Trivia Game

A command-line multiplayer trivia game written in Python. Players take turns answering questions from various categories and compete to achieve the highest score!

## My Specific Comments for This Assignment


- **Scope:** This submission includes the entire assignment along with all requested extensions.  
- **Testing:** I haven’t written tests for this submission, but in a real-world scenario I would include unit tests for key components such as question loading, scoring logic, and player management.  
- **Design choice:** I prioritized code readability and maintainability over building for overly generic or hypothetical use cases.  
- **AI assistance:** I let AI handle parts of the error handling and most of the display layer, while the core logic and structure were implemented independently.  
- **Git workflow:** For this assignment, I used a single main branch. In a real-world scenario, I would use feature and development branches, merging them into the main (or master) branch through pull requests to maintain clean version control and review flow.
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
4. Correct answers earn points according to question difficulty
5. The game continues until all questions are answered or skipped
6. The player with the highest score wins!


## License

This project is open source and available for educational purposes.

