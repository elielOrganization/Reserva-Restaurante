import flet as ft
from services.crud_operations import register_user
from utils.validators import is_nonempty, is_valid_email, is_valid_password, is_valid_phone

class RegisterView:
    def __init__(self, page: ft.Page, on_back_click=None):
        self.page = page
        self.on_back_click = on_back_click
        
        # Campos de entrada
        self.name_input = ft.TextField(label="Nombre Completo", width=350)
        self.user_input = ft.TextField(label="Usuario", width=350)
        self.password_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=350)
        self.confirm_password_input = ft.TextField(
            label="Confirmar Contraseña", password=True, can_reveal_password=True, width=350
        )
        self.phone_input = ft.TextField(label="Teléfono", width=350)
        self.email_input = ft.TextField(label="Email", width=350)

    def _clear_errors(self):
        """Limpia los mensajes de error de todos los campos"""
        for field in [self.name_input, self.user_input, self.password_input, 
                      self.confirm_password_input, self.phone_input, self.email_input]:
            field.error = None
        self.page.update()

    def _on_register(self, e):
        self._clear_errors() # Limpiar errores previos
        
        try:
            name = self.name_input.value or ""
            username = self.user_input.value or ""
            passwd = self.password_input.value or ""
            cpasswd = self.confirm_password_input.value or ""
            phone = self.phone_input.value or ""
            email = self.email_input.value or ""

            # Validaciones con error_text
            has_error = False

            if not is_nonempty(name):
                self.name_input.error = "Nombre requerido"
                has_error = True
            
            if not is_nonempty(username):
                self.user_input.error = "Usuario requerido"
                has_error = True

            if not is_valid_email(email):
                self.email_input.error = "Email inválido"
                has_error = True

            if not is_valid_password(passwd):
                self.password_input.error = "Mínimo 6 caracteres"
                has_error = True

            if passwd != cpasswd:
                self.confirm_password_input.error = "Las contraseñas no coinciden"
                has_error = True

            if not is_valid_phone(phone):
                self.phone_input.error = "Teléfono inválido"
                has_error = True

            if has_error:
                self.page.update()
                return

            # Si pasa las validaciones locales, llamar al servicio
            success, msg = register_user(name, username, email, phone, passwd)
            
            if success:
                self._show_snack("¡Usuario registrado con éxito!", success=True)
                if callable(self.on_back_click):
                    self.on_back_click(e)
            else:
                # Si el error viene de la DB (ej: usuario duplicado), usar snack o campo específico
                self._show_snack(msg, success=False)

        except Exception as ex:
            self._show_snack(f"Error: {str(ex)}", success=False)

    def _show_snack(self, message: str, success: bool = False):
        if success:
            bg_color = ft.Colors.GREEN_600
            text_color = ft.Colors.WHITE
        else:
            bg_color = ft.Colors.RED_600
            text_color = ft.Colors.WHITE  # ← BLANCO para contraste
        
        snack = ft.SnackBar(
            content=ft.Container(
                content=ft.Text(
                    message,
                    color=text_color,
                    size=16,  # ← Tamaño texto
                ),
                padding=20,  # ← Padding interno
            ),
            bgcolor=bg_color,
        )
        self.page.show_dialog(snack)
        self.page.update()

    def build(self) -> ft.Column:
        register_button = ft.ElevatedButton(
            "Registrarse", width=350, height=50, on_click=self._on_register
        )
        back_button = ft.TextButton(
            "¿Ya tienes cuenta? Inicia sesión", width=350, on_click=self.on_back_click
        )

        return ft.Column(
            [
                ft.Text("CREAR CUENTA", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Restaurante XYZ", size=16, color=ft.Colors.GREY_700),
                ft.Divider(),
                ft.Column(
                    [
                        self.name_input,
                        self.user_input,
                        self.password_input,
                        self.confirm_password_input,
                        self.phone_input,
                        self.email_input,
                        ft.Container(height=10),
                        register_button,
                        back_button,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )