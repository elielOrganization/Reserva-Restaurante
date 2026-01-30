import flet as ft
from services.crud_operations import login_user
from utils.utilidades import show_toast_msg

class LoginView:
    def __init__(self, page: ft.Page, on_register_click=None, on_login_success=None):
        self.page = page
        self.on_register_click = on_register_click
        self.on_login_success = on_login_success

    def _on_login(self, e):
        """Maneja el evento de clic en el botón de iniciar sesión"""
        try:
            username = self.usuario_input.value or ""
            password = self.password_input.value or ""
            
            if not username or not password:
                show_toast_msg(self.page, "Usuario y contraseña son requeridos", success=False)
                return
            
            success, msg, logged_username = login_user(username, password)
            
            if success and callable(self.on_login_success):
                self.on_login_success(logged_username)
            else:
                show_toast_msg(self.page, msg, success=False)

        except Exception as ex:
            show_toast_msg(self.page, f"Error: {str(ex)}", success=False)

    def build(self):
        """Construye la interfaz gráfica del Login"""
        # Forzar el color de fondo en la página y actualizar
        self.page.bgcolor = "#F9F8F5"
        self.page.update()

        # INPUT USUARIO
        self.usuario_input = ft.TextField(
            label="Usuario",
            width=350,
            border_color=ft.Colors.GREY_500,
            label_style=ft.TextStyle(color=ft.Colors.GREY_700),
            text_style=ft.TextStyle(color=ft.Colors.BLACK),
            cursor_color=ft.Colors.BLACK
        )

        # INPUT CONTRASEÑA
        self.password_input = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=350,
            border_color=ft.Colors.GREY_500,
            label_style=ft.TextStyle(color=ft.Colors.GREY_700),
            text_style=ft.TextStyle(color=ft.Colors.BLACK),
            cursor_color=ft.Colors.BLACK
        )

        # BOTÓN INICIAR SESIÓN (Actualizado con verde GastroBook)
        login_button = ft.ElevatedButton(
            content=ft.Text("Iniciar Sesión", color=ft.Colors.WHITE, weight="bold"),
            width=350,
            height=50,
            on_click=self._on_login,
            bgcolor="#225734", 
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )

        # BOTÓN REGISTRO (Actualizado con naranja GastroBook)
        register_button = ft.TextButton(
            content=ft.Text("¿No tienes cuenta? Regístrate aquí", color="#F1884D"),
            width=350,
            on_click=self.on_register_click,
        )

        logo_image = ft.Image(
            src="./images/banner/logo_login.jpg", 
            width=350,          
            fit="contain",
        )

        # Columna principal
        columna_login = ft.Column(
            [
                logo_image,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
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
        )

        # Envolvemos en un Container para asegurar que el color cubra toda la vista
        return ft.Container(
            content=columna_login,
            bgcolor="#F9F8F5",
            expand=True,
            alignment=ft.Alignment.CENTER
        )

def main(page: ft.Page):
    page.title = "Sistema de Reservas - GastroBook"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F9F8F5"
    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    
    login_view = LoginView(page)
    page.add(login_view.build())

if __name__ == "__main__":
    ft.run(main)