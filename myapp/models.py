from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.postgres.fields import IntegerRangeField

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
    jobtitle = models.CharField(max_length=300, default='')
    salary = models.IntegerField(default=0)

    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Job(models.Model):
    STAGE_CHOICES = (
        ('draft', "Draft"),
        ('posted', "Posted"),
        ('shortlisted', "Shortlisted"),
        ('interview', "Interview"),
        ('hired', "Hired")
    )
    title = models.CharField(max_length=300)
    department = models.CharField(max_length=300, blank=True)
    category = models.CharField(max_length=300, blank=True)
    salary_low = models.IntegerField(default=0) # IntegerRangeField(blank=True, null=True)
    salary_high = models.IntegerField(default=0) # IntegerRangeField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    closing_date = models.DateField(blank=True, null=True)
    reporting_line = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    stage = models.CharField(max_length=20,choices=STAGE_CHOICES, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    created_at =  models.DateTimeField(auto_now_add=True)
    keywords = models.ManyToManyField(Keyword,through='JobKeywords')
    def __str__(self):
        return self.title

class JobKeywords(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
