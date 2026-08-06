# 4x4: B2 English Game - Deployment Guide

## Configuración de la Base de Datos en Render

### 1. Crear una Base de Datos PostgreSQL en Render

1. Ve a [Render Dashboard](https://dashboard.render.com/)
2. Haz clic en **"New +"** y selecciona **"PostgreSQL"**
3. Configura tu base de datos:
   - **Name**: `english-game-db` (o el nombre que prefieras)
   - **Database**: `english_game`
   - **User**: Se genera automáticamente
   - **Region**: Elige la más cercana
   - **PostgreSQL Version**: 15 o superior
   - **Plan**: Free
4. Haz clic en **"Create Database"**
5. Espera a que se cree (tarda unos minutos)
6. Una vez creada, copia la **Internal Database URL** (la necesitarás después)

### 2. Inicializar la Base de Datos

Desde tu terminal local o usando el Shell de Render:

```bash
# Conectarte a la base de datos
psql <TU_INTERNAL_DATABASE_URL>

# Copiar y pegar el contenido del archivo database_schema.sql
# O ejecutar:
\i database_schema.sql
```

### 3. Configurar el Web Service en Render

1. En Render Dashboard, haz clic en **"New +"** y selecciona **"Web Service"**
2. Conecta tu repositorio de GitHub
3. Configura el servicio:
   - **Name**: `english-game`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

### 4. Añadir Variables de Entorno

En la configuración del Web Service, ve a **"Environment"** y añade:

- **Key**: `DATABASE_URL`
- **Value**: Tu Internal Database URL de PostgreSQL (la que copiaste antes)

### 5. Estructura de Archivos en tu Repositorio

```
tu-repo/
├── app.py
├── database.py
├── generate_connection.py
├── read_connection.py
├── requirements.txt
├── templates/
│   └── index.html
└── README.md
```

### 6. Generar el Primer Juego

Después del despliegue, necesitas generar el primer juego. Puedes hacerlo de dos formas:

**Opción A: Desde el Shell de Render**
1. Ve a tu Web Service en Render
2. Haz clic en **"Shell"**
3. Ejecuta: `python generate_connection.py`

**Opción B: Añadir un endpoint en app.py**
Añade esta ruta a `app.py`:

```python
@app.route("/generate")
def generate_game():
    import generate_connection
    generate_connection.main()
    return "Game generated! Go to <a href='/'>home</a>"
```

Luego visita `https://tu-app.onrender.com/generate` para generar un juego.

## Añadir Más Categorías

Para añadir nuevas categorías, conecta a tu base de datos y ejecuta:

```sql
INSERT INTO categories (difficulty, title, words) VALUES
('D', 'nombre de la categoría', 'PALABRA1,PALABRA2,PALABRA3,PALABRA4,PALABRA5,PALABRA6,PALABRA7');
```

**Nota sobre dificultad:**
- `D` = Difficult (1 categoría por juego)
- `O` = Otras/Other (3 categorías por juego)

## Verificar el Estado

Puedes verificar el estado de tu base de datos:

```sql
-- Ver todas las categorías disponibles
SELECT * FROM categories;

-- Ver categorías usadas
SELECT * FROM used_categories;

-- Ver el juego actual
SELECT * FROM current_game;

-- Resetear categorías usadas (para reutilizar todas)
DELETE FROM used_categories;
```

## Solución de Problemas

### Error: "no module named psycopg2"
- Asegúrate de que `requirements.txt` incluye `psycopg2-binary`

### Error: "relation does not exist"
- Ejecuta el schema SQL en tu base de datos PostgreSQL

### El juego no carga
1. Verifica que `DATABASE_URL` está configurada correctamente
2. Genera un juego ejecutando `python generate_connection.py`
3. Verifica los logs en Render Dashboard

### No hay categorías disponibles
- Inserta más categorías en la tabla `categories`
- O ejecuta `DELETE FROM used_categories;` para resetear

## Mantenimiento

- Las categorías usadas se acumulan en `used_categories`
- Cuando se agotan todas las categorías, el sistema las resetea automáticamente
- Puedes resetear manualmente ejecutando: `DELETE FROM used_categories;`