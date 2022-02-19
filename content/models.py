from django.db import models

# Create your models here.

class Content(models.Model):
    title = models.CharField(max_length=30, null=False)
    image = models.TextField(null=True)
    content = models.TextField(null=True, max_length=3000)
    nickname = models.CharField(max_length=24, null=False, default=False)
    stock = models.CharField(max_length=10, null=True)


class Reply(models.Model):
    contentId = models.IntegerField(default=0)
    nickname = models.CharField(max_length=24, null=False, default=False)
    replycontent = models.TextField(null=False, max_length=1000)
    date = models.DateField(auto_now=True)


class Like(models.Model):
    contentId = models.IntegerField(default=0)
    email = models.EmailField(max_length=40, null=False, default=False)
    isLike = models.BooleanField(default=True)


class Bookmark(models.Model):
    contentId = models.IntegerField(default=0)
    email = models.EmailField(max_length=40, null=False, default=False)
    isMarked = models.BooleanField(default=True)