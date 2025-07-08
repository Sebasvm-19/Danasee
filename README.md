# Danasee
Proyecto Danasee [Sena]

## Para el proyecto se utilizaron las siguientes herramientas que se deben instalar:
- BD: Postgress DB
- HTML
- Bootstrap
- React [Front]
- Django [Back y conexión con la BD]

## Instalación 
### Postgres DB
Se configuró en el puerto 5000 con los siguientes requerimientos al momento de su instalación:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5000'
    }
}

### Django 
```python 
python -m pip install Django
```
Para ejecutar el programa se debe estar en la ruta de my_courses

```python
python manage.py createsuperuser
Credenciales:
- usuario: sebas@example.com
- contraseña: Control1234

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Una vez que se ejecute sin errores, la ruta del administrador es la siguiente:
http://127.0.0.1:8000/admin/

En esta se colocan las creenciales y se accede a todo el modelo realizado. 

### React

```python
npm install # Instala los módulos requeridos para la ejecución referenciando el .json
npm start # inicializa la aplicación 
```

