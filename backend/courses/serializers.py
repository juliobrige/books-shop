# backend/courses/serializers.py

from rest_framework import serializers
from .models import Course, Lesson, Enrollment

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "order", "video_url", "duration"]

class CourseSerializer(serializers.ModelSerializer):
    # Aninha o LessonSerializer para mostrar as aulas de cada curso
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = [
            "id", "title", "slug", "description", 
            "price", "is_published", "owner", "lessons"
        ]

class EnrollmentSerializer(serializers.ModelSerializer):
    # Usa a representação em string do curso para clareza
    course = serializers.StringRelatedField()

    class Meta:
        model = Enrollment
        fields = ["id", "course", "status", "progress", "created_at"]