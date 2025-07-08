from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Estudiante
from .models import Profesor
from .models import Curso
from .models import Nota
from .models import Materia
from .models import Usuario
from .utils import TipoPermisos
from .models import Actividad

class UsuarioSerializer(serializers.ModelSerializer):
    contrasena = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'telefono', 'contrasena']

# Profesores
class CursoSerializer(serializers.ModelSerializer):
    nombre_display = serializers.CharField(source='get_nombre_display', read_only=True) 

    class Meta:
        model = Curso
        fields = ['id', 'nombre', 'nombre_display', 'profesor']

# Estudiantes
class CursoSimpleSerializer(serializers.ModelSerializer):
    nombre_display = serializers.CharField(source='get_nombre_display', read_only=True)

    class Meta:
        model = Curso
        fields = ['id', 'nombre', 'nombre_display']

class MateriaSerializer(serializers.ModelSerializer):
    nombre_display = serializers.CharField(source='get_nombre_display', read_only=True)

    class Meta:
        model = Materia
        fields = ['id', 'nombre', 'nombre_display', 'descripcion', 'tematica', 'curso']

class GradesEstuSelializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    grado = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all())

    class Meta:
        model = Estudiante
        fields = ['usuario', 'grado', 'direccion']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        grado = validated_data.pop('grado')

        contrasena = usuario_data.pop('contrasena', None)

        usuario = Usuario(**usuario_data)
        usuario.permiso = TipoPermisos.BASICO

        if contrasena:
            usuario.set_password(contrasena)
        else:
            raise serializers.ValidationError("Se requiere una contraseña.")

        usuario.save()

        estudiante = Estudiante.objects.create(usuario=usuario, grado=grado)
        estudiante.cursos.add(grado)
        return estudiante

class NotaSerializer(serializers.ModelSerializer):
    materia_nombre      = serializers.CharField(source='materia.nombre', read_only=True)
    materia_descripcion = serializers.CharField(source='materia.descripcion', read_only=True)
    materia_tematica    = serializers.CharField(source='materia.tematica', read_only=True)
    materia_grado       = serializers.CharField(source='materia.curso.get_nombre_display', read_only=True)

    comentario          = serializers.CharField(source='actividad.comentario', read_only=True)
    periodo_academico   = serializers.IntegerField(source='actividad.periodo_academico', read_only=True)
    porcentaje          = serializers.FloatField(source='actividad.porcentaje', read_only=True)

    class Meta:
        model = Nota
        fields = [
            'nombre', 'fecha', 'valor', 'comentario', 'periodo_academico', 'porcentaje',
            'materia_nombre', 'materia_descripcion', 'materia_tematica', 'materia_grado',
        ]

class NotaSerializerProf(serializers.ModelSerializer):
    estudiante_nombre = serializers.SerializerMethodField()
    comentario = serializers.CharField(source='actividad.comentario')
    periodo_academico = serializers.IntegerField(source='actividad.periodo_academico', read_only=True)

    class Meta:
        model = Nota
        fields = ['id', 'nombre', 'estudiante_nombre', 'fecha', 'valor', 'comentario', 'periodo_academico']

    def get_estudiante_nombre(self, obj):
        return f'{obj.estudiante.usuario.nombre} {obj.estudiante.usuario.apellido}'

    def update(self, instance, validated_data):
        actividad_data = validated_data.pop('actividad', {})
        
        # Actualizar el campo valor de la nota
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Actualizar el comentario en la actividad si se proporcionó
        if 'comentario' in actividad_data:
            actividad = instance.actividad
            actividad.comentario = actividad_data['comentario']
            actividad.save()

        return instance

class GradesProfSelializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta: 
        model = Profesor
        fields = ['usuario']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')

        especialidad = validated_data.pop('especialidad')

        contrasena = usuario_data.pop('contrasena', None)
        
        usuario = Usuario(**usuario_data)
        usuario.permiso = TipoPermisos.INTERMEDIO

        if contrasena:
            usuario.set_password(contrasena)
        else:
            raise serializers.ValidationError("Se requiere una contraseña.")
        
        usuario.save()
        
        profesor = Profesor.objects.create(usuario=usuario, especialidad=especialidad)
        return profesor

class NotaActividadSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Nota
        fields = ['id', 'estudiante', 'estudiante_nombre', 'valor', 'fecha']

    def get_estudiante_nombre(self, obj):
        return f"{obj.estudiante.usuario.nombre} {obj.estudiante.usuario.apellido}"

class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ['id', 'nombre', 'porcentaje', 'comentario', 'periodo_academico', 'materia']

class MateriaConActividadesSerializer(serializers.ModelSerializer):
    actividades = ActividadSerializer(many=True, read_only=True)

    class Meta:
        model = Materia
        fields = ['id', 'nombre', 'descripcion', 'tematica', 'actividades']

class ActividadNotasSerializer(serializers.ModelSerializer):
    notas = NotaActividadSerializer(many=True)

    class Meta:
        model = Actividad
        fields = ['id', 'nombre', 'comentario', 'periodo_academico', 'porcentaje', 'notas']

class MateriaConNotasSerializer(serializers.ModelSerializer):
    notas = serializers.SerializerMethodField()
    nombre_display = serializers.CharField(source='get_nombre_display', read_only=True)

    class Meta:
        model = Materia
        fields = ['id', 'nombre', 'nombre_display', 'descripcion', 'tematica', 'notas']

    def get_notas(self, materia):
        user = self.context['request'].user
        return NotaSerializer(
            materia.nota_set.filter(estudiante__usuario=user), many=True
        ).data


# Permisos para el front (profesor, estudiante)
class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Añadir permiso y otros datos útiles al token
        token['permiso'] = user.permiso
        token['nombre'] = user.nombre
        token['apellido'] = user.apellido
        return token
    
