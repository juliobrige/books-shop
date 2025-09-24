from django.conf import settings
from django.db import models
from django.utils.text import slugify

class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: abstract = True

class Course(TimeStamped):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    is_published = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="owned_courses")

    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    def __str__(self): return self.title

class Lesson(TimeStamped):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    video_url = models.URLField(help_text="Link do YouTube (watch ou embed)")
    duration = models.CharField(max_length=20, blank=True)
    class Meta: ordering = ["order","id"]
    def __str__(self): return f"{self.course.title} - {self.title}"

class Enrollment(TimeStamped):
    STATUS = [("PENDING","Pendente"),("ACTIVE","Ativa"),("CANCELED","Cancelada")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    status = models.CharField(max_length=10, choices=STATUS, default="ACTIVE")
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    class Meta: unique_together = ("user","course")
    def __str__(self): return f"{self.user} → {self.course} ({self.status})"
