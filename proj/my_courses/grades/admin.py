from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .models import Usuario
from .models import Estudiante
from .models import Profesor
from .models import Materia
from .models import Pedido
from .models import Almuerzo
from .models import Nota
from .models import Actividad


admin.site.register(Estudiante)
admin.site.register(Profesor)
admin.site.register(Materia)
admin.site.register(Pedido)
admin.site.register(Almuerzo)
admin.site.register(Nota)
admin.site.register(Actividad) 

try:
    admin.site.unregister(Usuario)
except admin.sites.NotRegistered:
    pass


class UsuarioAdmin(BaseUserAdmin):
    model = Usuario
    list_display = ['correo', 'nombre', 'apellido', 'permiso', 'is_staff']
    ordering = ['correo']

    fieldsets = (
        (None, {'fields': ('correo', 'password')}),
        ('Información personal', {'fields': ('nombre', 'apellido', 'telefono', 'fecha_registro')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'permiso')}),
    )

    readonly_fields = ['permiso']  # ✅ El campo 'permiso' será de solo lectura

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo', 'nombre', 'apellido', 'telefono', 'fecha_registro', 'password1', 'password2'),
        }),
    )

admin.site.register(Usuario, UsuarioAdmin)