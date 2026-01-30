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
            
            # Llamada a la lógica de negocio
            success, msg, logged_username = login_user(username, password)
            
            if success and callable(self.on_login_success):
                self.on_login_success(logged_username)
            else:
                show_toast_msg(self.page, msg, success=False)

        except Exception as ex:
            show_toast_msg(self.page, f"Error: {str(ex)}", success=False)

    def build(self) -> ft.Column:
        """Construye la interfaz gráfica del Login"""
        
        # INPUT USUARIO
        self.usuario_input = ft.TextField(
            label="Usuario",
            width=350,
            border_color=ft.Colors.GREY_500,
            label_style=ft.TextStyle(color=ft.Colors.GREY_700),
            text_style=ft.TextStyle(color=ft.Colors.BLACK), # Texto negro explícito
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

        # BOTÓN INICIAR SESIÓN
        login_button = ft.ElevatedButton(
            content=ft.Text("Iniciar Sesión", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            width=350,
            height=50,
            on_click=self._on_login,
            bgcolor=ft.Colors.BLUE_GREY_900, # Fondo oscuro elegante
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )

        # BOTÓN REGISTRO
        register_button = ft.TextButton(
            content=ft.Text("¿No tienes cuenta? Regístrate aquí", color=ft.Colors.BLUE_700),
            width=350,
            on_click=self.on_register_click,
        )

        # IMAGEN (LOGO)
        # Al estar en la carpeta 'assets', solo ponemos el nombre del archivo
        logo_image = ft.Image(
            src="./images/banner/logo_login.jpg", 
            width=350,          
            fit="contain", # Usamos string para evitar error de versión
        )

        # ESTRUCTURA DE LA COLUMNA
        return ft.Column(
            [
                logo_image, # La imagen va primero
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

# --- BLOQUE PARA PROBAR (OPCIONAL) ---
def main(page: ft.Page):
    page.title = "Sistema de Reservas - GastroBook"
    
    # Configuración visual: Modo Claro (Fondo Blanco)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    login_view = LoginView(page)
    page.add(login_view.build())

if __name__ == "__main__":
    # Si ejecutas este archivo directamente, le decimos que assets está en la carpeta superior
    # (Esto es solo para pruebas, al ejecutar app.py no hace falta)
    ft.run(main)