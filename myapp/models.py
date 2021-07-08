from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.postgres.fields import IntegerRangeField
from django.urls import reverse
from django.core.validators import MinLengthValidator, FileExtensionValidator
from djstripe.models import Customer, Subscription

class User(AbstractUser):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    subscription = models.ForeignKey(Subscription, null=True, blank=True,on_delete=models.SET_NULL)
    company = models.SlugField()


class Keyword(models.Model):
    name = models.CharField(max_length=300, unique=True) #, validators=[MinLengthValidator(2)])
    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(check=~models.Q(name=""), name="non_empty_name")
        ]

class Tag(models.Model):
    name = models.CharField(max_length=300) #, validators=[MinLengthValidator(2)])
    def __str__(self):
        return self.name

class CandidateProfile(models.Model):
    STAGE_CHOICES = (
        ('', ""),
        ('shortlisted', "Shortlisted"),
        ('interview', "Interview"),
        ('hired', "Hired"),
        ('not_suitable', "Not Suitable"),
    )
    candidate = models.OneToOneField('Candidate', on_delete=models.CASCADE)
    matching_results = models.IntegerField(default=0)
    # keyword = models.IntegerField(default=0) # - Keyword 1, 2 ,3,4,5 – integer field
    status = models.CharField(max_length=20,choices=STAGE_CHOICES, default='')

class Candidate(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    email = models.EmailField()
    jobtitle = models.CharField(max_length=300, default='')
    salary = models.IntegerField(default=0)
    resume = models.FileField(null=True, blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    resume_data = models.TextField(blank=True)
    def __str__(self):
        return self.name


class Job(models.Model):
    class Meta:
        ordering = ['-created_at']
    STAGE_CHOICES = (
        ('draft', "Draft"),
        ('posted', "Posted"),
        ('shortlisted', "Shortlisted"),
        ('interview', "Interview"),
        ('hired', "Hired")
    )
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    department = models.CharField(max_length=300, blank=True)
    category = models.CharField(max_length=300, blank=True)
    salary_low = models.IntegerField(default=0) # IntegerRangeField(blank=True, null=True)
    salary_high = models.IntegerField(default=0) # IntegerRangeField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    closing_date = models.DateField(blank=True, null=True)
    reporting_line = models.CharField(max_length=300) # models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    stage = models.CharField(max_length=20,choices=STAGE_CHOICES, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True)
    created_at =  models.DateTimeField(auto_now_add=True)
    keywords = models.ManyToManyField(Keyword,through='JobKeywords')
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('job:list') #, kwargs={'pk': self.pk})

class JobKeywords(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
