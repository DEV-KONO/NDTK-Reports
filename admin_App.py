from logging import warning
from turtle import bgcolor, fillcolor
from wsgiref import validate
from dotenv import load_dotenv
from flet import *
import flet as ft
import requests
import os

from yaml import add_multi_constructor

load_dotenv(".api.env")

def admin_page(page: ft.Page, user: str):

    api_url = os.getenv("api_url")

    admin_request = requests.get(f"{api_url}validate_admin", json={"email":user})

    if admin_request.json()["admin"]:

        admin_client_name = ft.TextField(
            label="Ingrese el nombre del cliente",
            border_radius=10,
            keyboard_type=ft.KeyboardType.TEXT,
            width=320,
            visible=True
        )

        admin_plant_name = ft.TextField(
            label="Ingrese el nombre de la planta",
            border_radius=10,
            keyboard_type=ft.KeyboardType.TEXT,
            width=320,
            visible=True
        )

        admin_contact_name = ft.TextField(
            label="Ingrese el nombre del contacto",
            border_radius=10,
            keyboard_type=ft.KeyboardType.TEXT,
            width=320,
            visible=True
        )

        warning_text =  ft.Text(visible=False)

        def send_all(e):
            if admin_client_name.value and admin_contact_name.value and admin_plant_name.value:
                # print("text")
                warning_text.visible = False
                client_data = {
                    "name" : admin_client_name.value
                }
                plant_data = {
                    "name" : admin_plant_name.value,
                    "client_name" : admin_client_name.value
                }
                contact_data = {
                    "name" : admin_contact_name.value,
                    "client_name" : admin_client_name.value
                }

                add_client_request = requests.post(url=f"{api_url}add_client/", json=client_data)

                try:
                    if add_client_request.json()["error"] == "Client already exists!!":
                        warning_text.visible = True
                        warning_text.value = "Ya hay un cliente con este nombre"
                        page.update()
                        return None
                    else:

                        add_plant_request = requests.post(url=f"{api_url}add_plant/", json=plant_data)

                        add_contact_request = requests.post(url=f"{api_url}add_contact/", json=contact_data)

                        admin_client_name.value = ""
                        admin_plant_name.value = ""
                        admin_contact_name.value = ""

                    page.update()
                except KeyError:
                    print("error with the add client request key")

                # print(add_client_request)
                # print(add_plant_request)
                # print(add_contact_request)

            else:
                warning_text.visible = True
                warning_text.value = "Faltó de rellenar algún dato"
                page.update()

        send_all_btn = ft.ElevatedButton(
            text="Guardar Cliente",
            color="white",
            bgcolor=ft.colors.PURPLE,
            visible=True,
            on_click=send_all
        )

        inspector_name = ft.TextField(
            label="Ingrese el nombre del Inspector",
            border_radius=10,
            keyboard_type=ft.KeyboardType.TEXT,
            width=320,
            visible=True
        )

        # def label_change(e):
        #     if admin_bool.value:
        #         admin_bool.label = "admin?: Sí"
        #     else:
        #         admin_bool.label = "admin?: No"
        #     e.page.update()


        # admin_bool = ft.CupertinoCheckbox(
        #     label="admin?: No",
        #     on_change=label_change,
        #     value=False
        # )

        def send_ins(e):
            if inspector_name.value != "":
                validate_inspector = requests.post(url=f"{api_url}add_inspector", json={"name" : inspector_name.value})

                validate_inspector = validate_inspector.json()

                if validate_inspector["error"]:
                    inspector_warning.visible = True
                    inspector_warning.value = validate_inspector["msg"]
                else:
                    inspector_warning.visible = False
                    inspector_name.value = ""

            else:
                inspector_warning.visible = True
                inspector_warning.value = "No inspector name given"

            page.update()

        inspector_btn = ft.ElevatedButton(
            text="Guardar Inspector",
            color="white",
            bgcolor=ft.colors.PURPLE,
            visible=True,
            on_click=send_ins
        )

        inspector_warning = ft.Text(visible=False)

        admin_request = requests.get(f"{api_url}all_admins")

        admin_json_list = admin_request.json()

        def admin_and_user(admin: dict):
            if admin["email"] == user:
                
                return
            
            else:

                if admin["admin"]:
                    admin_dropdown.options.append(ft.dropdown.Option(text=f"{admin["email"]}   <--   ADMIN"))
                else:
                    admin_dropdown.options.append(ft.dropdown.Option(text=f"{admin['email']}"))

        def reload_admin_dropdown(e):

            admin_dropdown.options = []

            nonlocal admin_request
            nonlocal admin_json_list
            
            admin_request = requests.get(f"{api_url}all_admins")
            admin_json_list = admin_request.json()
            
            parser = list(map(admin_and_user, admin_json_list))

            if "   <--   ADMIN" in e.control.value:
                admin_changer_btn.text = "Revocar Derechos"
                page.update()
            else:
                admin_changer_btn.text = "Hacer Administrador"
                page.update()

        admin_dropdown = ft.Dropdown(
            label="Lista de Usuarios",
            bgcolor="white",
            border_radius=10,
            width=320,
            color="black",
            on_change=reload_admin_dropdown
        )

        parser = list(map(admin_and_user, admin_json_list))

        def change_admin(e):

            if "   <--   ADMIN" in admin_dropdown.value:
                admin_change_request = requests.put(f"{api_url}change_admin", json={"email":admin_dropdown.value.replace("   <--   ADMIN", "")})
                admin_dropdown.value = admin_dropdown.value.replace("   <--   ADMIN", "")
                admin_changer_btn.text = "Hacer Administrador"
            else:
                admin_change_request = requests.put(f"{api_url}change_admin", json={"email":admin_dropdown.value})
                admin_dropdown.value = admin_dropdown.value + "   <--   ADMIN"
                admin_changer_btn.text = "Revocar Derechos"

            admin_dropdown.options = []

            nonlocal admin_request
            nonlocal admin_json_list
            
            admin_request = requests.get(f"{api_url}all_admins")
            admin_json_list = admin_request.json()
            
            parser = list(map(admin_and_user, admin_json_list))

            page.update()
            

        admin_changer_btn = ft.ElevatedButton(
            text="Hacer Administrador",
            color="white",
            bgcolor=ft.colors.PURPLE,
            visible=True,
            on_click=change_admin
        )

        admin_container = ft.Container(
            # width=400,
            # height=730,
            # padding=ft.padding.only(top=10),
            # bgcolor=ft.colors.WHITE,
            content= ft.Column(
                horizontal_alignment="center",
                controls=[
                    ft.Container(
                            width=400,
                            height=50,
                            padding=ft.padding.only(top=10),
                            bgcolor=ft.colors.WHITE,
                            content=ft.Column(
                                horizontal_alignment="center",
                                controls=[
                                    ft.Text("Admin Dashboard", size=20, weight="bold", color="black"),
                                ]
                            ),
                    ),
                    #Client Adder   
                    ft.Container(
                        width=400,
                        height=330,
                        padding=ft.padding.only(top=10),
                        bgcolor=ft.colors.WHITE,
                        content=ft.Column(
                            horizontal_alignment="center",
                            controls=[
                                ft.Text("Cliente", size=20, weight="bold", color="black"),
                                admin_client_name,
                                admin_plant_name,
                                admin_contact_name,
                                warning_text,
                                send_all_btn
                            ]
                        )
                    ),
                    ft.Container(
                        width=400,
                        height=230,
                        padding=ft.padding.only(top=10),
                        bgcolor=ft.colors.WHITE,
                        content=ft.Column(
                            horizontal_alignment="center",
                            controls=[
                                ft.Text("Inspector", size=20, weight="bold", color="black"),#Me estoy enamorando
                                inspector_name,
                                inspector_warning,
                                inspector_btn
                            ]
                        )
                    ),
                    ft.Container(
                        width=400,
                        height=300,
                        padding=ft.padding.only(top=10),
                        bgcolor=ft.colors.WHITE,
                        content=ft.Column(
                            horizontal_alignment="center",
                            controls=[
                                ft.Text("Cambiar Administrador", size=20, weight="bold", color="black"),
                                admin_dropdown,
                                admin_changer_btn
                            ]
                        )
                    ),
                ]
            )
        )
        
        return admin_container

    else:
        admin_container = ft.Container(
            width=400,
            height=730,
            padding=ft.padding.only(top=10),
            bgcolor=ft.colors.WHITE,
            content= ft.Column(
                horizontal_alignment="center",
                controls=[
                    ft.Text("No tienes permisos de administrador, pidele a un administrador que te otorgue permiso", color="black")
                ]
            )
        )
        
        return admin_container