import flet as ft


class RegisterView:
    """Vista de registro - Solo registro"""

    def __init__(self, page: ft.Page, on_back_click=None):
        self.page = page
        self.on_back_click = on_back_click

    def build(self) -> ft.Column:
        """Construye la vista visual de registro"""
        
        # Campos de entrada
        name_input = ft.TextField(
            label="Nombre Completo",
            width=350,
        )

        email_input = ft.TextField(
            label="Correo Electrónico",
            width=350,
        )

        password_input = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=350,
        )

        confirm_password_input = ft.TextField(
            label="Confirmar Contraseña",
            password=True,
            can_reveal_password=True,
            width=350,
        )

        phone_input = ft.TextField(
            label="Teléfono (Opcional)",
            width=350,
        )

        # Botón registro
        register_button = ft.ElevatedButton(
            "Registrarse",
            width=350,
            height=50,
        )

        # Botón volver
        back_button = ft.TextButton(
            "¿Ya tienes cuenta? Inicia sesión",
            width=350,
            on_click=self.on_back_click,
        )

        return ft.Column(
            [
                ft.Text(
                    "CREAR CUENTA",
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
                        name_input,
                        email_input,
                        password_input,
                        confirm_password_input,
                        phone_input,
                        ft.Container(height=10),
                        register_button,
                        ft.Container(height=10),
                        back_button,
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
