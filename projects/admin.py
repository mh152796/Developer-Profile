from django.contrib import admin

# Register your models here.
from .models import Projects, Tag, Review

admin.site.register(Projects)
admin.site.register(Tag)
admin.site.register(Review)
