from django.contrib import admin
from django.contrib.auth.models import User
from dashboard_app.models import Comment, Task, Board

# Register your models here.
admin.site.register(Comment)
admin.site.register(Task)
admin.site.register(Board)
