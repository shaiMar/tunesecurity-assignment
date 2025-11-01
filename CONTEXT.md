# Project Context

## Overview
This is a command-line trivia/game application built in Python. The project implements a turn-based game system where multiple players can compete against each other.

## Project Structure

```
tunesecurity/
├── trivia.py          # Main game logic and TurnBaseGame class
├── player.py          # Player class definition
├── display.py         # Display/UI functions for terminal output
├── run_game.py        # Command-line argument parser and game launcher
├── config.py          # Configuration file with default parameters
├── requirements.txt   # Python dependencies (standard library only)
└── CONTEXT.md         # This file - project documentation
```

## Files Description

### trivia.py
Main game engine containing:
- `TurnBaseGame` class - Core game logic and flow control
  - Game rules (max_skips per player)
- `MenuOption` classes - Game menu options (Skip, Cancel, Continue)
  - Skip logic (validation, limit checking)
- Turn management and game state
- Input handling and game flow

### player.py
Player management module containing:
- `Player` class - Represents individual players
- Player state tracking (name, inputs, score, skips_used)
- Score calculation logic based on character counting (n, m, v)
- Skip methods:
  - `get_skips_remaining(max_skips)` - Calculate skips remaining
  - `skip()` - Increment skip counter

### display.py
Display/UI module containing:
- `clear_screen()` - Clear terminal screen
- `display_player_turn_screen()` - Show current turn information
- `display_results()` - Show final game results and winner
- All terminal output formatting and UI elements

### config.py
Configuration module containing:
- `DEFAULT_NUM_TURNS` - Default number of turns per game (default: 3)
- `DEFAULT_MAX_SKIPS` - Default maximum skips per player (default: 2)
- `DEFAULT_TERMINAL_WIDTH` - Default terminal width (default: 80)
- `SCORE_CHARACTERS` - Characters that contribute to scoring

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
- Skip turn option (limited to N times per player, default: 2)
  - Shows remaining skips in menu
  - Blocks usage when limit reached
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

## Configuration

Default game parameters are stored in `config.py`:
- **DEFAULT_NUM_TURNS**: Number of turns (default: 3)
- **DEFAULT_MAX_SKIPS**: Maximum skips per player (default: 2)
- **DEFAULT_TERMINAL_WIDTH**: Terminal width fallback (default: 80)

To change default values, edit `config.py`:
```python
DEFAULT_NUM_TURNS = 5  # Change default turns to 5
DEFAULT_MAX_SKIPS = 3  # Change default skips to 3
```

## Development

### Adding New Features
1. Game logic modifications go in `trivia.py`
2. Player-related features go in `player.py`
3. Display/UI changes go in `display.py`
4. CLI argument parsing changes go in `run_game.py`
5. Default parameter changes go in `config.py`

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

