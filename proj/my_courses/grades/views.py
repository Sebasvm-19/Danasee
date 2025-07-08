from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import status 
from .models import Estudiante
from .models import Profesor
from .models import Materia
from .serializer import *

class ListStudent(generics.ListCreateAPIView):
    queryset = Estudiante.objects.all()
    serializer_class = GradesEstuSelializer
    
class ListProfessor(generics.ListCreateAPIView):
    queryset = Profesor.objects.all()
    serializer_class = GradesProfSelializer

class ListMaterias(generics.ListCreateAPIView):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer

class ListCurso(generics.ListCreateAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class NotasEstudianteAPIView(generics.ListAPIView):
    serializer_class = NotaSerializer
    permission_classes = [IsAuthenticated]        # Confirmación de la autenticación 

    def get_queryset(self):
        user = self.request.user
        if user.permiso == TipoPermisos.BASICO:   # Confirmar que es el estudiante
            return Nota.objects.filter(estudiante__usuario=user)
        return Nota.objects.none()
    
class MateriasDelEstudianteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.permiso == TipoPermisos.BASICO:
            materias = Materia.objects.filter(curso__estudiantes__usuario=user).distinct()
            serializer = MateriaConNotasSerializer(materias, many=True, context={'request': request})
            return Response(serializer.data)
        return Response([])
    
class NotasPorMateriaAPIView(ListAPIView):
    serializer_class = NotaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        materia_id = self.kwargs['materia_id']

        if user.permiso == TipoPermisos.BASICO:
            return Nota.objects.filter(
                materia_id=materia_id,
                estudiante__usuario=user
            )
        return Nota.objects.none()
    
class CursosDelProfesorAPIView(generics.ListAPIView):
    serializer_class = CursoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            profesor = Profesor.objects.get(usuario=user)
            return Curso.objects.filter(profesor=profesor)
        except Profesor.DoesNotExist:
            return Curso.objects.none()

# Materias de los cursos del profesor
class MateriasDelProfesorEnCursoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, curso_id):
        user = request.user
        try:
            profesor = Profesor.objects.get(usuario=user)
            materias = Materia.objects.filter(curso__id=curso_id, profesor=profesor)
            serializer = MateriaSerializer(materias, many=True)
            return Response(serializer.data)
        except Profesor.DoesNotExist:
            return Response({"error": "Profesor no encontrado"}, status=404)


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

class NotasCursoMateriaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, curso_id, materia_id):
        try:
            profesor = Profesor.objects.get(usuario=request.user)

            notas = Nota.objects.filter(
                materia__id=materia_id,
                materia__curso__id=curso_id,
                materia__profesor=profesor
            ).select_related('estudiante')

            serializer = NotaSerializerProf(notas, many=True)
            return Response(serializer.data)
        except Profesor.DoesNotExist:
            return Response({'detail': 'Profesor no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, curso_id, materia_id):
        try:
            profesor = Profesor.objects.get(usuario=request.user)
            nota_id = request.data.get('nota_id')
            nuevo_valor = request.data.get('valor')

            nota = Nota.objects.get(
                id=nota_id,
                materia__id=materia_id,
                materia__curso__id=curso_id,
                materia__profesor=profesor
            )

            nota.valor = nuevo_valor
            nota.save()

            return Response({'success': 'Nota actualizada correctamente'}, status=status.HTTP_200_OK)

        except Nota.DoesNotExist:
            return Response({'detail': 'Nota no encontrada o no autorizada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NotasPorActividadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, curso_id, materia_id, actividad_id):
        try:
            profesor = Profesor.objects.get(usuario=request.user)

            notas = Nota.objects.filter(
                actividad__id=actividad_id,
                materia__id=materia_id,
                materia__curso__id=curso_id,
                materia__profesor=profesor
            ).select_related('estudiante', 'actividad')

            serializer = NotaSerializerProf(notas, many=True)
            return Response(serializer.data)
        except Profesor.DoesNotExist:
            return Response({'detail': 'Profesor no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class CrearActividadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            materia_id = request.data.get("materia_id")
            materia = Materia.objects.get(id=materia_id)

            actividad = Actividad.objects.create(
                nombre=request.data.get("nombre", "Sin nombre"),
                porcentaje=request.data.get("porcentaje", 0),
                comentario=request.data.get("comentario", ""),
                periodo_academico=request.data.get("periodo_academico"),
            )

            # Aquí puedes crear las notas en 0 para los estudiantes del curso si deseas

            return Response({"detail": "Actividad creada", "id": actividad.id}, status=201)

        except Exception as e:
            return Response({"detail": str(e)}, status=500)

class ActividadesPorMateriaAPIView(APIView):
    def get(self, request, materia_id):
        actividades = Actividad.objects.filter(materia_id=materia_id)
        serializer = ActividadSerializer(actividades, many=True)
        return Response(serializer.data)

    def post(self, request, materia_id):
        data = request.data.copy()
        data['materia'] = materia_id  # Asegura que la materia se asigne correctamente
        serializer = ActividadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MateriasProfesorCursoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, curso_id):
        profesor = Profesor.objects.get(usuario=request.user)
        materias = Materia.objects.filter(curso__id=curso_id, profesor=profesor).prefetch_related('actividades')
        serializer = MateriaConActividadesSerializer(materias, many=True)
        return Response(serializer.data)
    
