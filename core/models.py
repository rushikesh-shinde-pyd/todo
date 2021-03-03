# django imports
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

# third-party imports 
import uuid
from datetime import datetime

# local imports
from .choices import *
from .validators import validate_mobile


User = get_user_model()


class CommonFields(models.Model):
    title           =   models.CharField(max_length=50, unique=True) 
    date_created    =   models.DateTimeField('created', auto_now_add=True, editable=False, blank=True)
    date_updated    =   models.DateTimeField('updated', auto_now=True, editable=False, blank=True)
    slug            =   models.SlugField(max_length=100, unique=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    picture = models.FileField('profile picture', upload_to='profile_pictures', null=True, blank=True)
    dob = models.DateField('Date of Birth', null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=6, null=True, blank=True)
    mobile = models.CharField(max_length=10, unique=True, null=True, blank=True)
    city = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return 'profile - %s' %self.user.get_full_name()


class TodoList(CommonFields):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists', null=True)
    is_pinned = models.BooleanField(default=False, null=True) 

    def get_absolute_url(self):
        return reverse('core:list-detail', kwargs={'title': self.slug})

    def get_list_delete_url(self):
        return reverse('core:list-delete', kwargs={'title': self.slug})

    def get_list_delete_confirm_url(self):
        return reverse('core:list-delete-confirm', kwargs={'title': self.slug})

    def get_list_update_url(self):
        return reverse('core:list-update', kwargs={'title': self.slug})
    
    def __str__(self):
        return self.slug    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs) 

    class Meta:
        ordering = ['-date_updated']


class TodoItem(CommonFields):
    td_list         = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name='list', null=True, blank=True)
    action          = models.CharField(choices=ACTIONS, max_length=50, null=True, default=ACTIONS[0][0])

    def get_task_delete_url(self):
        return reverse('core:task-delete', kwargs={'title': self.td_list.slug, 'task': self.slug})

    def get_task_delete_confirm_url(self):
        return reverse('core:task-delete-confirm', kwargs={'title': self.td_list.slug, 'task': self.slug})

    def get_task_update_url(self):
        return reverse('core:task-update', kwargs={'title': self.td_list.slug, 'task': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug   

    class Meta:
        ordering = ['-date_updated']