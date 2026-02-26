# T.A.P-PrOyEcTo_IntEgRaDoR
Este proyecto consiste en una aplicación de escritorio/web desarrollada con Flet (Python) que implementa un formulario de registro de estudiantes, basado en la imagen adjunta, e incorpora validaciones de entrada y una ventana modal para mostrar los datos ingresados.

### 📋 Características
- **Campos del formulario:**
  - Nombre (solo letras y espacios, mínimo 3 caracteres)
  - Número de control (solo dígitos, exactamente 8)
  - Email (validación de formato con expresión regular)
  - Carrera (menú desplegable con opciones predefinidas)
  - Semestre (menú desplegable del 1 al 10)
  - Género (botones de opción: Masculino / Femenino)
- **Validaciones en tiempo real:**
  - Los campos muestran mensajes de error si no cumplen los requisitos.
  - Filtros de entrada que evitan caracteres no permitidos (letras en nombre, números en control).
- **Botón Enviar:**
  - Realiza una validación final de campos obligatorios.
  - Si todo es correcto, abre una ventana modal (`AlertDialog`) con un resumen de los datos ingresados.
- **Interfaz limpia y responsiva**, con colores suaves.

### 🖼️ Captura de pantalla