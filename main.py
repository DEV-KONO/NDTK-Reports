import flet as ft 
from flet import*
from utils.int_button import Stepper
import os
import json


    
    
def main(page:ft.Page):
    page.window.width=400
    page.window.height=730
    page.adaptive=True
    theme=ft.Theme()
    theme.page_transitions.windows=ft.PageTransitionTheme.NONE
    theme.page_transitions.android=ft.PageTransitionTheme.NONE
    page.theme=theme
    page.theme_mode=ft.ThemeMode.SYSTEM
    page.window.always_on_top=True
    page.update()   

    def event(e):
        if e.data == "detach" and page.platform == ft.PagePlatform.ANDROID:
            os._exit(1)
    page.on_app_lifecycle_state_change = event
    

    user_log = ft.TextField(
        label="email", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.EMAIL,
        width=320
    )
    user_psw = ft.TextField(
        label="password",
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        password=True,
        can_reveal_password=True,
        width=320
    )

    box_group = ft.RadioGroup(
        content=ft.Column(
            spacing=5,
            controls=[
                ft.Radio(label="VT", value="VT", label_style=ft.TextStyle(color="black"),),
                ft.Radio(label="UT", value="UT", label_style=ft.TextStyle(color="black"),),
                ft.Radio(label="X", value="X,", label_style=ft.TextStyle(color="black"),),
            ]
        )
    )
   

    inspectors = [
        {"id": 1, "name": "abdul"},
        {"id": 2, "name": "sam"},
        {"id": 3, "name": "nana"},
        {"id": 4, "name": "zahra"},
        {"id": 5, "name": "ahra"},
    ]

    in_name = []       

    for inspector in inspectors:
        in_name.append(
            ft.Checkbox(
                label=inspector["name"],
                label_style=ft.TextStyle(color="black"),
            )
        )
        
        

    
    client_name = ft.Dropdown(
        bgcolor="white",
        border_radius=10,
        width=320,
        color="black",
        options=[
            ft.dropdown.Option("Client name 1"),
            ft.dropdown.Option("Client name 2"),
            ft.dropdown.Option("Client name 3"),
            ft.dropdown.Option("others")
        ]
    )

    plant_location = ft.Dropdown(
        bgcolor="white",
        text_style=ft.TextStyle(color="black"),
        border_radius=10,
        color="black",
        width=320,
        options=[
            ft.dropdown.Option("Location/address 1"),
            ft.dropdown.Option("Location/address 2"),
            ft.dropdown.Option("Loaction/address 3"),
            ft.dropdown.Option("others")
        ]
    )

    def click(e):
        print(f"you click{job.value}")


    contact = ft.TextField(
        width=320,
        border_radius=10,
        label="contact",
        color="black",
        border_color="black",
        label_style=ft.TextStyle(color="black"),
        border_width=1
        
    )


    txt_1 = ft.TextField(
        width=320,
        border_radius=10,
        label="Discription",
        color="black",
        label_style=ft.TextStyle(color="black"),
        border_color="black",
        border_width=1

    ) 

    txt_2 = ft.TextField(
        width=320,
        border_radius=10,
        label="material",
        color="black",
        label_style=ft.TextStyle(color="black"),
        border_color="black",
        border_width=1
        
    ) 

    txt_3 = ft.TextField(
        width=320,
        border_radius=10,
        label="Heat",
        color="black",
        label_style=ft.TextStyle(color="black"),
        border_color="black",
        border_width=1
        
    )

    accept_val=ft.TextField(
        width=320,
        border_radius=10,
        label="Acceptance",
        color="black",
        label_style=ft.TextStyle(color="black"),
        border_color="black",
        border_width=1
        
    )

    nde_val=ft.TextField(
        width=320,
        border_radius=10,
        label="NDE",
        color="black",
        label_style=ft.TextStyle(color="black"),
        border_color="black",
        border_width=1
    )

    surface_val=ft.TextField(
        width=320,
        border_radius=10,
        label="Surface",
        color="black",
        label_style=ft.TextStyle(color="black"),
        border_color="black",
        border_width=1
    )


    job = Stepper()
    od_val = Stepper()
    id_val = Stepper()
    thick_val = Stepper()
    height_val = Stepper()


    def route_chnage(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                bgcolor=ft.colors.BLUE_50,
                controls=[
                    ft.Container(
                        width=400,
                        expand=True,
                        content=ft.Column(
                            alignment="center",
                            horizontal_alignment="center",
                            controls=[
                                ft.Icon(name=ft.icons.PERSON, size=250, color="black"),
                                ft.Container(
                                    content=ft.Column(
                                        alignment="center",
                                        horizontal_alignment="center",
                                        spacing=15,
                                        controls=[
                                            user_log,
                                            user_psw,
                                            ft.Container(
                                                height=10
                                            ),
                                            ft.ElevatedButton(
                                                "login",
                                                elevation=30,
                                                width=200,
                                                height=50,
                                                bgcolor=ft.colors.PURPLE,
                                                color="white",
                                                on_click=lambda _:page.go("/main_screen")
                                            )
                                        ],
                                      
                                    )
                                )
                            ]
                        )
                    ) 
                ],
            )
        ),

        if page.route == "/main_screen":
            page.views.append(
                ft.View(
                    "/main",
                    scroll="always",
                    horizontal_alignment="center",
                    vertical_alignment="center",
                    padding=0,
                    bgcolor=ft.colors.BLUE_50,
                    controls=[
                        ft.SafeArea(
                            ft.Container(
                                height=10,
                                expand=True,
                                bgcolor=ft.colors.PURPLE,
                            ),
                        ),
                        ft.Column(
                            controls=[
                                ft.Container(
                                    width=400,
                                    height=195,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("tipo de preuba", size=20, weight="bold", color="black"),
                                            ft.Container(
                                                padding=ft.padding.only(top=10),
                                                content=ft.Column(
                                                    controls=[
                                                        box_group
                                                    ]
                                                )
                                            ),
                                        ]
                                    ),
                                ),
                                ft.Container(
                                    width=400,
                                    height=229,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("inspector", size=20, weight="bold", color="black"),
                                            ft.Container(
                                            padding=ft.padding.only(top=10),
                                            content=ft.Column(
                                                spacing=5,
                                                controls=in_name # here, the problem, in?name is a list, so remove this, look
                                                    
                                                ) 
                                            ),
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=120,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("Client Name", size=20, weight="bold", color="black"),
                                            client_name,
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=120,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("Planta/plant", size=20, color="black"),
                                            plant_location,
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=120,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                           ft.Text("Contact name", size=20, color="black"),
                                            contact,
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=510,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("Part Information", size=30, weight="bold", color="black"),
                                            ft.Text("Part description", size=20, color="black"),
                                            txt_1,
                                            ft.Text("Material specs", size=20, color="black"),
                                            txt_2,
                                            ft.Text("Heat", size=20, color="black"),
                                            txt_3,
                                            ft.Text("Job qty", size=20, color="black"),
                                            ft.Container(
                                            content=job
                                            ),
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=550,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        spacing=6,
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("Part information", size=30, weight="bold", color="black"),
                                            ft.Text("Dimensions", size=25),
                                            ft.Container(
                                            content=ft.Column(
                                                horizontal_alignment="center",
                                                controls=[
                                                    ft.Text("OD:", size=25, color="black"),
                                                    od_val
                                                ]
                                            )
                                        ),
                                        ft.Container(
                                            content=ft.Column(
                                                horizontal_alignment="center",
                                                controls=[
                                                    ft.Text("ID:", size=25, color="black"),
                                                    id_val
                                                ]
                                            )
                                        ),
                                        ft.Container(
                                            content=ft.Column(
                                                horizontal_alignment="center",
                                                controls=[
                                                    ft.Text("Thickness:", size=25, color="black"),
                                                    thick_val
                                                ]
                                            )
                                        ),
                                        ft.Container(
                                            content=ft.Column(
                                                horizontal_alignment="center",
                                                controls=[
                                                    ft.Text("Height:", size=25, color="black"),
                                                    height_val
                                                ]
                                            )
                                        ),
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=120,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                           ft.Text("NDE Specifications", size=20, weight="bold", color="black"),
                                            nde_val,
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=120,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                           ft.Text("Acceptance criteria", size=20, weight="bold", color="black"),
                                            accept_val,
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=120,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                           ft.Text("Surface roughness", size=20, weight="bold", color="black"),
                                            surface_val,
                                        ]
                                    )
                                ),
                                ft.Container(
                                    padding=10,
                                    height=100,
                                    width=400,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.ElevatedButton(
                                                content=ft.Text("Hacer Reporte",size=18),
                                                width=210,
                                                height=60,
                                                color="white",
                                                bgcolor=ft.colors.PURPLE,
                                                on_click= click
                                            )
                                        ]
                                    )
                                )
                            ]
                        )
                    ],
                )
            )
     
        page.update()
    
    
    
    def view_pop(view):
        page.views.pop()
        top_view=page.views[-1]
        page.go(top_view.route)

    page.on_route_change=route_chnage
    page.on_view_pop=view_pop
    page.go(page.route)


ft.app(target=main)