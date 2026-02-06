import flet as ft
from services.crud_operations import register_user
from utils.validators import is_nonempty, is_valid_email, is_valid_password, is_valid_phone
from utils.utilidades import show_toast_msg

class RegisterView:
    def __init__(self, page: ft.Page, on_back_click=None):
        self.page = page
        self.on_back_click = on_back_click
        
        # Estilos comunes para no repetir código
        input_style = {
            "width": 350,
            "border_color": ft.Colors.GREY_500,
            "label_style": ft.TextStyle(color=ft.Colors.GREY_700),
            "text_style": ft.TextStyle(color=ft.Colors.BLACK),
            "cursor_color": ft.Colors.BLACK
        }

        # Campos de entrada con el nuevo estilo visual
        self.name_input = ft.TextField(label="Nombre Completo", **input_style)
        self.user_input = ft.TextField(label="Usuario", **input_style)
        
        self.password_input = ft.TextField(
            label="Contraseña", 
            password=True, 
            can_reveal_password=True, 
            **input_style
        )
        
        self.confirm_password_input = ft.TextField(
            label="Confirmar Contraseña", 
            password=True, 
            can_reveal_password=True, 
            **input_style
        )
        
        self.phone_input = ft.TextField(label="Teléfono", **input_style)
        self.email_input = ft.TextField(label="Email", **input_style)

    def _clear_errors(self):
        """Limpia los mensajes de error de todos los campos"""
        for field in [self.name_input, self.user_input, self.password_input, 
                      self.confirm_password_input, self.phone_input, self.email_input]:
            field.error = None 
            
        self.page.update()

    def _on_register(self, e):
        self._clear_errors() 
        
        name = self.name_input.value or ""
        username = self.user_input.value or ""
        passwd = self.password_input.value or ""
        cpasswd = self.confirm_password_input.value or ""
        phone = self.phone_input.value or ""
        email = self.email_input.value or ""

        # Validaciones
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

        # Si pasa las validaciones, llamar al servicio
        success, msg = register_user(name, username, email, phone, passwd)

        show_toast_msg(self, msg, success)
        
        if success:
            self.on_back_click(e)    

    def build(self) -> ft.Column:
        # Botón de Registrar (Oscuro y redondeado)
        register_button = ft.ElevatedButton(
            content=ft.Text("Registrarse", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            width=350, 
            height=50, 
            on_click=self._on_register,
            bgcolor=ft.Colors.BLUE_GREY_900,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )

        # Botón volver (Azul)
        back_button = ft.TextButton(
            content=ft.Text("¿Ya tienes cuenta? Inicia sesión", color=ft.Colors.BLUE_700),
            width=350, 
            on_click=self.on_back_click
        )

        # Imagen del Logo
        logo_image = ft.Image(
            src="./images/banner/logo_login.jpg", 
            width=350,          
            fit="contain",
        )

        return ft.Column(
            [
                logo_image, 
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                
                
                ft.Column(
                    [
                        self.name_input,
                        self.user_input,
                        self.email_input,
                        self.phone_input,
                        self.password_input,
                        self.confirm_password_input,
                    ],
                    spacing=5, 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                
                ft.Container(height=10),
                register_button,
                back_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        )