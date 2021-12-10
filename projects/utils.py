from .models import Projects, Tag
from django.db.models import Q


def searchProject(request):
    search_query = ''
    if request.GET.get('text'):
        search_query = request.GET.get('text')
    
    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Projects.objects.distinct().filter(
        Q(title__icontains=search_query) | 
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in = tags)
    )
    
    return projects, search_query