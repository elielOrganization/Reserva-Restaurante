import flet as ft
from views.login_view import LoginView
from views.register_view import RegisterView
from views.main_view import MainView
from views.restaurant_view import RestauranteView
from views.user_reservations_view import UserReservationsView
from services.mongo_service import cargar_restaurantes

def main(page: ft.Page):
    page.title = "Sistema de Reservas - GastroBook"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    restaurantes_data = cargar_restaurantes()

    def show_login(e=None):
        page.clean()
        login_view = LoginView(
            page, 
            on_register_click=show_register,
            on_login_success=show_main
        )
        page.add(login_view.build())
        page.update()
    
    def show_register(e=None):
        page.clean()
        register_view = RegisterView(page, on_back_click=show_login)
        page.add(register_view.build())
        page.update()

    def show_reservas(username):
        page.clean()
        view = UserReservationsView(
            page,
            username=username,
            on_back_home=lambda: show_main(username),
            on_logout_click=show_login
        )
        page.add(view.build())
        page.update()
    
    def show_main(username: str, rest_list=None):
        page.clean()
        rest_to_pass = rest_list if rest_list else restaurantes_data
        
        main_view = MainView(
            page, 
            username=username, 
            restaurantes=rest_to_pass,
            on_logout_click=show_login,
            on_logo_click=lambda _: show_main(username),
            on_restaurant_click=lambda r: show_restaurant(r, username),
            on_reservas_click=lambda: show_reservas(username)
        )
        page.add(main_view.build())
        page.update()
    
    def show_restaurant(restaurante_obj, username: str):
        page.clean()
        restaurant_view = RestauranteView(
            page, 
            restaurante_data=restaurante_obj, 
            on_reserva_confirm=None,
            username=username, 
            on_logout_click=show_login, 
            on_logo_click=lambda _: show_main(username),
            on_reservas_click=lambda: show_reservas(username)
        )
        page.add(restaurant_view.build())
        page.update()
    
    show_login()

if __name__ == "__main__":
    ft.app(target=main)