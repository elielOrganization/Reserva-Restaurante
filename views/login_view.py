import flet as ft


class LoginView:
    """Vista de login - Solo login"""

    def __init__(self, page: ft.Page, on_register_click=None):
        self.page = page
        self.on_register_click = on_register_click

    def build(self) -> ft.Column:
        """Construye la vista visual de login"""
        
        # Campos de entrada
        email_input = ft.TextField(
            label="Usuario",
            width=350,
        )

        password_input = ft.TextField(
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
                        email_input,
                        password_input,
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
