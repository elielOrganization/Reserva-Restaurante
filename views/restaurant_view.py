import flet as ft
from typing import Callable
from datetime import datetime, timedelta
from models.restaurant_model import Restaurante, Horario
from utils.utilidades import create_header

class RestauranteView:
    def __init__(self, page: ft.Page, restaurante_data: Restaurante, on_reserva_confirm: Callable = None, username = None, on_logout_click=None, on_logo_click=None):
        self.page = page
        self.restaurante = restaurante_data
        self.on_reserva_confirm = on_reserva_confirm
        self.username = username
        self.on_logout_click = on_logout_click
        self.on_logo_click = on_logo_click
        
        # --- Selector de Fecha (DatePicker) ---
        today = datetime.now()
        self.date_picker = ft.DatePicker(
            first_date=today,
            last_date=today + timedelta(days=90),
            on_change=self._on_fecha_change,
            on_dismiss=self._on_date_dismiss
        )
        self.page.overlay.append(self.date_picker)

        self.fecha_input = ft.TextField(
            label="Fecha", 
            width=250,
            read_only=True,
            hint_text="Clic para seleccionar fecha",
            on_focus=self._open_date_picker,
            icon=ft.Icons.CALENDAR_MONTH 
        )

        # --- Selector de Hora (Dropdown filtrado) ---
        self.hora_input = ft.Dropdown(
            label="Hora", 
            width=250,
            options=self._get_lista_horas(),
            trailing_icon=ft.Icons.ACCESS_TIME 
        )
        
        self._build_components()

    def _open_date_picker(self, e):
        self.date_picker.open = True
        self.page.update()

    def _on_fecha_change(self, e):
        if e.control.value:
            self.fecha_input.value = e.control.value.strftime("%Y-%m-%d")
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
        
        # Información aumentada de tamaño
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
        self.fecha_input.error_text = None
        self.hora_input.error_text = None
        self.page.update()

    def _on_confirmar_reserva(self, e):
        self._clear_errors()
        fecha = self.fecha_input.value
        hora = self.hora_input.value
        
        has_error = False
        if not fecha:
            self.fecha_input.error_text = "Fecha requerida"
            has_error = True
        if not hora:
            self.hora_input.error_text = "Hora requerida"
            has_error = True
            
        if has_error:
            self.page.update()
            return
        
        if self.on_reserva_confirm:
            success = self.on_reserva_confirm(fecha, hora)
            if success:
                self._show_snack("¡Reserva confirmada!", success=True)
                self.fecha_input.value = ""
                self.hora_input.value = None
            else:
                self._show_snack("Error al confirmar reserva", success=False)
        else:
            self._show_snack("Reserva simulada exitosa", success=True)
        self.page.update()

    def _show_snack(self, message: str, success: bool = False):
        bg_color = ft.Colors.GREEN_600 if success else ft.Colors.RED_600
        snack = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE, size=16),
            bgcolor=bg_color
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    def build(self) -> ft.Container:
        header = create_header(
            username=self.username, 
            on_logout_click=self.on_logout_click,
            on_logo_click=lambda _: self.on_logo_click(self.username) if self.on_logo_click else None
        )

        col_imagen = ft.Container(content=self.img_principal, col={"sm": 12, "md": 6, "lg": 8})
        
        info_col = ft.Column([
            self.nombre_text,
            self.direccion_text,
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT), # Espaciador
            self.telefono_text,
            self.aforo_text,
            ft.Container(content=self.horario_text, padding=ft.padding.only(top=10))
        ], spacing=10)
        
        col_info = ft.Container(
            content=info_col,
            padding=ft.padding.only(top=40, left=20),
            col={"sm": 12, "md": 12, "lg": 4},
        )

        reserva_row = ft.Row(
            [
                self.fecha_input,
                ft.Container(width=12),
                self.hora_input,
                ft.Container(width=20),
                ft.ElevatedButton(
                    "Reservar ahora",
                    on_click=self._on_confirmar_reserva,
                    bgcolor=ft.Colors.GREEN_600,
                    color=ft.Colors.WHITE,
                    width=180,
                    height=50
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12
        )

        footer_reserva = ft.Container(
            content=ft.Column([
                ft.Text("Finalizar Reserva", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(height=10),
                reserva_row
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.all(30),
            col={"sm": 12, "md": 12, "lg": 12},
            border=ft.border.all(2, ft.Colors.GREEN_400),
            border_radius=15,
            margin=ft.margin.only(top=30, bottom=30)
        )

        contenido = ft.ResponsiveRow([
            header,
            col_imagen,
            col_info
        ], spacing=20, run_spacing=20)

        return ft.Container(
            content=ft.Column([contenido, footer_reserva], scroll=ft.ScrollMode.AUTO),
            expand=True
        )