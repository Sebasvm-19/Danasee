from enum import IntEnum

class TipoPermisos(IntEnum):
  BASICO = 1
  INTERMEDIO = 2
  AVANZADO = 3
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]
  
class TiposEstados(IntEnum):
  PENDIENTE = 1
  SERVIDO = 2
  CANCELADO = 3
      
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]
    
class TipoMenu(IntEnum):
  CORRIENTE = 1
  EJECUTIVO = 2
      
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]
  
class Grados(IntEnum):
  PRIMERO = 1
  SEGUNDO = 2
  TERCERO = 3
  CUARTO = 4
  QUINTO = 5
  SEXTO = 6
  SEPTIMO = 7
  OCTAVO = 8 
  NOVENO = 9
  DECIMO = 10
  ONCE = 11
      
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]