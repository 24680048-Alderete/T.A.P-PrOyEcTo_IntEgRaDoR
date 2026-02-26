# T.A.P-PrOyEcTo_IntEgRaDoR
Este repositorio contiene el proyecto correspondiente a la **Unidad 1** de la asignatura de Graficación. Se desarrolla un escenario 3D generado proceduralmente en Blender mediante scripting en Python, que consiste en un camino de bloques con una curva sinusoidal y una cámara que recorre dicho camino de principio a fin con animación por keyframes.

El objetivo es demostrar el uso de:
- Generación procedural de geometría.
- Creación y asignación de materiales.
- Animación programática de objetos (cámara).
- Iluminación y ambientación básica.

## 🚀 Instrucciones de uso

1. **Clona o descarga** este repositorio en tu computadora.
2. **Abre Blender**. Puedes iniciar con un archivo nuevo o con la escena por defecto (el script la limpiará automáticamente).
3. **Ve al espacio de trabajo "Scripting"** (menú superior, selecciona "Scripting").
4. **Abre el script** `escenario_procedural.py` desde el editor de texto de Blender (Archivo > Abrir o arrastra el archivo).
5. **Ejecuta el script** haciendo clic en el botón "Run Script" (triángulo hacia la derecha) o presionando `Alt + P`.
6. **Observa el resultado**:
   - Cambia al espacio de trabajo "Layout" o "3D Viewport".
   - Verás el camino de bloques generado con dos colores (gris oscuro y azul neón).
   - En la línea de tiempo (parte inferior) se han creado automáticamente 1800 frames (30 fps * 60 segundos).
   - Desliza el cabezal de tiempo para ver el movimiento de la cámara a lo largo del camino.
   - También puedes reproducir la animación con los controles de la línea de tiempo.
7. **Renderiza la animación** (opcional):
   - Configura la resolución y formato de salida en las propiedades de renderizado.
   - Ve a `Render` > `Render Animation` (o presiona `Ctrl + F12`).

## 📝 Explicación detallada del código

A continuación se desglosa el script paso a paso, con explicaciones de cada bloque.
### 1. Importación de módulos y limpieza de escena

