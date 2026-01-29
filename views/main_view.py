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
                    content=ft.Text(nombre, weight=ft.FontWeight.BOLD, size=18),
                    padding=ft.padding.only(top=10),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centrar texto bajo imagen
        )
        self.width = 300
        self.height = 320

class MainView:
    def __init__(self, page: ft.Page, on_logout_click=None, username=None, restaurantes=None):
        self.page = page
        # Configuración de página para eliminar márgenes laterales
        self.page.padding = 0
        self.page.spacing = 0
        self.on_logout_click = on_logout_click
        self.username = username
        self.restaurantes = restaurantes
        
        # Componente de búsqueda centrado y estilizado
        self.search_field = ft.TextField(
            hint_text="Buscar restaurantes...",
            border_radius=25,
            filled=True,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK87,
            text_style=ft.TextStyle(size=16),
            width=600, 
            height=50,
            on_change=self._on_search_change
        )

        # Carga de datos de restaurantes
        self.restaurantes_data = []
        if self.restaurantes:
            for r in self.restaurantes:
                self.restaurantes_data.append({
                    "nombre": r.nombre,
                    "img": r.imagen_url
                })
        else:
            # Fallback con tus rutas de imágenes locales según tu estructura
            self.restaurantes_data = [
                {"nombre": "Restaurante El Sol", "img": "./images/restaurantes/principal_sol.png"},
                {"nombre": "Carcas", "img": "./images/restaurantes/principal_carcas.png"},
                {"nombre": "La Paella Dorada", "img": "./images/restaurantes/principal_paella.png"},
            ]
        
        # Grid de restaurantes alineado al centro
        self.grid_restaurantes = ft.ResponsiveRow(
            [
                ft.Container(
                    col={"sm": 12, "md": 6, "lg": 4}, 
                    content=card, 
                    alignment=ft.Alignment.CENTER
                )
                for card in self._generar_tarjetas(self.restaurantes_data)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            run_spacing=20,
        )

    def _generar_tarjetas(self, lista_datos):
        return [
            RestaurantCard(
                r["nombre"], 
                r["img"], 
                lambda e, n=r["nombre"]: self._on_restaurant_click(n)
            ) for r in lista_datos
        ]

    def _on_search_change(self, e):
        query = self.search_field.value.lower() if self.search_field.value else ""
        filtrados = [
            r for r in self.restaurantes_data 
            if query in r["nombre"].lower()
        ]
        self.grid_restaurantes.controls = [
            ft.Container(col={"sm": 12, "md": 6, "lg": 4}, content=card, alignment=ft.Alignment.CENTER)
            for card in self._generar_tarjetas(filtrados)
        ]
        self.page.update()

    def _on_restaurant_click(self, nombre):
        print(f"Navegando a: {nombre}")

    def build(self) -> ft.Column:
        # --- HEADER ---
        header = ft.Container(
            bgcolor="#1b5e20",
            height=100,
            padding=ft.padding.symmetric(horizontal=40),
            content=ft.Row(
                [
                    ft.Image(src="./images/banner/logo.png", height=80),
                    ft.TextButton("MIS RESERVAS", style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )

        # --- BANNER CON BUSCADOR (Ajuste central) ---
        search_section = ft.Container(
            height=350,
            content=ft.Stack([
                ft.Image(
                    src="./images/banner/banner.png", 
                    fit=ft.BoxFit.COVER,
                    width=2000, # Valor alto para asegurar que cubra todo el ancho
                    height=350,
                ),
                # Superposición para mejorar contraste
                ft.Container(bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK), expand=True),
                # Buscador al medio
                ft.Container(
                    content=self.search_field,
                    alignment=ft.Alignment.CENTER,
                )
            ]),
        )

        # --- TÍTULO ---
        titulo = ft.Container(
            content=ft.Text(
                "RESTAURANTES",
                size=32,
                weight=ft.FontWeight.W_600,
                color="#1b5e20",
            ),
            alignment=ft.Alignment.CENTER,
            padding=ft.padding.only(top=40, bottom=20),
        )

        # --- CONTENEDOR PRINCIPAL DEL GRID ---
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