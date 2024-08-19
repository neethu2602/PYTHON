from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    skill = models.TextField(blank=True, null=True)  # Added field
    contact = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

# projects/models.py

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True, null=True)
    title = models.CharField(max_length=200, blank=True)

class Project(models.Model):
    portfolio = models.ForeignKey('Portfolio', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class WorkExperience(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE,blank=True, null=True)
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    document = models.FileField(upload_to='work_experience_documents/', blank=True, null=True)

class Education(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE,blank=True, null=True)
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    graduation_date = models.DateField()
    document = models.FileField(upload_to='work_experience_documents/', blank=True, null=True)

class Certification(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    issue_date = models.DateField()
    document = models.FileField(upload_to='work_experience_documents/', blank=True, null=True)

# portfolio/forms.py




