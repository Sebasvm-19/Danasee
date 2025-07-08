from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from .utils import *
from django.utils.timezone import now

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, contrasena=None, **extra_fields):
        if not correo:
            raise ValueError('El correo es obligatorio')

        correo = self.normalize_email(correo)

        # Asignar permiso automáticamente si no fue dado
        if 'permiso' not in extra_fields or extra_fields['permiso'] is None:
            if extra_fields.get('es_estudiante'):
                extra_fields['permiso'] = TipoPermisos.BASICO
            elif extra_fields.get('es_profesor'):
                extra_fields['permiso'] = TipoPermisos.INTERMEDIO
            else:
                raise ValueError("Debe indicar si es estudiante o profesor para asignar permiso.")
        user = self.model(correo=correo, **extra_fields)
        user.set_password(contrasena)
        user.save(using=self._db)
        return user 

    def create_superuser(self, correo, contrasena=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if 'permiso' not in extra_fields or extra_fields['permiso'] is None:
            extra_fields['permiso'] = TipoPermisos.AVANZADO
        return self.create_user(correo, contrasena, **extra_fields)
    
class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)
    telefono = PhoneNumberField()
    fecha_registro = models.DateField(default=now)
    permiso = models.IntegerField(choices=TipoPermisos.choices())
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    objects = UsuarioManager()

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

# Herencia profesor
class Profesor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    especialidad = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f'{self.usuario.nombre} {self.usuario.apellido} - {self.especialidad}'

class Curso(models.Model):
    nombre =  models.IntegerField(choices=Grados.choices())
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_nombre_display()}'

# Herencia estudiante
class Estudiante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    grado = models.ForeignKey(Curso, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=100)
    cursos =  models.ManyToManyField(Curso, related_name='estudiantes')

    def __str__(self):
        return f'{self.usuario.nombre} {self.usuario.apellido}'

class Almuerzo(models.Model):
    menu = models.IntegerField(choices=TipoMenu.choices(), null=True)

class Pedido(models.Model):
    fecha = models.DateField()
    estados = models.IntegerField(choices=TiposEstados.choices())
    almuerzo = models.OneToOneField(Almuerzo, on_delete=models.RESTRICT)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Materia(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    tematica = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre

class Actividad(models.Model):
    nombre = models.CharField(max_length=200, default='Sin nombre')
    porcentaje = models.FloatField(default=0)
    comentario = models.CharField(max_length=100, default='Pendiente')
    periodo_academico = models.IntegerField()
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='actividades', null=True)

    def __str__(self):
        return self.nombre
    
class Nota(models.Model):
    nombre = models.CharField(max_length=200,  default='Sin nombre')
    actividad = models.ForeignKey(
        Actividad, on_delete=models.CASCADE, related_name='notas', null=True
    )
    fecha = models.DateField()
    valor = models.IntegerField(default=0)    
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, null=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('actividad', 'estudiante')

    def __str__(self):
        return f'{self.estudiante} - {self.actividad}: {self.valor}'

class RegisAsistencia(models.Model):
    fechaEntrada = models.DateField()
    fechaSalida = models.DateField()
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, null=True)










