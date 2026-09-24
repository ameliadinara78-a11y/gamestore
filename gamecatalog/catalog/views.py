from django.views.generic import DetailView, ListView

from .models import Game, Platform, Tag


class GameListView(ListView):
    model = Game
    context_object_name = "games"
    paginate_by = 12

    def get_queryset(self):
        params = self.request.GET
        return (
            Game.objects.catalog()
            .search(params.get("q"))
            .for_tag(params.get("tag"))
            .for_platform(params.get("platform"))
            .distinct()
        )

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["catalog/partials/game_results.html"]
        return ["catalog/index.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.request.GET
        context["active_tag"] = params.get("tag", "")
        context["active_platform"] = params.get("platform", "")
        context["query"] = params.get("q", "")
        context["tags"] = Tag.objects.all()
        context["platforms"] = Platform.objects.all()
        context["total_count"] = Game.objects.published().count()
        return context


class GameDetailView(DetailView):
    model = Game
    context_object_name = "game"
    template_name = "catalog/game_detail.html"

    def get_queryset(self):
        return Game.objects.catalog()
