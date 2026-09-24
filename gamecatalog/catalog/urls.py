from django.urls import path

from .views import GameDetailView, GameListView

app_name = "catalog"

urlpatterns = [
    path("", GameListView.as_view(), name="index"),
    path("games/<slug:slug>/", GameDetailView.as_view(), name="game_detail"),
]
