# backend/courses/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Enrollment
from .serializers import CourseSerializer, LessonSerializer, EnrollmentSerializer

# --------------------------------------------------------------------------
# A classe CourseViewSet começa aqui, com a indentação correta
# --------------------------------------------------------------------------
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    tags = ['Cursos']
    queryset = Course.objects.filter(is_published=True).prefetch_related("lessons").order_by("-created_at")
    serializer_class = CourseSerializer
    # Qualquer pessoa pode ver a lista de cursos
    permission_classes = [permissions.AllowAny]
    # --- Ações personalizadas para a CourseViewSet ---

    @action(detail=True, methods=["post"], url_path="enroll", permission_classes=[permissions.IsAuthenticated])
    def enroll(self, request, pk=None):
        """
        Matricula o utilizador autenticado no curso.
        """
        course = self.get_object()
        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user, course=course, defaults={"status": "ACTIVE"}
        )

        if not created and enrollment.status == "ACTIVE":
            return Response({"detail": "Você já está matriculado neste curso."}, status=status.HTTP_400_BAD_REQUEST)
            enrollment.status = "ACTIVE"
        enrollment.save()
        return Response({"detail": f"Matrícula confirmada em {course.title}."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], url_path="lessons", permission_classes=[permissions.IsAuthenticated])
    def lessons_for_me(self, request, pk=None):
        """
        Retorna as aulas de um curso, apenas para utilizadores matriculados.
        """
        course = self.get_object()
        if not Enrollment.objects.filter(user=request.user, course=course, status="ACTIVE").exists():
            return Response({"detail": "Acesso negado. Você não está matriculado neste curso."}, status=status.HTTP_403_FORBIDDEN)
        
        data = LessonSerializer(course.lessons.all(), many=True).data
        return Response(data)

class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    tags = ['Cursos']

    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Esta view deve retornar uma lista de todas as matrículas
        para o utilizador atualmente autenticado.
        """
        return (Enrollment.objects
                .filter(user=self.request.user)
                .select_related("course")
                .prefetch_related("course__lessons"))

    @action(detail=True, methods=["post"], url_path="progress", permission_classes=[permissions.IsAuthenticated])
    def update_progress(self, request, pk=None):
        """
        Atualiza o progresso de um utilizador numa matrícula específica.
        """
        enrollment = get_object_or_404(self.get_queryset(), pk=pk)
        try:
            progress = float(request.data.get("progress", 0))
        except (TypeError, ValueError):
            return Response({"detail": "Valor de 'progress' inválido."}, status=status.HTTP_400_BAD_REQUEST)

        if not (0 <= progress <= 100):
            return Response({"detail": "O progresso deve estar entre 0 e 100."}, status=status.HTTP_400_BAD_REQUEST)
        
        enrollment.progress = progress
        enrollment.save()
        return Response({"detail": "Progresso atualizado.", "progress": progress})