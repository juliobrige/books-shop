from rest_framework import serializers
from .models import Course, Lesson, Enrollment

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id","title","order","video_url","duration"]

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ["id","title","slug","description","price","is_published","lessons"]

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    class Meta:
        model = Enrollment
        fields = ["id","course","status","progress","created_at"]
