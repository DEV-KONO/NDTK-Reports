import flet as ft

'''
pasos para leer, mostrar y editar el json desde la app
1.- leer el json
2.- guardar el json
3.- mostrar una tabla en pantalla por cada "tabla" del json
4.- cuando se edite algun dato, se guarda en el json del programa y se reescribe el archivo
'''

def fabaction(e):
    e.page.go("/main_screen")
    e.page.update()

def data_page():
    return ft.View(
        "/data",
        scroll="always",
        floating_action_button= ft.FloatingActionButton(
            icon=ft.Icons.ARROW_BACK,
            bgcolor=ft.Colors.PURPLE,
            on_click=fabaction
        ),   
        horizontal_alignment="center",
        vertical_alignment="center",
        padding=0,
        bgcolor=ft.Colors.BLUE_50,
        controls=[ft.Text("Hola")]
    )