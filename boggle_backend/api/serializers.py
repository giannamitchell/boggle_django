# serializers.py
from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Game, LeaderBoard, LeaderBoardEntry

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Works for default Django user + most custom users
        fields = ("id", "username", "email")
        read_only_fields = ("id", "username", "email")


class LeaderBoardEntrySerializer(serializers.ModelSerializer):
    # Read-only nested user for responses
    user = UserSerializer(read_only=True)

    # Optional write-time field when request.user is anonymous
    user_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = LeaderBoardEntry
        fields = (
            "id",
            "leaderboard",
            "user",
            "user_id",
            "words_found_count",
            "total_time_seconds",
            "saved_at",
        )
        read_only_fields = ("id", "saved_at")

    def validate(self, attrs):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            return attrs

        # If not authenticated, require user_id
        if not attrs.get("user_id"):
            raise serializers.ValidationError(
                {"user_id": "Required when not authenticated."}
            )
        return attrs


class LeaderBoardSerializer(serializers.ModelSerializer):
    entries = LeaderBoardEntrySerializer(many=True, read_only=True)

    class Meta:
        model = LeaderBoard
        fields = ("id", "game", "title", "entries")
        read_only_fields = ("id",)


class GameSerializer(serializers.ModelSerializer):
    leaderboard = LeaderBoardSerializer(read_only=True)

    class Meta:
        model = Game
        fields = (
            "id",
            "name",
            "size",
            "grid",
            "dictionary_language",
            "solution_words",
            "date_created",
            "leaderboard",
        )
        read_only_fields = (
            "id",
            "name",
            "grid",
            "dictionary_language",
            "solution_words",
            "date_created",
            "leaderboard",
        )