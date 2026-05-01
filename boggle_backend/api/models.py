 

# Create your models here.
 
# models.py
from __future__ import annotations
from django.db import models

import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


User = get_user_model()


class Game(models.Model):
    """
    Represents a single Boogle puzzle instance (solitaire).
    Stores the grid, dictionary reference, and pre-computed solution words.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=200)
    size = models.PositiveIntegerField(validators=[MinValueValidator(2)])

    # Grid stored as JSON. Expected shape: size x size, e.g. [["A","B"],["C","D"]]
    grid = models.JSONField()

    # Dictionary Language. By default this is "English". You can replace with a other language as a stretch goal.
    dictionary_language = models.CharField(max_length=25, default="English")

    # Precomputed solver output. Store as a list of unique words, e.g. ["CAT","DOG",...]
    solution_words = models.JSONField(default=list, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Name: {self.name} Size: {self.size} Grid: {self.grid}'


class LeaderBoard(models.Model):
    """
    One leaderboard per game. Holds many LeaderBoardEntry records.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    game = models.OneToOneField(
        Game,
        on_delete=models.CASCADE,
        related_name="leaderboard",
    )

    title = models.CharField(max_length=200, blank=True, default="")

    def __str__(self) -> str:
        return self.title or f"Leaderboard for {self.game.name}"


class LeaderBoardEntry(models.Model):
    """
    A saved result for a completed play-through of a game.
    Per requirements, it stores:
      - user
      - number of words found
      - total time for the game
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    leaderboard = models.ForeignKey(
        LeaderBoard,
        on_delete=models.CASCADE,
        related_name="entries",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="boogle_leaderboard_entries",
    )

    words_found_count = models.PositiveIntegerField(default=0)
    total_time_seconds = models.PositiveIntegerField(default=0)

    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["total_time_seconds", "-words_found_count", "-saved_at"]
        indexes = [
            models.Index(fields=["leaderboard", "total_time_seconds"]),
            models.Index(fields=["leaderboard", "words_found_count"]),
        ]

    def __str__(self) -> str:
        return (
            f"{self.user} - {self.words_found_count} words "
            f"in {self.total_time_seconds}s ({self.leaderboard})"
        )