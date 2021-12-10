from django import forms
from django.shortcuts import render, redirect
from .models import Projects
from .forms import ProjectForm, ReviewForm
from django.contrib import messages
from .utils import searchProject
from django.contrib.auth.decorators import login_required

# Create your views here.

def projects(request):
    
    project, search_query = searchProject(request)
    context = {'projects':project}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    project = Projects.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()
        messages.success(request, 'your review was succfully submitted!')
        return redirect('single-project', project.id)
    context = {'project':project,'form':form}
    return render(request, 'projects/single-project.html', context)


def createProject(request):
    form = ProjectForm()
     
    if request.method == 'POST':
         form = ProjectForm(request.POST, request.FILES)
         if form.is_valid():
             project = form.save(commit=False)
     
    context = {'form':form}
     
    return render(request, 'users/project-form.html', context)

@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            form.save()
            return redirect('account')
    context = {'form':form}
    return render(request, 'projects/project-form.html',context)


@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.projects_set.get(id=pk)
    form = ProjectForm(instance=project)
    
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form}
    return render(request, 'projects/project-form.html',context)
@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.projects_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    context = {'object':project}
    
    return render(request, 'delete-template.html',context)

    
    


