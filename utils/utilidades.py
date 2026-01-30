import flet as ft

def show_toast_msg(self, message: str, success: bool = False):
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

import flet as ft

import flet as ft

def create_header(username, on_logout_click, on_logo_click, on_reservas_click=None):
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
                on_click=on_logout_click
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
                on_tap=on_logo_click, # <--- CAMBIO: Ahora ejecuta la función que le pasemos
                mouse_cursor=ft.MouseCursor.CLICK,
            ),
    
                ft.Row(
                    controls=[
                        ft.TextButton(
                            "MIS RESERVAS", 
                            style=ft.ButtonStyle(color=ft.Colors.WHITE),
                            on_click=on_reservas_click
                        ),
                        user_menu,
                    ],
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

