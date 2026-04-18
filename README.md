# Sistema de Registro de Notas OTEC

Aplicación web para registrar notas de alumnos y calcular promedios.

## Requisitos

- Python 3.8+
- MySQL (base de datos externa en andy.cl)

## Instalación

1. Clona o descarga el repositorio.
2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Configuración

La base de datos ya está configurada en el código con los siguientes datos:
- Host: andy.cl
- Base de datos: curso
- Usuario: curso
- Contraseña: aiep

La tabla `alumnos` debe tener las columnas: `nombre`, `nota1`, `nota2`, `nota3`.

## Ejecución

Ejecuta la aplicación:
```
python app.py
```

Abre tu navegador en `http://localhost:5000`

## Funcionalidades

- Agregar nuevos alumnos con sus notas
- Ver lista de alumnos con sus promedios calculados

## Control de Versiones

Este proyecto utiliza Git para control de versiones.