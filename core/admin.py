from django.contrib import admin

from .models import TodoList, TodoItem, Profile


@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display    = ('title', 'is_pinned',)
    prepopulated_fields = {'slug': ('title',)}

    def get_full_name(self, obj):
        return obj.user.get_full_name()


@admin.register(TodoItem)
class TodoListAdmin(admin.ModelAdmin):
    list_display    = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display    = ('user',)
    # prepopulated_fields = {'slug': ('title',)}