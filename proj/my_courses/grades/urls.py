from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path('api/estudiante/', views.ListStudent.as_view()),
    path('api/profesor/', views.ListProfessor.as_view()),
    path('api/materia/', views.ListMaterias.as_view()),
    path('api/curso/', views.ListCurso.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/materiasEstudiante/', views.MateriasDelEstudianteAPIView.as_view()),
    path('api/notasMateria/<int:materia_id>/', views.NotasPorMateriaAPIView.as_view()),
    path('api/token/', views.CustomTokenView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profesorCursos/', views.CursosDelProfesorAPIView.as_view()),
    path('api/materiasProfesorCurso/<int:curso_id>/', views.MateriasDelProfesorEnCursoAPIView.as_view()),
    path(
        'api/profesor/curso/<int:curso_id>/materia/<int:materia_id>/notas/',
        views.NotasCursoMateriaAPIView.as_view(), 
        name='notas-curso-materia'
    ),
    path('api/actividad/<int:actividad_id>/notas/', views.NotasPorActividadAPIView.as_view(), name='actividad-notas'),
    path('api/actividad/', views.CrearActividadAPIView.as_view()),
    path('api/materias/<int:materia_id>/actividades/', views.ActividadesPorMateriaAPIView.as_view()),
    path('api/profesor/curso/<int:curso_id>/materia/<int:materia_id>/actividad/<int:actividad_id>/notas/', views.NotasPorActividadAPIView.as_view()),


]
