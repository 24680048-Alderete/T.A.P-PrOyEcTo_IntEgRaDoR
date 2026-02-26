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
<img width="1327" height="416" alt="image" src="https://github.com/user-attachments/assets/8c3f111a-5cbc-4fdc-b5a9-f7afeb64e19e" />

🧠 Explicación del código

El archivo main.py contiene los siguientes bloques principales:

### 1. Importaciones y configuración inicial

```python
import flet as ft
import re

def main(page: ft.Page):
    page.title = "Registro de Estudiantes - Tópicos Avanzados"
    page.bgcolor = "#FDFBE3"  # Fondo crema
    page.padding = 30
    page.theme_mode = ft.ThemeMode.LIGHT
```

- Se importa flet (como ft) y re para expresiones regulares.
- Se configura el título, color de fondo, padding y tema claro.

### 2. Diálogo de resumen (AlertDialog)

```python
    dlg_resumen = ft.AlertDialog(
        title=ft.Text("Información Guardada", weight=ft.FontWeight.BOLD),
        content=ft.Text(""), 
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(e)),
        ],
    )

    def cerrar_dialogo(e):
        dlg_resumen.open = False
        page.update()
```

- Se crea un AlertDialog vacío que se reutilizará para mostrar los datos.
- Se define una función para cerrar el diálogo.

### 3. Funciones de validación

```python
    def validar_nombre(e):
        if not e.control.value:
            e.control.error_text = "El nombre es obligatorio"
        elif len(e.control.value) < 3:
            e.control.error_text = "Mínimo 3 letras"
        else:
            e.control.error_text = None
        e.control.update()

    def validar_control(e):
        if not e.control.value:
            e.control.error_text = "Número de control obligatorio"
        elif len(e.control.value) < 8:
            e.control.error_text = "Deben ser exactamente 8 dígitos"
        else:
            e.control.error_text = None
        e.control.update()

    def validar_email(e):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not e.control.value:
            e.control.error_text = "El email es obligatorio"
        elif not re.match(pattern, e.control.value):
            e.control.error_text = "Formato de email inválido"
        else:
            e.control.error_text = None
        e.control.update()
```

- Cada función valida el contenido del campo correspondiente y establece error_text para mostrar mensajes debajo del campo.
- Se usa on_change para validar en tiempo real mientras el usuario escribe.

### 4. Controles de entrada con filtros

```python
    txt_nombre = ft.TextField(
        label="Nombre", 
        border_color="#4D2A32",
        expand=True,
        input_filter=ft.InputFilter(
            allow=True, 
            regex_string=r"[a-zA-ZáéíóúÁÉÍÓÚñÑ ]", 
            replacement_string=""
        ),
        on_change=validar_nombre
    )
    
    txt_control = ft.TextField(
        label="Número de control", 
        border_color="#4D2A32", 
        expand=True,
        input_filter=ft.InputFilter(
            allow=True, 
            regex_string=r"[0-9]", 
            replacement_string=""
        ),
        max_length=8,
        on_change=validar_control
    )

    txt_email = ft.TextField(
        label="Email", 
        hint_text="ejemplo@gmail.com",
        border_color="#4D2A32", 
        expand=True,
        on_change=validar_email
    )

    dd_carrera = ft.Dropdown(
        label="Carrera",
        expand=True,
        options=[
            ft.dropdown.Option("Ingeniería en Sistemas Computacionales"),
            ft.dropdown.Option("Ingeniería Civil"),
            ft.dropdown.Option("Ingeniería Industrial"),
            ft.dropdown.Option("Ingeniería Mecatrónica"),
            ft.dropdown.Option("Ingeniería en Gestión Empresarial"),
            ft.dropdown.Option("Ingeniería Electronica"),
            ft.dropdown.Option("Contador Público"),
        ]
    )

    dd_semestre = ft.Dropdown(
        label="Semestre",
        expand=True,
        options=[ft.dropdown.Option(str(i)) for i in range(1, 11)]
    )

    rg_genero = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(label="Masculino", value="Masculino"),
            ft.Radio(label="Femenino", value="Femenino"),
        ])
    )
```

- input_filter en txt_nombre permite solo letras (incluyendo acentos y ñ) y espacios.
- input_filter en txt_control permite solo dígitos, y se limita a 8 caracteres con max_length.
- Los Dropdowns se crean con opciones predefinidas.
- RadioGroup para género, organizado en una fila horizontal.

### 5. Función de envío

```python
    txt_mensaje_error = ft.Text("", color="red", weight="bold")

    def enviar_click(e):
        # Validación final antes de abrir ventana
        if not txt_nombre.value or not txt_control.value or not txt_email.value:
            txt_mensaje_error.value = "Error: Nombre, Control y Email son obligatorios."
            page.update()
            return

        if len(txt_control.value) < 8:
            txt_mensaje_error.value = "Error: El número de control debe tener 8 dígitos."
            page.update()
            return

        # Si todo está OK
        txt_mensaje_error.value = ""
        resumen = (
            f"Nombre: {txt_nombre.value}\n"
            f"Control: {txt_control.value}\n"
            f"Email: {txt_email.value}\n"
            f"Carrera: {dd_carrera.value}\n"
            f"Género: {rg_genero.value if rg_genero.value else 'No seleccionado'}"
        )
        
        dlg_resumen.content = ft.Text(resumen, size=16)
        page.dialog = dlg_resumen
        dlg_resumen.open = True
        page.update()
```

- Se comprueba que los campos obligatorios no estén vacíos y que el número de control tenga 8 dígitos.
- Si hay error, se muestra un mensaje en rojo.
- Si todo es correcto, se construye un texto resumen y se asigna al contenido del diálogo, luego se abre.

### 6. Botón de envío

```python
    btn_enviar = ft.ElevatedButton(
        content=ft.Text("Enviar", color="black"),
        bgcolor=ft.Colors.GREY_500,
        width=page.width,
        on_click=enviar_click
    )
```

### 7. Armado de la interfaz

```python
    page.overlay.append(dlg_resumen)

    page.add(
        ft.Column([
            ft.Text("Formulario Estudiantil", size=25, weight="bold", color="#4D2A32"),
            txt_nombre,
            txt_control,
            txt_email,
            ft.Row([dd_carrera, dd_semestre], spacing=10),
            ft.Row([ft.Text("Género:"), rg_genero]),
            txt_mensaje_error,
            btn_enviar
        ], spacing=15)
    )
```

- Se agrega el diálogo al overlay para que pueda mostrarse.
- Se organizan todos los controles en una columna vertical.

### 8. Ejecución

```python
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
```

- Se ejecuta la aplicación en el navegador web.

##✨ Mejoras implementadas respecto al formulario base

- Validación de campos vacíos en todos los campos obligatorios.
- Validación de formato de email mediante expresión regular.
- Filtros de entrada para evitar caracteres no deseados en nombre y número de control.
- Menús desplegables para Carrera y Semestre.
- Botones de opción para Género.
- Ventana modal (AlertDialog) que muestra los datos ingresados al hacer clic en "Enviar".
