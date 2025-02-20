from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from myapp.forms import ProjectForm, LoginForm, RegistrationForm, ProjectImageForm, SearchByCategoryForm
from myapp.models.chat import Chat
from myapp.models.project import Project
from myapp.models.projectimage import ProjectImage

from django.views.generic.base import View

@login_required
def index(request):
    projects = Project.objects.order_by('id')
    project_images = ProjectImage.objects.order_by('id')
    return render(request, 'myapp/index.html', {'title': 'Главная страница сайта', 'projects': projects, 'project_images': project_images})

@login_required
def project_images(request, project_id):
    project = Project.objects.get(id=project_id)
    images = project.images.all()
    return render(request, 'myapp/project_images.html', {'project': project, 'images': images})


@login_required
def create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user  # Привязываем проект к текущему пользователю
            project.save()
            form.save_m2m()  # Сохраняем ManyToMany поля
            return redirect('myapp:index')
    else:
        form = ProjectForm()

    return render(request, 'myapp/create.html', {'form': form})


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('myapp:index')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'myapp/edit_project.html', {'form': form})

@login_required
def edit_project_image(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.method == 'POST':
        form = ProjectImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.project = project
            image.save()
            return redirect('myapp:index')
    else:
        form = ProjectImageForm()

    return render(request, 'myapp/edit_project_image.html', {'project': project, 'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('myapp:index')
            else:
                error_message = "Invalid username or password."
                return render(request, 'myapp/login_view.html', {'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form data."
            return render(request, 'myapp/login_view.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()

    return render(request, 'myapp/login_view.html', {'form': form})


class registration_view(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'myapp/registration_view.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('myapp:index')  # Перенаправление на PostView
        else:
            error_message = "Invalid form data."
            return render(request, 'myapp/registration_view.html', {'form': form, 'error_message': error_message})


@login_required
def search_projects_by_category(request):
    if request.method == 'GET':
        form = SearchByCategoryForm(request.GET)
        if form.is_valid():
            category = form.cleaned_data['category']
            projects = Project.objects.filter(category=category)
            context = {
                'form': form,
                'projects': projects,
            }
            return render(request, 'myapp/search_results.html', context)
    else:
        form = SearchByCategoryForm()

    context = {
        'form': form,
    }
    return render(request, 'myapp/search_by_category.html', context)


@login_required
def chat_view(request):
    messages = Chat.objects.all()
    return render(request, 'myapp/chat.html', {'messages': messages})


@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        user = request.user
        Chat.objects.create(user=user, content=content)
    return redirect('myapp:chat')
