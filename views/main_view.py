import flet as ft


class RestaurantCard(ft.Container):
    """Componente reutilizable para las tarjetas de restaurante"""
    def __init__(self, nombre, imagen_url, on_click_action):
        super().__init__()
        self.padding = 10
        self.ink = True
        self.on_click = on_click_action
        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(
                        src=imagen_url,
                        border_radius=ft.border_radius.all(15),
                        width=280,
                        height=200,
                        fit=ft.BoxFit.COVER,  # ← Corregido aquí
                    ),
                    border_radius=ft.border_radius.all(15),
                    shadow=ft.BoxShadow(
                        spread_radius=2,
                        blur_radius=10,
                        color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                    )
                ),
                ft.Container(
                    content=ft.Text(nombre, weight=ft.FontWeight.BOLD, size=18),
                    padding=ft.padding.only(top=10),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
        self.width = 300
        self.height = 320


class MainView:
    def __init__(self, page: ft.Page, on_logout_click=None, username=None, restaurantes=None):
        self.page = page
        self.on_logout_click = on_logout_click
        self.username = username
        self.restaurantes = restaurantes
        
        # Componentes de búsqueda
        self.search_field = ft.TextField(
            hint_text="Buscar restaurantes...",
            # prefix_icon=ft.icons.SEARCH,
            border_radius=25,
            filled=True,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK87,
            text_style=ft.TextStyle(size=16),
            width=500,
            height=50,
            on_change=self._on_search_change
        )

        # Datos de ejemplo (Luego los traerás de mongo_service.py)
        self.restaurantes_data = [
            {"nombre": "Casa ramon", "img": "https://picsum.photos/300/200?1"},
            {"nombre": "res", "img": "https://picsum.photos/300/200?2"},
            {"nombre": "mar casa", "img": "https://picsum.photos/300/200?3"},
        ]
        
        # Contenedor para el grid que se actualizará al buscar
        self.grid_restaurantes = ft.ResponsiveRow(
            [
                ft.Container(col=4, content=card)
                for card in self._generar_tarjetas(self.restaurantes_data)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def _generar_tarjetas(self, lista_datos):
        """Genera la lista de controles RestaurantCard"""
        return [
            RestaurantCard(
                r["nombre"], 
                r["img"], 
                lambda e, n=r["nombre"]: self._on_restaurant_click(n)
            ) for r in lista_datos
        ]

    def _on_search_change(self, e):
        """Lógica funcional para filtrar restaurantes en tiempo real"""
        query = self.search_field.value.lower() if self.search_field.value else ""
        filtrados = [
            r for r in self.restaurantes_data 
            if query in r["nombre"].lower()
        ]
        self.grid_restaurantes.controls = [
            ft.Container(col=4, content=card)
            for card in self._generar_tarjetas(filtrados)
        ]
        self.page.update()

    def _on_restaurant_click(self, nombre):
        """Lógica al hacer click en un restaurante"""
        print(f"Navegando a: {nombre}")
        # self.page.go(f"/reserva/{nombre}")

    def build(self) -> ft.Column:
       # --- HEADER UNICO ---
        header = ft.Container(
            bgcolor="#1b5e20",
            height=70,
            padding=ft.padding.only(left=20, right=20),
            content=ft.Row(
                [
                    ft.Image(src="./images/banner/banner.png", height=50, width=200),
                    # ft.Container(expand=1),  # ← Spacer más chico
                    ft.TextButton("MIS RESERVAS", style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )
        # --- BANNER ---
        search_section = ft.Container(
            height=280,
            width=1700,  # ← Ancho fijo grande
            alignment=ft.Alignment.CENTER,
            content=ft.Stack([
                ft.Image(
                    src="./images/banner/banner.png", 
                    fit=ft.BoxFit.COVER,
                    expand=True  # ← Expande dentro del Container
                ),
                ft.Container(
                    content=self.search_field,
                    alignment=ft.Alignment.CENTER,
                    width=500,
                    height=50,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
                    ),
                )
            ]),
        )


        # --- Título ---
        titulo = ft.Container(
            content=ft.Text(
                "RESTAURANTES",
                size=32,
                weight=ft.FontWeight.W_600,
                color="#1b5e20",
            ),
            alignment=ft.Alignment.CENTER,
            padding=ft.padding.only(top=30, bottom=20),
        )

        # --- Grid de restaurantes ---
        grid_container = ft.Container(
            content=self.grid_restaurantes,
            padding=ft.padding.only(left=20, right=20),
            alignment=ft.Alignment.CENTER,
        )

        return ft.Column(
            controls=[header, search_section, titulo, grid_container],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
