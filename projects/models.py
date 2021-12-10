from django.db import models
from django.db.models.fields import CharField, DateField, TextField
from django.db.models.fields.files import ImageField
import uuid
from users.models import Profile
# Create your models here.

class Projects(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    created = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']
    @property
    def reviewers(self):
        queryset = self.review_set.alll().values_list('owner__id', flat=True)
        return queryset
    
class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.name
    
   
class Review(models.Model):
    
    owner = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    class Meta:
        unique_together = [['owner', 'project']]
    def __str__(self):
        return "Review"     