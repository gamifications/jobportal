
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Keyword(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name


class Candidate(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=300)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at =  models.DateTimeField(auto_now_add=True)
    keywords = models.ManyToManyField(Keyword,through='JobKeywords')
    candidate = models.ManyToManyField(Candidate)
    def __str__(self):
        return self.title

class JobKeywords(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
