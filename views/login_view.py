import flet as ft
from services.crud_operations import login_user
from utils.utilidades import show_toast_msg


class LoginView:
    """Vista de login"""

    def __init__(self, page: ft.Page, on_register_click=None, on_login_success=None):
        self.page = page
        self.on_register_click = on_register_click
        self.on_login_success = on_login_success

    def _on_login(self, e):
        """Valida credenciales y ejecuta on_login_success si son correctas"""
        try:
            username = self.usuario_input.value or ""
            password = self.password_input.value or ""
            
            if not username or not password:
                show_toast_msg(self, "Usuario y contraseña son requeridos")
                return
            
            success, msg, logged_username = login_user(username, password)
            
            if success and callable(self.on_login_success):
                self.on_login_success(logged_username)
            else:
                show_toast_msg(self,msg, success=False)

        except Exception as ex:
            show_toast_msg(self, f"Error: {str(ex)}", success=False)

    def build(self) -> ft.Column:
        """Construye la vista visual de login"""
        
        # Campos de entrada
        self.usuario_input = ft.TextField(
            label="Usuario",
            width=350,
        )

        self.password_input = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=350,
        )

        # Botón login
        login_button = ft.ElevatedButton(
            "Iniciar Sesión",
            width=350,
            height=50,
            on_click=self._on_login,
        )

        # Botón ir a registro
        register_button = ft.TextButton(
            "¿No tienes cuenta? Regístrate aquí",
            width=350,
            on_click=self.on_register_click,
        )

        return ft.Column(
            [
                ft.Text(
                    "SISTEMA DE RESERVAS",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Restaurante XYZ",
                    size=16,
                    color=ft.Colors.GREY_700,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(),
                ft.Column(
                    [
                        self.usuario_input,
                        self.password_input,
                        ft.Container(height=10),
                        login_button,
                        ft.Container(height=10),
                        register_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )


def main(page: ft.Page):
    """Función para ejecutar el login directamente"""
    page.title = "Sistema de Reservas - Restaurante"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    login_view = LoginView(page)
    page.add(login_view.build())


if __name__ == "__main__":
    ft.run(main)
