import flet as ft

def show_toast_msg(self, message: str, success: bool = False):
    if success:
        bg_color = ft.Colors.GREEN_600
        text_color = ft.Colors.WHITE
    else:
        bg_color = ft.Colors.RED_600
        text_color = ft.Colors.WHITE
    
    snack = ft.SnackBar(
        content=ft.Container(
            content=ft.Text(
                message,
                color=text_color,
                size=16,
            ),
            padding=20,
        ),
        bgcolor=bg_color,
    )
    self.page.show_dialog(snack)
    self.page.update()

def create_header(username, on_logout_click=None, on_logo_click=None, on_reservas_click=None):
    """Genera el header reutilizable con logo clicable usando GestureDetector"""
    
    user_menu = ft.PopupMenuButton(
        content=ft.Image(
            src="./images/banner/tl.png", 
            height=40,
            width=40,
            fit=ft.BoxFit.CONTAIN,
        ),
        items=[
            ft.PopupMenuItem(
                icon=ft.Icons.PERSON, 
                content=ft.Text(f"Usuario: {username}" if username else "Perfil")
            ),
            ft.PopupMenuItem(), 
            ft.PopupMenuItem(
                icon=ft.Icons.LOGOUT, 
                content=ft.Text("Cerrar Sesión"), 
                on_click=on_logout_click if on_logout_click else None
            ),
        ],
    )

    return ft.Container(
        bgcolor="#1b5e20",
        height=100,
        padding=ft.padding.symmetric(horizontal=40),
        content=ft.Row([
            ft.GestureDetector(
                content=ft.Image(src="./images/banner/logo.png", height=80),
                # El logo ejecuta la acción si existe
                on_tap=lambda _: on_logo_click(username) if on_logo_click else None, 
                mouse_cursor=ft.MouseCursor.CLICK,
            ),
    
            ft.Row(
                controls=[
                    ft.TextButton(
                        content=ft.Text(
                            "MIS RESERVAS", 
                            color=ft.Colors.WHITE, 
                        ),
                        # --- CORRECCIÓN CLAVE AQUÍ ---
                        # Ahora el botón sí responde al click
                        on_click=lambda _: on_reservas_click() if on_reservas_click else None
                    ),
                    user_menu,
                ],
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )