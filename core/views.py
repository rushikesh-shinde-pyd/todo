# django imports
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.http import HttpResponseNotAllowed
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.text import slugify
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test

# local imports
from .models import *
from .forms import SignupForm, ListForm, TaskForm

# third-party imports
from itertools import chain

User = get_user_model()


@login_required
def index(request):
    """ Renders lists created by logged in user. ie. homepage """

    context = {}
    context['list'] = TodoList.objects.filter(user=request.user)
    return render(request, 'core/index.html', context)


# TODO list operations
@login_required
def list_create(request, *args, **kwargs):
    """ Create todo list with provided data and render empty form. """
    context = {}
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, '"%s" list created'%(obj.title))
            return HttpResponseRedirect(reverse('core:index'))
        else:
            context['form'] = form
            return render(request, 'core/list-create.html', context)
    else:
        context['form'] = ListForm()
        return render(request, 'core/list-create.html', context)
    

@login_required
def list_update(request, *args, **kwargs):
    """ Update todo list. """
    context = {}
    if request.method == 'POST':
        obj = TodoList.objects.get(slug=kwargs.get('title'))
        form = ListForm(request.POST, instance=obj)
        if form.is_valid():
            if form.has_changed():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
                messages.success(request, '"%s" list updated'%(obj.title))
                return HttpResponseRedirect(reverse('core:index'))
            else:
                messages.info(request, 'Nothing has updated')
                return HttpResponseRedirect(reverse('core:index'))
        else:
            context['form'] = form
            return render(request, 'core/list-update.html', context)
    else:
        obj = TodoList.objects.get(slug=kwargs.get('title'), user=request.user)
        context['form'] = ListForm(instance=obj)
        return render(request, 'core/list-update.html', context)



@login_required
def list_detail(request, *args, **kwargs):
    """ Renders todo list details. """
    context = {}
    try:
        obj = TodoList.objects.get(slug=kwargs.get('title'))
        context['object'] = obj
        return render(request, 'core/list-detail.html', context)
    except TodoList.DoesNotExist as e:
        return HttpResponseRedirect(reverse('core:index'))
    return render(request, 'core/index.html', context)


@login_required
def list_delete(request, *args, **kwargs):
    """ Prompts user for the deletion of todo list. """
    context = {}
    try:
        obj = TodoList.objects.get(slug=kwargs.get('title'))
        context['object'] = obj
        return render(request, 'core/list-delete-confirm.html', context)
    except TodoList.DoesNotExist as e:
        return HttpResponseRedirect(reverse('core:index'))
    return render(request, 'core/index.html', context)


@login_required
def list_delete_confirm(request, *args, **kwargs):
    """ Delete todo list after confirmation. """
    context = {}
    try:
        obj = TodoList.objects.get(slug=kwargs.get('title'))
        messages.success(request, '"%s" deleted'%(obj.title))
        obj.delete()
        return HttpResponseRedirect(reverse('core:index'))
    except TodoList.DoesNotExist as e:
        return HttpResponseRedirect(reverse('core:list-detail', kwargs={'title': kwargs.get('title')}))


# TODO task operations

@login_required
def task_create(request, *args, **kwargs):
    """ Creates task and add to the list. """
    context = {}
    instance = TodoList.objects.get(slug=kwargs.get('title'))
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.td_list = instance
            obj.save()
            messages.success(request, '"%s" task created'%(obj.title))
            return HttpResponseRedirect(reverse('core:list-detail', kwargs={'title': instance.slug}))
        else:
            context['form'] = form
            context['object'] = instance
            return render(request, 'core/task-create.html', context)
    else:
        context['object'] = instance
        context['form'] = TaskForm()
        return render(request, 'core/task-create.html', context)
    

@login_required
def task_update(request, *args, **kwargs):
    """ Update todo task. """
    context = {}
    instance = TodoList.objects.get(slug=kwargs.get('title'))
    obj = TodoItem.objects.get(slug=kwargs.get('task'))
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=obj)
        if form.is_valid():
            if form.has_changed():
                obj = form.save(commit=False)
                obj.td_list = instance
                obj.save()
                messages.success(request, '"%s" task updated'%(obj.title))
                return HttpResponseRedirect(reverse('core:list-detail', kwargs={'title': instance.slug}))
            else:
                messages.info(request, 'Nothing has updated')
                return HttpResponseRedirect(reverse('core:list-detail', kwargs={'title': instance.slug}))
        else:
            context['form'] = form
            context['object'] = instance
            context['task'] = obj
            return render(request, 'core/task-update.html', context)
    else:
        context['object'] = instance
        context['task'] = obj
        context['form'] = TaskForm(instance=obj)
        return render(request, 'core/task-update.html', context)
    

@login_required
def task_delete(request, *args, **kwargs):
    """ Prompts user for the deletion of todo task. """
    context = {}
    try:
        obj = TodoList.objects.get(slug=kwargs.get('title'))
        task = TodoItem.objects.get(slug=kwargs.get('task'))
        context['object'] = obj
        context['task'] = task
        return render(request, 'core/task-delete-confirm.html', context)
    except TodoList.DoesNotExist as e:
        return HttpResponseRedirect(reverse('core:index'))
    return render(request, 'core/index.html', context)


@login_required
def task_delete_confirm(request, *args, **kwargs):
    """ Delete todo task after confirmation. """
    context = {}
    try:
        obj = TodoItem.objects.get(slug=kwargs.get('task'))
        messages.success(request, '"%s" deleted'%(obj.title))
        obj.delete()
        return HttpResponseRedirect(reverse('core:list-detail', kwargs={'title': kwargs.get('title')}))
    except TodoList.DoesNotExist as e:
        return HttpResponseRedirect(reverse('core:list-detail', kwargs={'title': kwargs.get('title')}))


@login_required
def profile(request, *args, **kwargs):
    """ Display details of logged in user. """
    context = {}
    return render(request, 'registration/profile.html', context)


def signup(request, *args, **kwargs):
    """ Render signup form and create user and profile object. """
    context = {}
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data.get('username'), 
                password=data.get('password1'),
                email=data.get('email'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name')
            )
            profile = Profile.objects.get(user=user)
            profile.mobile = data.get('mobile')
            profile.city = data.get('city')
            profile.gender = data.get('gender')
            profile.dob = data.get('dob')
            profile.save()
            messages.success(request, 'You have successfully signed up')
            return HttpResponseRedirect(reverse('login'))
        else:
            context['form'] = form
            return render(request, 'registration/signup.html', context)            
    else:        
        context['form'] = SignupForm()
        return render(request, 'registration/signup.html', context)

def search_list_or_task(request, *args, **kwargs):
    context = {}
    q = request.GET.get('query').strip()
    if q:
        if TodoList.objects.filter(Q(user=request.user, title__iexact=q)).exists():
            obj = TodoList.objects.get(user=request.user, title__iexact=q)
            return HttpResponseRedirect(reverse('core:list-detail', kwargs={'title': obj.slug}))
        else:   
            lists = TodoList.objects.filter(
                    Q(user=request.user) &
                    Q(title__icontains=q)
                ).distinct()
            tasks = TodoItem.objects.filter(
                    Q(td_list__user=request.user) &
                    Q(title__icontains=q)
                ).distinct()
            context['results'] = list(chain(lists, tasks))
            return render(request, 'core/search-results.html', context)
    else:
        return render(request, 'core/search-results.html', context)