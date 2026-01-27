import flet as ft
from views.login_view import LoginView
from views.register_view import RegisterView
from views.main_view import MainView


def main(page: ft.Page):
    """Función principal de la aplicación"""
    
    # Configurar página
    page.title = "Sistema de Reservas - Restaurante"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def show_login(e=None):
        """Muestra la vista de login"""
        page.clean()
        login_view = LoginView(
            page, 
            on_register_click=show_register,
            on_login_success=show_main
        )
        page.add(login_view.build())
    
    def show_register(e=None):
        """Muestra la vista de registro"""
        page.clean()
        register_view = RegisterView(page, on_back_click=show_login)
        page.add(register_view.build())
    
    # Esta parte la tiene que hacer Diego
    def show_main(username: str):
        """Muestra la vista principal tras login exitoso"""
        page.clean()
        main_view = MainView(page, username=username, on_logout_click=show_login)
        page.add(main_view.build())
    
    # Mostrar login inicialmente
    show_login()


if __name__ == "__main__":
    ft.run(main)
