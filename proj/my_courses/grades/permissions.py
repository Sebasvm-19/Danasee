from rest_framework.permissions import BasePermission
from .utils import TipoPermisos

class EsAvanzado(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.permiso == TipoPermisos.AVANZADO

class EsIntermedio(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.permiso == TipoPermisos.INTERMEDIO

class EsBasico(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.permiso == TipoPermisos.BASICO

class PuedeEditarNotas(BasePermission):
    """
    Permite editar notas solo a usuarios con permiso INTERMEDIO o AVANZADO.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.permiso in [
            TipoPermisos.INTERMEDIO
        ]
