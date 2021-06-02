from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Job(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=300)
    created_at =  models.DateTimeField(auto_now_add=True)
    # {'WebDevelopment':['python', 'javascript'], 'Mobile Development':['flutter','react native']}
    keywords = models.JSONField(null=True)

    def __str__(self):
        return self.position

class Resume(models.Model):
    name = models.CharField(max_length=300)
    contact = models.CharField(max_length=300)
    file_data = models.TextField()    


class Applicant(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applicants")
    apply_date =  models.DateTimeField(auto_now_add=True)
    resumes = models.ManyToManyField(Resume)
