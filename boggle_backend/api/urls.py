from django.urls import path
from .views import (
    CreateGameBySizeView,
    GameListView,
    GameDetailView,
    GameLeaderBoardView,
)

urlpatterns = [
    path("game/<int:size>/", CreateGameBySizeView.as_view(), name="create-game-by-size"),
    path("games/", GameListView.as_view(), name="game-list"),
    path("games/<uuid:id>/", GameDetailView.as_view(), name="game-detail"),
    path(
        "games/<uuid:id>/leaderboard/",
        GameLeaderBoardView.as_view(),
        name="game-leaderboard",
    ),
]