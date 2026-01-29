import flet as ft
from typing import Callable
from models.restaurant_model import Restaurante, Horario
from utils.utilidades import create_header

class RestauranteView:
    def __init__(self, page: ft.Page, restaurante_data: Restaurante, on_reserva_confirm: Callable = None, username = None, on_logout_click=None):
        self.page = page
        self.restaurante = restaurante_data
        self.on_reserva_confirm = on_reserva_confirm
        self.username = username
        self.on_logout_click = on_logout_click
        
        # Campos de formulario reserva
        self.fecha_input = ft.TextField(
            label="Fecha", 
            width=250
        )
        self.hora_input = ft.TextField(
            label="Hora", 
            width=250
        )
        
        self._build_components()

    def _build_components(self):
        """Inicializa componentes visuales con datos del restaurante"""
        # Imagen principal (Ajustada para ser más prominente)
        self.img_principal = ft.Image(
            src=self.restaurante.imagenes,
            height=400,  
            expand=True,
            fit=ft.BoxFit.COVER, 
            border_radius=10
        )
        
        # Info del restaurante
        self.nombre_text = ft.Text(self.restaurante.nombre, size=24, weight=ft.FontWeight.BOLD)
        self.direccion_text = ft.Text(self.restaurante.direccion, size=14, color=ft.Colors.GREY_700)
        self.telefono_text = ft.Text(f"📞 {self.restaurante.telefono}", size=14)
        self.aforo_text = ft.Text(f"👥 Capacidad: {self.restaurante.aforo_maximo}", size=14)
        self.horario_text = ft.Text(
            f"🕒 {self.restaurante.horario.apertura} - {self.restaurante.horario.cierre}", 
            size=16
        )

    def _clear_errors(self):
        """Limpia errores de los campos"""
        self.fecha_input.error = None
        self.hora_input.error = None
        self.page.update()

    def _on_confirmar_reserva(self, e):
        """Maneja el click del botón confirmar reserva"""
        self._clear_errors()
        
        fecha = self.fecha_input.value or ""
        hora = self.hora_input.value or ""
        
        # Validaciones simples
        has_error = False
        if not fecha:
            self.fecha_input.error = "Fecha requerida"
            has_error = True
        if not hora:
            self.hora_input.error = "Hora requerida"
            has_error = True
            
        if has_error:
            self.page.update()
            return
        
        # Llamar callback o servicio de reserva
        if self.on_reserva_confirm:
            success = self.on_reserva_confirm(fecha, hora)
            if success:
                self._show_snack("¡Reserva confirmada!", success=True)
                self.fecha_input.value = ""
                self.hora_input.value = ""
            else:
                self._show_snack("Error al confirmar reserva", success=False)
        else:
            self._show_snack("Reserva simulada exitosa", success=True)
            
        self.page.update()

    def _show_snack(self, message: str, success: bool = False):
        """Muestra snackbar con feedback"""
        bg_color = ft.Colors.GREEN_600 if success else ft.Colors.RED_600
        snack = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE, size=16),
            bgcolor=bg_color
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    def build(self) -> ft.Container:
        """Construye la vista completa con padding y proporciones ajustadas"""
        header = create_header(
            username=self.username, 
            on_logout_click=self.on_logout_click,
        )
        # Columna 1: Imagen principal
        col_imagen = ft.Container(
            content=self.img_principal,
            col={"sm": 12, "md": 6, "lg": 6},
        )
        
        # Columna 2: Información del restaurante
        info_col = ft.Column([
            self.nombre_text,
            self.direccion_text,
            self.telefono_text,
            self.aforo_text,
            ft.Divider(),
            self.horario_text
        ], spacing=8)
        
        col_info = ft.Container(
            content=info_col,
            padding=ft.padding.only(top=40),
            col={"sm": 12, "md": 12, "lg": 6},
        )

        # Columna 3: Formulario de reserva
        formulario = ft.Column([
            ft.Text("Reserva", size=20, weight=ft.FontWeight.BOLD),
            self.fecha_input,
            self.hora_input,
            ft.Container(height=10),
            ft.ElevatedButton(
                "Confirmar reserva",
                on_click=self._on_confirmar_reserva,
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
                width=250,
                height=45
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12)
        
        col_formulario = ft.Container(
            content=formulario,
            padding=ft.padding.only(top=40),
            col={"sm": 12, "md": 6, "lg": 4},
            border=ft.border.all(2, ft.Colors.GREEN_400),
            border_radius=12
        )
        
        # Layout principal con ResponsiveRow
        contenido = ft.ResponsiveRow([
            header,
            col_imagen,
            col_info,
            col_formulario
        ], spacing=20, run_spacing=20)
        
        # Retornamos un Container con padding para que no toque los bordes de la ventana
        return ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO),
            # padding=ft.padding.only(top=40, left=20, right=20),
            expand=True
        )