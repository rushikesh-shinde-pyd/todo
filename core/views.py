# django imports
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.http import HttpResponseNotAllowed
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.text import slugify
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test

# third-party imports

# local imports
from .models import *
from .forms import SignupForm, ListCreateForm, ListUpdateForm


User = get_user_model()

def get_cleaned_data(data):
    print(data)
    cleaned_data = {}
    for key, value in data.items():
        if value.strip():
            cleaned_data[key] = value.strip()
        else:
            cleaned_data = None
            break
    return cleaned_data


@login_required
def index(request):
    context = {}
    # context['pending'] = TodoItem.objects.filter(action='pending').order_by('title')
    context['list'] = TodoList.objects.filter(user=request.user, is_pinned=True)
    print(context['list'], request.user)
    return render(request, 'core/index.html', context)


# TODO list operations
@login_required
def list_create(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        form = ListCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, '"%s" list created'%(obj.title.title()))
            return HttpResponseRedirect(reverse('core:index'))
        else:
            context['form'] = form
            return render(request, 'core/list-create.html', context)
    else:
        context['form'] = ListCreateForm()
        return render(request, 'core/list-create.html', context)
    

@login_required
def list_update(request, *args, **kwargs):
    context = {}
    # if request.method == 'POST':
    #     cleaned_data = get_cleaned_data(request.POST)
    #     if cleaned_data:
    #         instance = TodoList.objects.get(slug=kwargs.get('title'))
    #         instance.title       = cleaned_data.get('list-title', instance.title)
    #         instance.is_pinned   = True if cleaned_data.get('is_pinned') else False
    #         try:
    #             instance.save()
    #         except IntegrityError as e:
    #             messages.error(request, 'List name already exists')
    #             return HttpResponseRedirect(reverse('core:list-update', kwargs={'title': kwargs.get('title')}))
    #         else:
    #             instance.refresh_from_db()
    #             messages.success(request, 'List updated')
    #             return HttpResponseRedirect(reverse('core:list-detail', kwargs={'title': instance.slug}))
    #     else:
    #         messages.error(request, 'Invalid list name')
    #         return HttpResponseRedirect(reverse('core:list-update', kwargs={'title': kwargs.get('title')}))
    # elif request.method == 'GET':
    #     context['object'] = TodoList.objects.get(slug=kwargs.get('title'))
    #     return render(request, 'core/list-update.html', context)
    if request.method == 'POST':
        form = ListCreateForm(request.POST)
        # obj = TodoList.objects.get(slug=kwargs.get('title'), user=request.user)
        if form.is_valid():
            form = ListCreateForm(request.POST, instance=obj)
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, '"%s" list created'%(obj.title.title()))
            return HttpResponseRedirect(reverse('core:index'))
        else:
            context['form'] = form
            return render(request, 'core/list-update.html', context)
    else:
        obj = TodoList.objects.get(slug=kwargs.get('title'), user=request.user)
        context['form'] = ListCreateForm(instance=obj)
        return render(request, 'core/list-update.html', context)



@login_required
def list_detail(request, *args, **kwargs):
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
    context = {}
    try:
        obj = TodoList.objects.get(slug=kwargs.get('title'))
        messages.success(request, '"%s" deleted'%(obj.title.title()))
        obj.delete()
        return HttpResponseRedirect(reverse('core:index'))
    except TodoList.DoesNotExist as e:
        return HttpResponseRedirect(reverse('core:list-detail', kwargs={'title': kwargs.get('title')}))


# TODO task operations

@login_required
def task_create(request, *args, **kwargs):
    context = {}
    try:
        if request.method == 'POST':
            data = request.POST
            cleaned_data = get_cleaned_data(request.POST)
            print(cleaned_data)
            if cleaned_data:
                queryset = TodoItem.objects.filter(title=cleaned_data.get('task-title'))
                if queryset.exists():
                    messages.error(request, 'Task name already exists')
                    context['object'] = TodoList.objects.get(slug=kwargs.get('title'))
                    context['task_title'] = cleaned_data.get('task-title')
                    return render(request, 'core/task-create.html', context)
                else:            
                    l = TodoList.objects.get(slug=kwargs.get('title'))
                    obj = TodoItem.objects.create(td_list=l, title=cleaned_data.get('task-title').lower(), action=cleaned_data.get('action'))
                    messages.success(request, '"%s" task created'%(obj.title.title()))
                    return HttpResponseRedirect(reverse('core:list-detail', kwargs={'title': kwargs.get('title')}))
            else:
                print('sadfasfd')
                context['object'] = TodoList.objects.get(slug=kwargs.get('title'))
                messages.error(request, 'Invalid list name')
                return render(request, 'core/task-create.html', context)
        elif request.method == 'GET':
            print('yass')
            context['object'] = TodoList.objects.get(slug=kwargs.get('title'))
            return render(request, 'core/task-create.html', context)
    except Exception as e:
        print('*'*10, e)
        return HttpResponseNotAllowed('<h1>Not allowed method</h1>')


@login_required
def task_update(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        cleaned_data = get_cleaned_data(request.POST)
        if cleaned_data:
            instance = TodoItem.objects.get(slug=kwargs.get('task'))
            instance.title       = cleaned_data.get('list-title', instance.title)
            instance.action      = cleaned_data.get('action')
            try:
                instance.save()
            except IntegrityError as e:
                messages.error(request, 'Task title already exists')
                return HttpResponseRedirect(reverse('core:task-update', kwargs={'title': kwargs.get('title'), 'task': kwargs.get('task')}))
            else:
                instance.refresh_from_db()
                messages.success(request, 'Task updated')
                print('something')
                return HttpResponseRedirect(reverse('core:list-detail', kwargs={'title': instance.slug}))
        else:
            messages.error(request, 'Invalid task name')
            return HttpResponseRedirect(reverse('core:list-update', kwargs={'title': kwargs.get('title'), 'task': kwargs.get('task')}))
    elif request.method == 'GET':
        context['object'] = TodoItem.objects.get(slug=kwargs.get('task'))
        context['list'] = TodoList.objects.get(slug=kwargs.get('title'))
        return render(request, 'core/task-update.html', context)


@login_required
def task_delete(request, *args, **kwargs):
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
    context = {}
    try:
        obj = TodoItem.objects.get(slug=kwargs.get('task'))
        messages.success(request, '"%s" deleted'%(obj.title.title()))
        obj.delete()
        return HttpResponseRedirect(reverse('core:list-detail', kwargs={'title': kwargs.get('title')}))
    except TodoList.DoesNotExist as e:
        return HttpResponseRedirect(reverse('core:list-detail', kwargs={'title': kwargs.get('title')}))


@login_required
def profile(request, *args, **kwargs):
    context = {}
    context['list'] = TodoList.objects.filter(user=request.user)
    return render(request, 'registration/profile.html', context)


# def check_user(user):
#     if user.is_authenticated:
#         # print(user, '*'*10)
#         # return redirect('/login/')
#         return None


# @user_passes_test(check_user, login_url='/')
def signup(request, *args, **kwargs):
    print(request.user)
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