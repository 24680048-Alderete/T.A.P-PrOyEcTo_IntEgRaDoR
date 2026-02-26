import flet as ft

def main(page: ft.Page):
    # Configuración de página para entorno Web/Pyodide
    page.title = "Registro de Estudiantes - Tópicos Avanzados"
    page.bgcolor = "#FDFBE3"  # Fondo crema de la imagen
    page.padding = 30
    page.theme_mode = ft.ThemeMode.LIGHT
    dlg_confirmacion = ft.AlertDialog(
        title=ft.Text("Confirmar Registro"),
        content=ft.Text(""), # Aquí inyectaremos los datos
        actions=[
            ft.TextButton("Corregir", on_click=lambda e: page.close(dlg_confirmacion)),
            ft.TextButton("Confirmar", on_click=lambda e: print("¡Datos Guardados!")),
        ],
    )

    # --- CONTROLES DE ENTRADA (Subtema 1.4) ---
    txt_nombre = ft.TextField(label="Nombre", border_color="#4D2A32",expand=True,input_filter=ft.InputFilter(allow=True, regex_string=r"[a-zA-ZáéíóúÁÉÍÓÚñÑ ]", replacement_string=""),
    on_change=lambda e: validar_nombre(e)
    )
    def validar_nombre(e):
    # Si el campo está vacío, mandamos error
        if e.control.value == "":
            e.control.error_text = None
        elif len(e.control.value)<3:
            e.control.error_text = None
        e.control.update()
    txt_control = ft.TextField(label="Numero de control", border_color="#4D2A32", expand=True,input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""),max_length=8,on_change=lambda e: validar_control(e))
    def validar_control(e):
        if len(e.control.value) == "":
            e.control.error_text = None
        elif 0 < len(e.control.value) < 8:
            e.control.error_text = "Mínimo 8 dígitos"
        else:
            e.control.error_text = None
        e.control.update()
    txt_email = ft.TextField(label="Email", border_color="#4D2A32", expand=True)
    def validar_email(e):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if e.control.value == "":
            e.control.error_text = None
        elif not re.match(pattern, e.control.value):
            e.control.error_text = "Formato de email inválido"
        else:
            e.control.error_text = None
        e.control.update()
    dd_carrera = ft.Dropdown(
        label="Carrera",
        expand=True,
        border_color="#4D2A32",
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
        border_color="#4D2A32",
        options=[ft.dropdown.Option(str(i)) for i in range(1, 7)]
    )
    
    # Campos que se integrarán como Dropdowns posteriormente
    txt_carrera = ft.TextField(label="Carrera", expand=True, border_color="#4D2A32")
    txt_semestre = ft.TextField(label="Semestre", expand=True, border_color="#4D2A32")

    # Contenedor para Genero (Se integrará Radio posteriormente)
    # Por ahora mantenemos la estructura visual con Texto
    row_genero = ft.Row([
        ft.Text("Genero:", color="#4D2A32", weight=ft.FontWeight.BOLD),
        ft.RadioGroup(
            content=ft.Row([
                ft.Radio(label="Masculino", value="Masculino"),
                ft.Radio(label="Femenino", value="Femenino"),
                ft.Radio(label="Otro", value="Otro"),
            ])
        )
    ], alignment=ft.MainAxisAlignment.START)

    # Botón Enviar adaptado a versión 0.80.6.dev (usando content)
    # --- FUNCIÓN DEL BOTÓN ENVIAR ---
    def enviar_click(e):
        resumen = (
            f"Nombre: {txt_nombre.value}\n"
            f"Control: {txt_control.value}\n"
            f"Email: {txt_email.value}\n"
            f"Carrera: {dd_carrera.value}\n"
            f"Semestre: {dd_semestre.value}\n"
            f"Género: {row_genero.value}" # Ahora sí podemos leerlo
        )
        dlg_confirmacion.content = ft.Text(resumen)
        page.open(dlg_confirmacion)
        page.update()
    btn_enviar = ft.ElevatedButton(
        content=ft.Text("Enviar", color="black", size=16),
        bgcolor=ft.Colors.GREY_500,
        width=page.width, # Ocupa el ancho disponible
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0),
        )
    
    )

    # --- CONSTRUCCIÓN DE LA INTERFAZ (Subtema 1.1) ---
    page.add(
        ft.Column([
            ft.Text("Formulario Estudiantil", size=25, weight="bold",color="#AD2A32"),
            txt_nombre,
            txt_control,
            txt_email,
            # Fila para Carrera y Semestre
            ft.Row([
                dd_carrera,
                dd_semestre
            ], spacing=10),
            # Espacio para el Genero
            row_genero,
            # Botón final
            btn_enviar
        ], spacing=15)
    )

# Ejecución específica para visualización en Navegador
ft.app(target=main, view=ft.AppView.WEB_BROWSER)