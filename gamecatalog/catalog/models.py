from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from .managers import GameManager


class SlugModel(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True, blank=True)

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class License(SlugModel):
    is_copyleft = models.BooleanField(default=False)
    url = models.URLField(blank=True)


class Platform(SlugModel):
    pass


class Tag(SlugModel):
    pass


class Game(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    summary = models.CharField(max_length=280)
    description = models.TextField(blank=True)
    license = models.ForeignKey(
        License, on_delete=models.PROTECT, related_name="games"
    )
    platforms = models.ManyToManyField(Platform, related_name="games", blank=True)
    tags = models.ManyToManyField(Tag, related_name="games", blank=True)
    homepage_url = models.URLField(blank=True)
    source_url = models.URLField(blank=True)
    stars = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GameManager()

    class Meta:
        ordering = ["-stars", "title"]
        indexes = [
            models.Index(fields=["-stars"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:game_detail", args=[self.slug])
