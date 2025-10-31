# Project Context

## Overview
This is a command-line trivia/game application built in Python. The project implements a turn-based game system where multiple players can compete against each other.

## Project Structure

```
tunesecurity/
├── trivia.py          # Main game logic and TurnBaseGame class
├── player.py          # Player class definition
├── run_game.py        # Command-line argument parser and game launcher
├── requirements.txt   # Python dependencies (standard library only)
└── CONTEXT.md         # This file - project documentation
```

## Files Description

### trivia.py
Main game engine containing:
- `TurnBaseGame` class - Core game logic and flow control
- `MenuOption` classes - Game menu options (Skip, Cancel, Continue)
- Game display and turn management
- Scoring system based on character counting (n, m, v)

### player.py
Player management module containing:
- `Player` class - Represents individual players
- Player state tracking (name, inputs, score)
- Score calculation logic

### run_game.py
Command-line interface containing:
- Argument parser for player names and game configuration
- Interactive prompts for missing parameters
- Game launcher entry point

## How to Run

### Basic Usage
```bash
python run_game.py
```
You'll be prompted to enter player names interactively.

### With Command Line Arguments
```bash
python run_game.py Player1 Player2 -n 10 -f questions.txt
```

Arguments:
- `player1`: Name of first player (required)
- `player2`: Name of second player (required)
- `-n, --num_questions`: Number of questions (default: 10)
- `-f, --questions_file`: Path to questions file (optional)

## Game Features

### Gameplay
- Turn-based system with multiple players
- Score tracking based on inputs
- Real-time score display
- Skip turn option
- Cancel game option
- Final results and winner announcement

### Scoring System
Players earn points based on character count in their inputs:
- Each 'n', 'm', or 'v' character (case insensitive) = 1 point
- Skipped turns don't contribute to score

## Technical Details

### Python Version
- Requires Python 3.6+

### Dependencies
- No external dependencies
- Uses only Python standard library:
  - `argparse` - command-line parsing
  - `os` - system operations
  - `sys` - system-specific parameters

## Development

### Adding New Features
1. Game logic modifications go in `trivia.py`
2. Player-related features go in `player.py`
3. CLI changes go in `run_game.py`

### Testing
Run the game with test players:
```bash
python trivia.py
```

## Future Enhancements
- Add question file loading functionality
- Implement different game modes
- Add more scoring mechanisms
- Support for more than 2 players
- Save/load game state
- Leaderboard system

