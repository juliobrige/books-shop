# backend/courses/admin.py

from django.contrib import admin
from .models import Course, Lesson, Enrollment

# Regista os modelos para que apareçam na área de admin
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Enrollment)