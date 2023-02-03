from django.contrib import admin
from .models import Todo

class ToDoAdmon(admin.ModelAdmin):
    readonly_fields = ('date_time',)

admin.site.register(Todo, ToDoAdmon)