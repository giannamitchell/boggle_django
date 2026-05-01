from __future__ import annotations
from django.shortcuts import render

# Create your views here.
# views.py
 
import random
import string
from typing import List
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.staticfiles import finders

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from random import randrange
from .randomGen import *
from .readJSONFile import *
from .boggle_solver import *

from .models import Game, LeaderBoard, LeaderBoardEntry
from .serializers import (
    GameSerializer,
    LeaderBoardEntrySerializer,
    LeaderBoardSerializer,
    UserSerializer,
)

User = get_user_model()


class CreateGameBySizeView(APIView):
    """
    GET /game/{size}
    Creates, persists, and returns a new Game with:
        - random grid of given size
        - dictionary (default or query param ?dictionary=...)
        - solution_words via Boggle_solver.getSolutions(grid, dictionary)
        - date_created auto set
        - leaderboard auto created
    """
    permission_classes = [AllowAny]

    def get(self, request, size: int):

        # Basic guardrails
        if size < 3 or size > 10:
            return Response(
                {"detail": "size must be between 3 and 10."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Look for query parameter "dictionary"
        dictionary_language = request.query_params.get("dictionary", "English")

        try:
            with transaction.atomic():
                grid = random_grid(size)
                
                # 2. ADD THESE TWO LINES BACK:
                now = datetime.now()
                gname = f"Random{size}Grid:{now.strftime('%Y-%m-%d %H:%M:%S')}"
                # 1. Determine which file to open based on the language
                # Make sure these files actually exist in your api/ folder!
                if dictionary_language.lower() == "spanish":
                    file_path = "api/dictionary_es.json"
                 
                else:
                    file_path = "api/dictionary.json" # Default English

                # 2. Use that specific file
                dictionary = read_json_to_list(file_path)

                # ... (rest of your code remains the same)
                 
                mygame = Boggle(grid, dictionary)

                 
                # Solver call
                 
                foundwords = mygame.getSolution()

                # Normalize words
                normalized = sorted({
                    str(w).strip().upper()
                    for w in foundwords
                    if str(w).strip()
                })

                # Create Game
                game = Game.objects.create(
                    name=gname,
                    size=size,
                    grid=grid,
                    dictionary_language=dictionary_language,
                    solution_words=normalized,
                )

                # Create LeaderBoard
                LeaderBoard.objects.create(
                    game=game,
                    title=f"Leaderboard for {game.name}",
                )

            return Response(
                GameSerializer(game).data,
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"detail": f"Game creation failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GameListView(APIView):
    """
    GET /games
    Lists all games (most recent first).
    """
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Game.objects.all().order_by("-date_created")
        return Response(GameSerializer(qs, many=True).data)


class GameDetailView(APIView):
    """
    GET /games/{id}
    Returns a game by UUID.
    """
    permission_classes = [AllowAny]

    def get(self, request, id):
        game = get_object_or_404(Game, id=id)
        return Response(GameSerializer(game).data)


class GameLeaderBoardView(APIView):
    """
    GET  /games/{id}/leaderboard
    POST /games/{id}/leaderboard
    """
    permission_classes = [AllowAny]

    def get(self, request, id):
        game = get_object_or_404(Game, id=id)
        leaderboard = getattr(game, "leaderboard", None)

        if leaderboard is None:
            leaderboard = LeaderBoard.objects.create(
                game=game,
                title=f"Leaderboard for {game.name}",
            )

        return Response(LeaderBoardSerializer(leaderboard).data)

    def post(self, request, id):
        game = get_object_or_404(Game, id=id)
        leaderboard = getattr(game, "leaderboard", None)

        if leaderboard is None:
            leaderboard = LeaderBoard.objects.create(
                game=game,
                title=f"Leaderboard for {game.name}",
            )

        serializer = LeaderBoardEntrySerializer(
            data={**request.data, "leaderboard": str(leaderboard.id)},
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        # Determine user
        if request.user and request.user.is_authenticated:
            user = request.user
        else:
            user_id = serializer.validated_data.pop("user_id")
            user = get_object_or_404(User, id=user_id)

        entry = LeaderBoardEntry.objects.create(
            leaderboard=leaderboard,
            user=user,
            words_found_count=serializer.validated_data.get("words_found_count", 0),
            total_time_seconds=serializer.validated_data.get("total_time_seconds", 0),
        )

        return Response(
            LeaderBoardEntrySerializer(entry).data,
            status=status.HTTP_201_CREATED,
        )