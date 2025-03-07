from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    RATING_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]

    title = models.CharField(max_length=200)
    book_title = models.CharField(max_length=200, default='')
    book_author = models.CharField(max_length=200, default='')
    genre = models.ManyToManyField(Genre, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES, default=3)
    content = models.TextField(help_text="Share your thoughts about the book")
    book_cover = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[
        ('draft', 'Draft'),
        ('published', 'Published')
    ], default='draft')
    reading_status = models.CharField(max_length=20, choices=[
        ('currently_reading', 'Currently Reading'),
        ('finished', 'Finished'),
        ('want_to_read', 'Want to Read'),
        ('dnf', 'Did Not Finish')
    ], default='finished')
    recommended = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f"Review: {self.book_title} by {self.book_author}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
