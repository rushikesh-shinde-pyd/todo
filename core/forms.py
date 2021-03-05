# django imports
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

# third-party imports
import re
from datetime import date
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Button

# local imports
from .models import *
from .choices import GENDER


User = get_user_model()


class SignupForm(forms.Form):
    """ Todo signup form. """
    first_name = forms.CharField(max_length=20, min_length=3)
    last_name = forms.CharField(max_length=20, min_length=3)
    username = forms.CharField(max_length=20, min_length=3)
    email = forms.EmailField(max_length=20)
    gender = forms.ChoiceField(choices=GENDER)
    mobile = forms.CharField(max_length=10, min_length=10)
    city = forms.CharField(max_length=20, min_length=3)
    dob = forms.DateField(label='Date of Birth', initial=date(1970, 1, 1), widget=forms.DateInput(attrs={
        'type': 'date',
    }))
    password1 = forms.CharField(
        label='Password', 
        help_text='Must be between 8 and 20 characters long<br>Must contain following combinations<ul><li>Uppercase characters (A-Z)</li><li>Lowercase characters (a-z)</li><li>Number (0-9)</li><li>Special characters</li></ul>',
        max_length=20, min_length=8, widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password confirmation', max_length=20, min_length=8, widget=forms.PasswordInput())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('gender', css_class='form-group col-md-6 mb-0'),
                Column('city', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('mobile', css_class='form-group col-md-6 mb-0'),
                Column('dob', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Signup', css_class='w-100')
        )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Profile.objects.filter(user__username=username).exists():
            raise ValidationError('Username already taken')
        return username


    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if not date(1970, 1, 1) < dob < date(2010, 1, 1):
            raise ValidationError('Invalid date')
        return dob
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if Profile.objects.filter(user__email=email).exists():
                raise ValidationError('Email already exists')
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError('Password did not meet the criteria')
        else:
            pattern = ['\d', '[a-zA-Z]', '\W']
            for each in pattern:
                print(re.search(each, password))
                if not re.search(each, password):
                    raise ValidationError('Password did not meet the criteria')
        return password

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if mobile:
            pattern = '[6-9][0-9]{9}'
            if not re.fullmatch(pattern, mobile):
                raise ValidationError('Invalid mobile number')
            if Profile.objects.filter(mobile=mobile).exists():
                raise ValidationError('Mobile number already exists')
        return mobile

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        print(password1, password2)

        if (password1 and password2) and password1 != password2:
            raise ValidationError('Password did not match')
            

class ListForm(forms.ModelForm):
    """ Todo list create and update form. """
    class Meta:
        model = TodoList
        fields = ('title', 'is_pinned')
        widgets = {
            'is_pinned': forms.CheckboxInput()
        }
        help_texts = {
            'title': 'List name must be 3 to 50 character long',
            'is_pinned': 'Set list to homepage as pinned'
        },
        error_messages = {
            'title': {
                'unique': 'List name already exists'
            }
        }
        

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError('Invalid title')
        else:
            if not 2 < len(title) < 50:
                raise ValidationError('Invalid list name')
            # if TodoList.objects.filter()
        return title

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_pinned', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Create list', css_class='w-100')
        )


class TaskForm(forms.ModelForm):
    """ Todo task create and update form. """
    class Meta:
        model = TodoItem
        fields = ('title', 'action')
        help_texts = {
            'title': 'List name must be 3 to 50 character long'
        }
        error_messages = {
            'title': {
                'unique': 'Task name already exists'
            }
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError('Invalid title')
        else:
            if not 2 < len(title) < 50:
                raise ValidationError('Invalid task name')
            # if TodoItem.objects.filter(title=title).exists():
            #     raise ValidationError('Task name already taken')
        return title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('action', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Create task', css_class='w-100')
        )