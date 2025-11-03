"""
Player module for Trivia game.
"""

from typing import List

from config import DEFAULT_MAX_SKIPS


class Player:
    """Represents a player in the Trivia game."""

    def __init__(self, name, idx):
        """
        Initialize a player.

        Args:
            name (str): The player's name
            idx (int): The player's index in the game
        """
        self._name = name
        self.score = 0
        self.skips_used = 0
        self._idx = idx
        self.last_played_turn = 0
        self.max_skips_allowed = DEFAULT_MAX_SKIPS
        self.last_question = None

    @property
    def name(self):
        """Get the player's name."""
        return self._name

    @property
    def idx(self):
        """Get the player's index."""
        return self._idx

    def get_index(self):
        """Get the player's index."""
        return self._idx

    def update_last_question(self, question):
        self.last_question = question

    def get_last_question(self):
        return self.last_question

    def get_skips_remaining(self):
        """
        Get the number of skips remaining for this player.

        Args:
            max_skips (int): Maximum number of skips allowed (from game rules)

        Returns:
            int: Number of skips remaining
        """
        return self.max_skips_allowed - self.skips_used

    def skip_turn(self):
        """
        Mark that the player used a skip.
        Increments the skips_used counter.
        """
        self.skips_used += 1
        self.last_played_turn += 1

    def played_turn(self, score: int):
        self.last_played_turn += 1
        self.score += score

    def __str__(self):
        """String representation of the player."""
        return self.name


class Players:
    def __init__(self, player_names: list):
        """Initialize the Players collection."""
        self.players: List[Player] = [
            Player(name, i) for i, name in enumerate(player_names)
        ]
        self.name_to_player_idx = {player.name: player.idx for player in self.players}
        self._current_index = 0  # For rotation

    def get_by_index(self, index):
        return self.players[index]

    def get_by_name(self, name):
        idx = self.name_to_player_idx.get(name)
        if idx is not None:
            return self.players[idx]
        return None

    def get_all_players(self):
        return self.players

    def get_player_count(self):
        return len(self.players)

    def get_next_player(self, idx=None) -> Player:
        """
        Get the next player in rotation.

        Returns:
            Player: Return The next player in the sequence and updates the current index.
        """
        if idx is None:
            player = self.players[self._current_index]
            self._current_index = (self._current_index + 1) % len(self.players)
        else:
            player = self.players[idx]
            self._current_index = (idx + 1) % len(self.players)
        return player

    def who_is_the_next_player(self) -> Player:
        """
        Peek at who is the next player without changing the current index.

        Returns:
            Player: The next player in the sequence.
        """
        return self.players[self._current_index]

    def __iter__(self):
        return iter(self.players)
