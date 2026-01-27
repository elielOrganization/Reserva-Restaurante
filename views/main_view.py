import flet as ft


class MainView:
    """Vista principal después del login"""

    def __init__(self, page: ft.Page, username: str, on_logout_click=None):
        self.page = page
        self.username = username
        self.on_logout_click = on_logout_click

    def build(self) -> ft.Column:
        """Construye la vista principal"""
        
        logout_button = ft.ElevatedButton(
            "Cerrar Sesión",
            width=150,
            height=50,
            on_click=self.on_logout_click,
            bgcolor=ft.Colors.RED_400,
            color=ft.Colors.WHITE,
        )

        return ft.Column(
            [
                ft.Text(
                    "BIENVENIDO AL SISTEMA",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"Usuario: {self.username}",
                    size=16,
                    color=ft.Colors.GREY_700,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(),
                ft.Container(
                    content=ft.Text(
                        "Aquí irá el contenido principal de la aplicación",
                        size=14,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=20,
                ),
                ft.Container(height=20),
                logout_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )
