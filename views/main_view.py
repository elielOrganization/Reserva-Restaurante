import flet as ft
from utils.utilidades import create_header

class RestaurantCard(ft.Container):
    """Componente reutilizable para las tarjetas de restaurante usando el objeto BD directamente"""
    def __init__(self, on_click_action, restaurante_obj):
        super().__init__()
        self.padding = 10
        self.ink = True
        self.restaurante_obj = restaurante_obj 
        self.on_click = lambda _: on_click_action(self.restaurante_obj)

        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(
                        src=self.restaurante_obj.imagen_url, 
                        border_radius=ft.border_radius.all(15),
                        width=280,
                        height=200,
                        fit=ft.BoxFit.COVER,
                    ),
                    border_radius=ft.border_radius.all(15),
                    shadow=ft.BoxShadow(
                        spread_radius=2,
                        blur_radius=10,
                        color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                    )
                ),
                ft.Container(
                    content=ft.Text(
                        self.restaurante_obj.nombre, 
                        weight=ft.FontWeight.BOLD, 
                        size=18
                    ),
                    padding=ft.padding.only(top=10),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.width = 300
        self.height = 320

class MainView:
    def __init__(self, page: ft.Page, on_logout_click=None, username=None, restaurantes=None,  on_restaurant_click=None):
        self.page = page
        self.page.padding = 0
        self.page.spacing = 0
        self.on_logout_click = on_logout_click
        self.on_restaurant_click = on_restaurant_click
        self.username = username
        self.restaurantes = restaurantes 

        # Buscador
        self.search_field = ft.TextField(
            hint_text="Buscar restaurantes...",
            border_radius=25,
            filled=True,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK87,
            width=600, 
            height=50,
            on_change=self._on_search_change
        )

        # Grid inicial con todos los objetos
        self.grid_restaurantes = ft.ResponsiveRow(
            controls=self._generar_tarjetas(self.restaurantes),
            alignment=ft.MainAxisAlignment.CENTER,
            run_spacing=20,
        )

    def _generar_tarjetas(self, lista_objetos):
        """Crea los contenedores del grid usando los objetos de la BD"""
        if not lista_objetos:
            return []
        return [
            ft.Container(
                col={"sm": 12, "md": 6, "lg": 4}, 
                content=RestaurantCard(
                    restaurante_obj=obj, 
                    on_click_action=self._on_restaurant_click
                ), 
                alignment=ft.Alignment.CENTER
            ) for obj in lista_objetos
        ]

    def _on_search_change(self, e):
        """Filtra directamente sobre los atributos del objeto"""
        query = self.search_field.value.lower() if self.search_field.value else ""
        filtrados = [
            r for r in self.restaurantes 
            if query in r.nombre.lower()
        ]
        self.grid_restaurantes.controls = self._generar_tarjetas(filtrados)
        self.page.update()

    def _on_restaurant_click(self, restaurante_obj):
        if self.on_restaurant_click:
            self.on_restaurant_click(restaurante_obj, self.username, self.on_logout_click)

    def build(self) -> ft.Column:
        # LLAMADA A LA UTILIDAD CON NAVEGACIÓN
        header = create_header(
            username=self.username, 
            on_logout_click=self.on_logout_click,
            # on_reservas_click=lambda _: self.page.go("/mis_reservas") # <-- Cambia la ruta por la tuya
        )

        # --- BANNER ---
        search_section = ft.Container(
            height=350,
            content=ft.Stack([
                ft.Image(
                    src="./images/banner/banner.png", 
                    fit=ft.BoxFit.COVER,
                    width=2000, 
                    height=350,
                ),
                ft.Container(bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK), expand=True),
                ft.Container(
                    content=self.search_field,
                    alignment=ft.Alignment.CENTER,
                )
            ]),
        )

        # --- TÍTULO ---
        titulo = ft.Container(
            content=ft.Text("RESTAURANTES", size=32, weight=ft.FontWeight.W_600, color="#1b5e20"),
            alignment=ft.Alignment.CENTER,
            padding=ft.padding.only(top=40, bottom=20),
        )

        # --- GRID ---
        grid_container = ft.Container(
            content=self.grid_restaurantes,
            padding=ft.padding.symmetric(horizontal=60),
            alignment=ft.Alignment.CENTER,
        )

        return ft.Column(
            controls=[header, search_section, titulo, grid_container],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER 
        )