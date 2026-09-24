from django.db import models
from django.db.models import Q


class GameQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def with_related(self):
        return self.select_related("license").prefetch_related("platforms", "tags")

    def search(self, term):
        term = (term or "").strip()
        if not term:
            return self
        return self.filter(
            Q(title__icontains=term)
            | Q(summary__icontains=term)
            | Q(tags__name__icontains=term)
        ).distinct()

    def for_tag(self, slug):
        slug = (slug or "").strip()
        if not slug:
            return self
        return self.filter(tags__slug=slug)

    def for_platform(self, slug):
        slug = (slug or "").strip()
        if not slug:
            return self
        return self.filter(platforms__slug=slug)


class GameManager(models.Manager.from_queryset(GameQuerySet)):
    def catalog(self):
        return self.published().with_related()
