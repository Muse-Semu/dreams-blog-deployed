from audioop import reverse
from distutils.command.upload import upload
from distutils.filelist import FileList
from email.policy import default
from random import choices
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone
import math
post_catagory = [
    ('sports', 'Sports'),
    ('technology', 'Technology'),
    ('entertainment', 'Entertainment'),
    ('science', 'Science'),
    ('other', 'Other'),
    ('fashion', 'Fashion'),

]


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True)
    title = models.CharField(max_length=200)
    discription = models.TextField(null=True, blank=True)
    articles = RichTextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    image = models.ImageField(null=True, blank=True, upload_to='image')
    videos = models.FileField(null=True, blank=True, upload_to='image')
    catagory = models.CharField(max_length=200, choices=post_catagory)
    liked = models.ManyToManyField(
        User, default=None, related_name='liked', blank=True)
    unliked = models.ManyToManyField(
        User, default=None, related_name='unliked', blank=True)
    is_video = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def num_like(self):
        return self.like.all().count()

    class Meta:
        ordering = ['-created','-updated']

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "defualt.png"

    @property
    def get_video_url(self):
        if self.videos and hasattr(self.videos, 'url'):
            return self.videos.url
        else:
            return "/static/images/defualt.png"

    def whenupdated(self):
        now = timezone.now()

        diff = now - self.updated

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.post)


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.post)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='image',blank=True,null=True)
    bios = models.TextField(null=True, blank=True)
    youtube_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    telegram_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.user} Profile'

    @property
    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return "/images/defualt.png"

class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(
        Post, related_name='comment', on_delete=models.CASCADE)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return f'{self.post.title,self.user}'

    def whenpublished(self):
        now = timezone.now()

        diff = now - self.date_added

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, related_name='reply', on_delete=models.CASCADE)
    reply = models.TextField()
    reply_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.comment.comment,self.user}'

    class Meta:
        ordering = ['-reply_date']
