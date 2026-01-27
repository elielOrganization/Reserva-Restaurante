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