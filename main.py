import flet as ft 
from flet import*


    
    
def main(page:ft.Page):
    page.window_width=400
    page.window_height=730
    page.update()   
    

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
            [
                ft.Radio(label="VT", value="VT"),
                ft.Radio(label="UT", value="UT"),
                ft.Radio(label="X", value="X"),
            ]
        )
    )

    box_1 = ft.Checkbox(
        label="inspector 1 name"
    )
    box_2 = ft.Checkbox(
        label="inspector 2 name"
        )
    box_3 = ft.Checkbox(
        label="inspector 3 name"
        )
    box_4 = ft.Checkbox(
        label="inspector 4 name"
        )
    
    client_name = ft.Dropdown(
        border_radius=10,
        width=320,
        options=[
            ft.dropdown.Option("Client name 1"),
            ft.dropdown.Option("Client name 2"),
            ft.dropdown.Option("Client name 3"),
            ft.dropdown.Option("others")
        ]
    )

    plant_location = ft.Dropdown(
        border_radius=10,
        width=320,
        options=[
            ft.dropdown.Option("Location/address 1"),
            ft.dropdown.Option("Location/address 2"),
            ft.dropdown.Option("Loaction/address 3"),
            ft.dropdown.Option("others")
        ]
    )

    contact = ft.TextField(
        width=320,
        border_radius=10,
        label="contact",
    )


    txt_1 = ft.TextField(
        width=320,
        border_radius=10,
        label="Discription"

    ) 

    txt_2 = ft.TextField(
        width=320,
        border_radius=10,
        label="material"
        
    ) 

    txt_3 = ft.TextField(
        width=320,
        border_radius=10,
        label="Heat"
        
    )

    accept_val=ft.TextField(
        width=320,
        border_radius=10,
        label="Acceptance"
        
    )

    nde_val=ft.TextField(
        width=320,
        border_radius=10,
        label="NDE"
    )

    surface_val=ft.TextField(
        width=320,
        border_radius=10,
        label="Surface"
    )


    job = ft.TextField(
        text_align="center",
        value="0",
        width=320,
        height=60,
        prefix=ft.IconButton(ft.icons.ARROW_UPWARD),
        suffix=ft.IconButton(ft.icons.ARROW_DOWNWARD),
        border_radius=10
    )

    od_val = ft.TextField(
        text_align="center",
        value="0",
        width=320,
        height=60,
        prefix=ft.IconButton(ft.icons.ARROW_UPWARD),
        suffix=ft.IconButton(ft.icons.ARROW_DOWNWARD),
        border_radius=10
    )

    id_val = ft.TextField(
        text_align="center",
        value="0",
        width=320,
        height=60,
        prefix=ft.IconButton(ft.icons.ARROW_UPWARD),
        suffix=ft.IconButton(ft.icons.ARROW_DOWNWARD),
        border_radius=10
    )


    def route_chnage(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
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
                                                on_click=lambda _:page.go("/main")
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

        if page.route == "/main":
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
                                    height=190,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("tipo de preuba", size=20, weight="bold"),
                                            ft.Container(
                                                padding=10,
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
                                    height=225,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("inspector", size=20, weight="bold"),
                                            ft.Container(
                                            padding=10,
                                            content=ft.Column(
                                                controls=[
                                                    box_1,
                                                    box_2,
                                                    box_3,
                                                    box_4,
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
                                            ft.Text("Client Name", size=20, weight="bold"),
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
                                            ft.Text("Planta/plant", size=20),
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
                                           ft.Text("Contact name", size=20),
                                            contact,
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=500,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("Part Information", size=30, weight="bold"),
                                            ft.Text("Part description", size=20),
                                            txt_1,
                                            ft.Text("Material specs", size=20),
                                            txt_2,
                                            ft.Text("Heat", size=20),
                                            txt_3,
                                            ft.Text("Job qty", size=20),
                                            ft.Container(
                                            content=job
                                            ),
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=530,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("Part information", size=30, weight="bold"),
                                            ft.Container(
                                            content=ft.Column(
                                                horizontal_alignment="center",
                                                controls=[
                                                    ft.Text("OD:", size=25),
                                                    od_val
                                                ]
                                            )
                                        ),
                                        ft.Container(
                                            content=ft.Column(
                                                horizontal_alignment="center",
                                                controls=[
                                                    ft.Text("ID:", size=25),
                                                    id_val
                                                ]
                                            )
                                        ),
                                        ft.Container(
                                            content=ft.Column(
                                                horizontal_alignment="center",
                                                controls=[
                                                    ft.Text("Thickness:", size=25),
                                                    id_val
                                                ]
                                            )
                                        ),
                                        ft.Container(
                                            content=ft.Column(
                                                horizontal_alignment="center",
                                                controls=[
                                                    ft.Text("Height:", size=25),
                                                    id_val
                                                ]
                                            )
                                        ),
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=110,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                           ft.Text("NDE Specifications", size=20, weight="bold"),
                                            nde_val,
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=110,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                           ft.Text("Acceptance criteria", size=20, weight="bold"),
                                            accept_val,
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=115,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                           ft.Text("Surface roughness", size=20, weight="bold"),
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
                                                "print",
                                                width=200,
                                                height=60,
                                                color="white",
                                                bgcolor=ft.colors.PURPLE
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


if __name__ == "__main__":
    ft.app(target=main)