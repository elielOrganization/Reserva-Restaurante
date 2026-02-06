import flet as ft
from utils.utilidades import create_header, show_toast_msg
from services.crud_operations import obtener_reservas_usuario, cancelar_reserva_usuario

class UserReservationsView:
    def __init__(self, page: ft.Page, username: str, on_back_home=None, on_logout_click=None):
        self.page = page
        self.username = username
        self.on_back_home = on_back_home
        self.on_logout_click = on_logout_click
        self.content_column = ft.Column(spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def build(self):
        header = create_header(
            self.username, 
            on_logout_click=self.on_logout_click,
            on_logo_click=lambda _: self.on_back_home() if self.on_back_home else None
        )

        titulo = ft.Container(
            content=ft.Text("Gestión de Reservas", size=30, weight=ft.FontWeight.BOLD, color="#1b5e20"),
            padding=ft.padding.symmetric(vertical=20),
            alignment=ft.Alignment.CENTER
        )

        self.cargar_datos()

        return ft.Column(
            controls=[
                header,
                titulo,
                ft.Container(
                    content=self.content_column, 
                    padding=20, 
                    alignment=ft.Alignment.CENTER
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

    def cargar_datos(self):
        self.content_column.controls.clear()
        
        try:
            reservas = obtener_reservas_usuario(self.username)
        except Exception as e:
            self.content_column.controls.append(ft.Text(f"Error cargando reservas: {e}", color="red"))
            self.page.update()
            return

        if not reservas:
            self.content_column.controls.append(
                ft.Column([
                    ft.Icon(ft.Icons.EVENT_BUSY, size=50, color=ft.Colors.GREY_400),
                    ft.Text("No tienes reservas activas.", size=18, color=ft.Colors.GREY_500)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
            self.page.update()
            return

        for res in reservas:
            fecha_raw = res.get('fecha_hora', '').replace('T', ' ')
            nombre_rest = res.get("restaurante_nombre", "Restaurante")
            
            btn_cancelar = ft.ElevatedButton(
                "Cancelar Reserva",
                icon=ft.Icons.DELETE_OUTLINE,
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.RED_600,
                ),
                on_click=lambda e, r=nombre_rest, f=res.get('fecha_hora'): self.eliminar_reserva(r, f)
            )

            card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.RESTAURANT_MENU, color="#F1884D"),
                        ft.Text(nombre_rest, weight="bold", size=20)
                    ]),
                    ft.Divider(),
                    ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_MONTH, size=16, color="grey"),
                        ft.Text(f" {fecha_raw}", size=16),
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.PEOPLE, size=16, color="grey"),
                        ft.Text(f" {res.get('num_personas')} personas", size=16),
                    ]),
                    ft.Container(height=15),
                    ft.Row([btn_cancelar], alignment=ft.MainAxisAlignment.END)
                ]),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                border=ft.border.all(1, ft.Colors.GREY_300),
                width=500,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
            )
            self.content_column.controls.append(card)
        
        self.page.update()

    def eliminar_reserva(self, restaurante_nombre, fecha_hora):
        try:
            success, msg = cancelar_reserva_usuario(self.username, restaurante_nombre, fecha_hora)
            
            if success:
                show_toast_msg(self.page, "Reserva cancelada correctamente", success=True)
                self.cargar_datos()
            else:
                show_toast_msg(self.page, f"Error: {msg}", success=False)
                
        except Exception as ex:
            show_toast_msg(self.page, f"Error de conexión: {str(ex)}", success=False)