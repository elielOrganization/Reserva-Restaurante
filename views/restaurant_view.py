import flet as ft
from typing import Callable
from datetime import datetime, timedelta
from models.restaurant_model import Restaurante, Horario
from utils.utilidades import create_header, show_toast_msg
from services.crud_operations import registrar_reserva, calcular_reservas_disponible

class RestauranteView:
    def __init__(self, page: ft.Page, restaurante_data: Restaurante, on_reserva_confirm: Callable = None, username = None, on_logout_click=None, on_logo_click=None):
        self.page = page
        self.restaurante = restaurante_data
        self.on_reserva_confirm = on_reserva_confirm
        self.username = username
        self.on_logout_click = on_logout_click
        self.on_logo_click = on_logo_click
        
        # --- Atributos de clase ---
        today = datetime.now()
        self.fecha_hoy = today.strftime("%Y-%m-%d")

        # --- Selector de Fecha ---
        self.date_picker = ft.DatePicker(
            first_date=today,
            last_date=today + timedelta(days=90),
            on_change=self._on_fecha_change,
            on_dismiss=self._on_date_dismiss
        )
        self.page.overlay.append(self.date_picker)

        # --- Componentes de Formulario ---
        self.fecha_input = ft.TextField(
            label="Fecha", 
            width=250,
            read_only=True,
            hint_text="Clic para seleccionar fecha",
            on_click=self._open_date_picker,
            suffix_icon=ft.Icons.CALENDAR_MONTH,
            value=self.fecha_hoy,
        )

        self.hora_input = ft.Dropdown(
            label="Hora", 
            width=250,
            options=self._get_lista_horas(),
            hint_text="Clic para seleccionar hora",
            trailing_icon=ft.Icons.ACCESS_TIME 
        )
        
        # Inicializar opciones de personas para la fecha de hoy
        disponibles_hoy = calcular_reservas_disponible(self.restaurante, self.fecha_hoy)
        self.personas_input = ft.Dropdown(
            label="Personas",
            width=150,
            options=[ft.dropdown.Option(str(i)) for i in range(1, disponibles_hoy + 1)],
            hint_text="Nº personas"
        )
        
        self._build_components()

    # --- Gestión de Eventos ---
    def _open_date_picker(self, e):
        self.date_picker.open = True
        self.page.update()

    def _on_fecha_change(self, e):
        self._clear_errors()

        if e.control.value:
            nueva_fecha = e.control.value.strftime("%Y-%m-%d")
            self.fecha_input.value = nueva_fecha
            
            disponibles = calcular_reservas_disponible(self.restaurante, nueva_fecha)
            nuevas_opciones = [ft.dropdown.Option(str(i)) for i in range(1, disponibles + 1)]

            self.personas_input.options = nuevas_opciones
            self.personas_input.value = None 
            
        self.date_picker.open = False 
        self.page.update() 

    def _on_date_dismiss(self, e):
        self.date_picker.open = False
        self.page.update()

    def _get_lista_horas(self):
        opciones = []
        fmt = "%H:%M"
        try:
            inicio = datetime.strptime(self.restaurante.horario.apertura, fmt)
            fin = datetime.strptime(self.restaurante.horario.cierre, fmt)
            actual = inicio
            while actual <= fin:
                hora_str = actual.strftime(fmt)
                opciones.append(ft.dropdown.Option(hora_str))
                actual += timedelta(minutes=30)
        except Exception as e:
            print(f"Error procesando horario: {e}")
            return [ft.dropdown.Option("Horario no disponible")]
        return opciones

    def _build_components(self):
        self.img_principal = ft.Image(
            src=self.restaurante.imagenes,
            height=400,  
            expand=True,
            fit=ft.BoxFit.COVER, 
            border_radius=10
        )
        
        self.nombre_text = ft.Text(self.restaurante.nombre, size=40, weight=ft.FontWeight.BOLD)
        self.direccion_text = ft.Text(self.restaurante.direccion, size=18, color=ft.Colors.GREY_700)
        self.telefono_text = ft.Text(f"📞 {self.restaurante.telefono}", size=18, weight=ft.FontWeight.W_500)
        self.aforo_text = ft.Text(f"👥 Capacidad: {self.restaurante.aforo_maximo} personas", size=18)
        self.horario_text = ft.Text(
            f"Horario: {self.restaurante.horario.apertura} - {self.restaurante.horario.cierre}", 
            size=22,
            color=ft.Colors.GREEN_700,
            weight=ft.FontWeight.BOLD
        )

    def _clear_errors(self):
        self.fecha_input.error = None
        self.hora_input.error_text = None
        self.personas_input.error_text = None
        
        self.page.update()

    def _on_confirmar_reserva(self, e):
        self._clear_errors()

        usuario = self.username
        fecha = self.fecha_input.value
        hora = self.hora_input.value
        fecha_hora_completa = f"{fecha}T{hora}:00"
        personas = self.personas_input.value
        restaurante_nombre = self.restaurante.nombre

        has_error = False
        if not personas:
            self.personas_input.error_text = "Seleccione número de personas"
            has_error = True

        if not fecha:
            self.fecha_input.error = "Fecha requerida"  
            has_error = True

        if not hora:
            self.hora_input.error_text = "Hora requerida"
            has_error = True
        
        if has_error:
            self.page.update()
            return
        
        personas = int(personas)

        success, msg = registrar_reserva(usuario, fecha_hora_completa, restaurante_nombre, personas)

        show_toast_msg(self.page, msg, success)

        if success:
            nueva_reserva = {
            "fecha_hora": fecha_hora_completa,
            "estado": "confirmada",
            "restaurante_nombre": restaurante_nombre,
            "num_personas": personas,
            "usuario": usuario,
            }

            self.restaurante.reservas.append(nueva_reserva)
            disponibles = calcular_reservas_disponible(self.restaurante, self.fecha_input.value)
            nuevas_opciones = [ft.dropdown.Option(str(i)) for i in range(1, disponibles + 1)]
       
            self.personas_input.options = nuevas_opciones
            self.fecha_input.value = self.fecha_hoy
            self.hora_input.value = None
            self.personas_input.value = None

            self.page.update()

    def build(self) -> ft.Container:
        header = create_header(
            username=self.username, 
            on_logout_click=self.on_logout_click,
            on_logo_click=lambda _: self.on_logo_click(self.username) if self.on_logo_click else None
        )

        reserva_row = ft.Row(
            [
                self.personas_input,
                ft.Container(width=5),
                self.fecha_input,
                ft.Container(width=5),
                self.hora_input,
                ft.ElevatedButton(
                    "Reservar ahora",
                    on_click=self._on_confirmar_reserva,
                    bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE,
                    width=180, height=50
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )

        footer_reserva = ft.Container(
            content=ft.Column([
                ft.Text("Finalizar Reserva", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(height=10),
                reserva_row
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=30, border=ft.border.all(2, ft.Colors.GREEN_400), border_radius=15, margin=ft.margin.only(top=30)
        )

        return ft.Container(
            content=ft.Column([ 
                header,
                ft.ResponsiveRow([
                    ft.Container(content=self.img_principal, col={"sm": 12, "md": 7}),
                    ft.Container(content=ft.Column([
                        self.nombre_text, self.direccion_text, self.telefono_text, self.aforo_text, self.horario_text
                    ], spacing=10), col={"sm": 12, "md": 5}, padding=20)
                ]),
                footer_reserva
            ], scroll=ft.ScrollMode.AUTO),
            expand=True
        )