import flet as ft
from typing import Callable
from models.restaurant_model import Restaurante, Horario  # Tu dataclass anterior

class RestauranteView:
    def __init__(self, page: ft.Page, restaurante_data: Restaurante, on_reserva_confirm: Callable = None):
        self.page = page
        self.restaurante = restaurante_data
        self.on_reserva_confirm = on_reserva_confirm
        
        # Campos de formulario reserva
        self.fecha_input = ft.TextField(
            label="Fecha", 
            prefix_icon=ft.icons.CALENDAR_TODAY,
            width=250
        )
        self.hora_input = ft.TextField(
            label="Hora", 
            prefix_icon=ft.icons.ACCESS_TIME,
            width=250
        )
        
        self._build_components()

    def _build_components(self):
        """Inicializa componentes visuales con datos del restaurante"""
        # Imagen principal
        self.img_principal = ft.Image(
            src=self.restaurante.imagenes[0] if self.restaurante.imagenes else "placeholder.jpg",
            width=300,
            height=200,
            fit=ft.ImageFit.COVER,
            border_radius=10
        )
        
        # Galería pequeña
        self.galeria_imgs = [
            ft.Image(
                src=img, 
                width=80, 
                height=80, 
                fit=ft.ImageFit.COVER, 
                border_radius=8
            )
            for img in self.restaurante.imagenes[1:4]
        ]
        
        # Info del restaurante
        self.nombre_text = ft.Text(self.restaurante.nombre, size=24, weight=ft.FontWeight.BOLD)
        self.direccion_text = ft.Text(self.restaurante.direccion, size=14, color=ft.colors.GREY_700)
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
        bg_color = ft.colors.GREEN_600 if success else ft.colors.RED_600
        snack = ft.SnackBar(
            content=ft.Text(message, color=ft.colors.WHITE, size=16),
            bgcolor=bg_color
        )
        self.page.show_dialog(snack)
        self.page.update()

    def build(self) -> ft.Column:
        """Construye la vista completa del restaurante"""
        # Sección info izquierda
        info_col = ft.Column([
            self.nombre_text,
            self.direccion_text,
            self.telefono_text,
            self.aforo_text,
            ft.Divider(),
            self.horario_text
        ], spacing=8)
        
        # Galería
        galeria = ft.Row(self.galeria_imgs, wrap=True, spacing=8)
        
        # Sección izquierda completa (info + imágenes)
        izquierda = ft.Column([self.img_principal, galeria], spacing=10)
        
        # Formulario reserva derecha
        formulario = ft.Column([
            ft.Text("Reserva", size=20, weight=ft.FontWeight.BOLD),
            self.fecha_input,
            self.hora_input,
            ft.Container(height=10),
            ft.ElevatedButton(
                "Confirmar reserva",
                on_click=self._on_confirmar_reserva,
                bgcolor=ft.colors.GREEN_600,
                color=ft.colors.WHITE,
                width=250,
                height=45
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12)
        
        # Layout principal
        contenido = ft.Row([
            ft.Column([info_col, izquierda], col={"sm": 8}, spacing=20),
            ft.Container(
                formulario,
                col={"sm": 4},
                padding=20,
                border=ft.border.all(2, ft.colors.GREEN_400),
                border_radius=12
            )
        ], vertical_alignment=ft.CrossAxisAlignment.START)
        
        return ft.Column([contenido], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