```python
import bpy
import math
```
- `bpy`: Es el módulo principal de Python en Blender. Permite acceder y manipular todos los objetos, escenas, materiales, etc.
- `math`: Proporciona funciones matemáticas como `sin`, que usaremos para generar la curva.
```Python
# 1. Limpieza absoluta
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
```
- `bpy.ops.object.select_all(action='SELECT')`: Selecciona todos los objetos presentes en la escena actual.
- `bpy.ops.object.delete()`: Elimina los objetos seleccionados. De esta forma garantizamos que empezamos con una escena completamente vacía.
### 2. Creación de materiales
Definimos una función auxiliar para crear materiales de forma rápida:
```Python
def crear_material(nombre, r, g, b):
    mat = bpy.data.materials.new(name=nombre)
    mat.diffuse_color = (r, g, b, 1.0)  # Color RGB con canal alpha = 1.0 (opaco)
    return mat
```
Luego creamos dos materiales:
```Python
mat_base = crear_material("GrisOscuro", 0.1, 0.1, 0.1)   # Gris muy oscuro
mat_acento = crear_material("Neon", 0.0, 0.8, 1.0)       # Azul cian (neón)
```
- mat_base se usará en la mayoría de los bloques.
- mat_acento se asignará a algunos bloques para dar un contraste visual.
### 3. Parámetros configurables
```Python
largo = 120               # Número de bloques (pares de columnas)
punto_curva = 10           # A partir de qué bloque comienza la curvatura
amplitud = 6               # Amplitud de la onda sinusoidal
suavizado = 15             # Suavizado de la entrada a la curva
fps = 60                   # Fotogramas por segundo
duracion_seg = 30          # Duración del recorrido en segundos
total_frames = fps * duracion_seg   # Fotogramas totales (1800)
```
Estos parámetros controlan la geometría y la animación. Modificándolos se pueden obtener diferentes comportamientos.
- `largo`: Cantidad de "filas" de bloques. Cada fila tiene dos bloques (izquierdo y derecho).
- `punto_curva`: Índice del bloque donde empieza la ondulación. Si es `0`, la curva empieza desde el primer bloque.
- `amplitud`: Magnitud del desplazamiento lateral máximo.
- `suavizado`: Número de bloques durante los cuales la amplitud crece desde 0 hasta su valor máximo (transición suave).
- `fps` y `duracion_seg`: Determinan la duración total de la animación y la cantidad de keyframes que se generarán.
### 4. Generación de los bloques
Iteramos desde `i = 0` hasta `largo - 1`:
```Python
for i in range(largo):
    n = max(0, i - punto_curva)               # Desplazamiento desde el inicio de la curva
    entrada_suave = min(1.0, n / suavizado)   # Factor de suavizado (0 a 1)
    offset_curva = math.sin(n * 0.3) * amplitud * entrada_suave  # Desplazamiento en X
    pos_y = i * 2                              # Posición en el eje Y
```
- `n`: Representa cuántos bloques han pasado desde `punto_curva`. Si `i < punto_curva`, `n` es 0 (sin curva).
- `entrada_suave`: Controla la progresión de la curva. Durante los primeros suavizado bloques después de `punto_curva`, este valor aumenta linealmente de `0 a 1`, evitando un cambio brusco.
- `offset_curva`: Es el desplazamiento lateral que sufrirán ambos bloques. Usamos `sin(n * 0.3)` para generar una onda suave; amplitud escala la onda; `entrada_suave` aplica la transición gradual.
- `pos_y`: Cada bloque se coloca separado 2 unidades en Y, creando una hilera.
#### Bloque Izquierdo
```Python
    # Bloque Izquierdo
    bpy.ops.mesh.primitive_cube_add(location=(-3 + offset_curva, pos_y, 1))
    obj = bpy.context.active_object
    obj.data.materials.append(mat_base if i % 2 == 0 else mat_acento)
    if i % 2 != 0:
        obj.scale.z = 1.5
```
- Se añade un cubo en la posición `(-3 + offset_curva, pos_y, 1)`. La coordenada X base es -3 (separación inicial), luego se suma el offset de la curva.
- El objeto recién creado se asigna a la variable `obj`.
- Se le asigna un material: si `i` es par, se usa `mat_base`; si es impar, `mat_acento`. Esto crea un patrón de colores alternados.
- Además, si `i` es impar, se escala el cubo en Z a 1.5 (más alto), dando variedad visual.
#### Bloque Derecho
```Python
    # Bloque Derecho
    bpy.ops.mesh.primitive_cube_add(location=(3 + offset_curva, pos_y, 1))
    bpy.context.active_object.data.materials.append(mat_base)
```
- Simétrico al izquierdo, pero con posición X base = 3.
- Siempre se le asigna  `mat_base` (gris oscuro) para mantener el contraste con los bloques izquierdos acentuados.
### 5. Configuración de la cámara
```Python
bpy.ops.object.camera_add()
camara = bpy.context.active_object
camara.rotation_euler = (math.radians(85), 0, 0)  # Inclinada ligeramente hacia el frente
```
- Se añade una nueva cámara a la escena.
- Se rota 85 grados en el eje X (usando `math.radians` para convertir a radianes). Esto hace que la cámara apunte ligeramente hacia abajo, simulando una vista de "paseo".
### 6. Animación de la cámara mediante keyframes
Primero establecemos el rango de la animación:
```Python
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = total_frames
```
Luego, para cada frame desde 1 hasta `total_frames`:
```Python
for f in range(1, total_frames + 1):
    # Calculamos la posición equivalente a lo largo del camino (en índice de bloque)
    i_anim = (f / total_frames) * (largo - 1)
```
- `i_anim` es un número real que representa la posición "virtual" de la cámara a lo largo de los bloques. Al inicio del recorrido `(f=1)` vale 0, y al final `(f=total_frames)` vale `largo-1`.
Aplicamos la misma lógica de curva que a los bloques:
```python
    n_anim = max(0, i_anim - punto_curva)
    entrada_anim = min(1.0, n_anim / suavizado)
    offset_anim = math.sin(n_anim * 0.3) * amplitud * entrada_anim
````
- Así la cámara sigue exactamente la misma trayectoria sinusoidal que los bloques.

Actualizamos la posición de la cámara:

```python
    camara.location.x = offset_anim
    camara.location.y = i_anim * 2
    camara.location.z = 1.8   # Altura aproximada de los ojos
```
- x: Se desplaza lateralmente según la curva.
- y: Avanza linealmente (cada bloque son 2 unidades).
- z: Se fija en 1.8 para dar una sensación de altura humana.

Finalmente insertamos un keyframe para la propiedad `location` en el frame actual:

```python
    camara.keyframe_insert(data_path="location", frame=f)
```
Esto guarda la posición en ese frame, creando la animación.

## 7. Suelo y luces
### Suelo
```python
bpy.ops.mesh.primitive_plane_add(location=(0, largo, 0))
bpy.context.active_object.scale = (20, largo + 10, 1)
```
- Se añade un plano en el centro del eje X, al final del camino en Y (aproximadamente), y en Z=0.
- Se escala para que cubra un ancho de 20 unidades y una profundidad de `largo+10` (suficiente para abarcar todo el recorrido y un poco más).
### Luz principal
```python
bpy.ops.object.light_add(type='POINT', location=(0, 10, 15))
luz = bpy.context.active_object
luz.data.energy = 10000
```
- Se agrega una luz puntual en `(0, 10, 15)` (centrada, cerca del inicio, elevada).
- Se establece su energía en 10000 para iluminar intensamente.
### Luz secundaria (final del camino)
```python
bpy.ops.object.light_add(type='POINT', location=(0, largo*2, 10))
bpy.context.active_object.data.energy = 5000
```
- Otra luz puntual al final del pasillo para evitar que la parte más alejada quede oscura.
- Menos energía que la principal (5000).
## 8. Regreso al frame inicial
```python
bpy.context.scene.frame_set(1)
```
- Coloca el cabezal de tiempo en el primer frame, listo para visualizar la animación desde el inicio.
