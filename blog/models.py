from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models import Q


class PostQuerySet(models.QuerySet):
    def search(self, query):
        lookup = Q(title__icontains=query) | Q(text__icontains=query)
        return self.filter(lookup)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)


class Post(
    models.Model
):  # Means that the Post is a Django Model, so Django knows that it should be saved in the database.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    objects = PostManager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/post/{self.pk}"  # /blog/<slug>

    def get_delete_url(self):
        return f"/post/{ self.pk }/delete"

    def get_edit_url(self):
        return f"/post/{ self.pk }/edit"