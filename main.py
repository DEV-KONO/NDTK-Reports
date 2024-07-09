import flet as ft 
from flet import*
from utils.int_button import Stepper, Stepper_qty
from dotenv import load_dotenv
from pathlib import Path
from playwright.async_api import async_playwright
import os
import json
import requests
import datetime
import pdfkit
import asyncio

load_dotenv()    

year = datetime.datetime.now().year
downloads_path = str(Path.home() / "Downloads")


inspectors_list = []
#test = ""
#client_name_var = ""
#plant_loc = ""

def main(page:ft.Page):
    api_url = os.getenv('api_url')
    names_width = 0

    test_sn_height = 165

    page.window.width=400
    page.window.height=730
    page.adaptive=True
    theme=ft.Theme()
    theme.page_transitions.windows=ft.PageTransitionTheme.NONE
    theme.page_transitions.android=ft.PageTransitionTheme.NONE
    page.theme=theme
    page.theme_mode=ft.ThemeMode.LIGHT
    page.window.always_on_top=True
    page.update()   

    # def test_grabber(e):
    #     global test
    #     test =  e.control.value
    #     page.update()
    #     print(f"Test:{test}")

    def ins_grabber(e):
        global inspectors_list

        if e.control.value:
            inspectors_list.append(e.control.label)
        else:
            inspectors_list.remove(e.control.label)
        page.update()
        print(inspectors_list)

    # def Text_Grabber(e, var):
    #     var = e.control.value
    #     page.update()
    #     print(var)

    # def cn_grabber(e):
    #     global client_name_var
    #     client_name_var = e.control.value
    #     page.update()
    #     print(client_name_var)
    
    # def pl_grabber(e):
    #     global plant_loc
    #     plant_loc = e.control.value
    #     page.update()
    #     print(plant_loc)

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
                ft.Radio(label="PT", value="PT", label_style=ft.TextStyle(color="black"),),
                ft.Radio(label="ET", value="ET", label_style=ft.TextStyle(color="black"),),
                ft.Radio(label="MT", value="MT", label_style=ft.TextStyle(color="black"),),
            ]
        )
    )

    response = requests.get(f"{api_url}all_inspectors")

    inspectors = json.loads(json.dumps(response.json()))

    # {"id": 1, "name": "abdul"},
    # {"id": 2, "name": "sam"},
    # {"id": 3, "name": "nana"},
    # {"id": 4, "name": "zahra"},
    # {"id": 5, "name": "ahra"},

    in_name = []       

    for inspector in inspectors:
        names_width += 75
        in_name.append(
            ft.Checkbox(
                label=inspector["name"],
                label_style=ft.TextStyle(color="black"),
                on_change=ins_grabber
            )
        )
        
        

    
    client_name = ft.TextField(
        label="Nombre de cliente", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320,
        #on_change=lambda _:Text_Grabber(var=client_name_var)
    )
    
    # ft.Dropdown(
    #     bgcolor="white",
    #     border_radius=10,
    #     width=320,
    #     color="black",
    #     options=[
    #         ft.dropdown.Option("Client name 1"),
    #         ft.dropdown.Option("Client name 2"),
    #         ft.dropdown.Option("Client name 3"),
    #         ft.dropdown.Option("others")
    #     ]
    # )

    plant_location = ft.TextField(
        label="Ubicación de la Planta", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320,
        #on_change=lambda _:Text_Grabber(var=client_name_var)
    )
    
    # ft.Dropdown(
    #     label="Plant Location", 
    #     border_radius=10,
    #     color="black",
    #     width=320,
    #     options=[
    #         ft.dropdown.Option("Location/address 1"),
    #         ft.dropdown.Option("Location/address 2"),
    #         ft.dropdown.Option("Loaction/address 3"),
    #         ft.dropdown.Option("others")
    #     ]
    # )

    async def click(e):
        print(box_group.value, inspectors_list)
        print(f"you click{job.value}")
        #hacer una función para que se guarde el reporte en la base de datos y se haga un numero de reporte
        url = f"{api_url}?test={box_group.value}&report_num={box_group.value}-R-{year}-234&client_name={client_name.value}&plant={plant_location.value}&contact_name={contact.value}&part_desc={Description.value}&material={material.value}&heat={heat.value}&j_order={job_order.value}&j_qty={job.value}&od={od_val.value}&id={id_val.value}&width={thick_val.value}&height={height_val.value}&NDE={nde_val.value}&crit_accept={accept_val.value}&rough={surface_val.value}&uti_sn={uti_sn.value}&sn1={test_sn.value}&d_cal={distance.value}&sens_block={sensitivity.value}&notch={notch.value}&rec_lvl={record.value}&ax_scanning={axial_x.value}&circ_ax_scanning={circumferental_x.value}&method={inspection.value}&coupling={coupling.value}&stage={inspector_s.value}&remarks={textarea.value}&insp_name={inspectors_list[0]}&ndt_act={ndt_act.value}"
        print(url)
        if check.value:
            url = url + f"&acc_sn={sn.value}"
        else:
            url = url + f"&rej_sn={sn.value}"

        pdfurldownload = str(downloads_path) + "\\" + str(box_group.value) + "-R-" + str(year) + ".pdf"

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            await page.pdf(path=pdfurldownload)
            await browser.close()
        
        #print(pdfurldownload)
        
        #pdfkit.from_url(url, pdfurldownload, configuration=config)
        # response = response.get(url)

    ndt_act = ft.TextField(
        width=320,
        border_radius=10,
        label="NDT Activities",
        color="black",
        border_color="black",
        label_style=ft.TextStyle(color="black"),
        border_width=1
    )

    check = ft.CupertinoCheckbox(
        label="Accept?"
    )

    contact = ft.TextField(
        width=320,
        border_radius=10,
        label="contact",
        color="black",
        border_color="black",
        label_style=ft.TextStyle(color="black"),
        border_width=1
        
    )


    Description = ft.TextField(
        width=320,
        border_radius=10,
        label="Description",
        color="black",
        label_style=ft.TextStyle(color="black"),
        border_color="black",
        border_width=1

    ) 

    material = ft.TextField(
        width=320,
        border_radius=10,
        label="material",
        color="black",
        label_style=ft.TextStyle(color="black"),
        border_color="black",
        border_width=1
        
    ) 

    heat = ft.TextField(
        width=320,
        border_radius=10,
        label="Heat",
        color="black",
        label_style=ft.TextStyle(color="black"),
        border_color="black",
        border_width=1
        
    )

    job_order = ft.TextField(
        width=320,
        border_radius=10,
        label="Job Order",
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

    uti_sn = ft.TextField(
        label="UT Instrument Serial Number", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320
    )

    distance = ft.TextField(
        label="Distance", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320
    )

    sensitivity = ft.TextField(
        label="sensitivity", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320
    )

    notch = ft.TextField(
        label="notch", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320
    )

    record = ft.TextField(
        label="recording", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320
    )

    axial_x = ft.TextField(
        label="axial scanning", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320
    )

    circumferental_x = ft.TextField(
        label="circumferental", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320
    )

    inspection = ft.TextField(
        label="inspection method", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320
    )

    coupling = ft.TextField(
        label="coupling agent", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320
    )

    inspector_s = ft.TextField(
        label="Inspection stage", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320
    )

    sn = ft.TextField(
        label="s/n", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320
    )

    textarea = ft.TextField(
        width=300,
        height=350,
        multiline=True,
        min_lines=6,
        max_lines=6,
        border_radius=10
    )

    test_sn1 = ft.TextField(
        label="Test Serial Number 1", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320,
    )

    test_sn2 = ft.TextField(
        label="Test Serial Number 2", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320,
        visible=False
    )

    test_sn3 = ft.TextField(
        label="Test Serial Number 3", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320,
        visible=False
    )

    test_sn4 = ft.TextField(
        label="Test Serial Number 4", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320,
        visible=False
    )

    test_sn5 = ft.TextField(
        label="Test Serial Number 5", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320,
        visible=False
    )

    textarea_counter = 1

    def add_textarea(e, textarea_counter, test_sn_height):
        if textarea_counter > 0 and textarea_counter < 6:
            textarea_counter += 1
            if textarea_counter == 2:
                test_sn2.visible == True
            elif textarea_counter == 3:
                test_sn3.visible == True
            elif textarea_counter == 4:
                test_sn4.visible == True
            elif textarea_counter == 5:
                test_sn5.visible == True

            test_sn_height += 200

            e.page.update()
        elif textarea_counter > 5:
            textarea_counter -= 1
        else:
            print("error")

    def del_textarea(e, textarea_counter, test_sn_height):
        if textarea_counter > 0 and textarea_counter < 6:
            if textarea_counter == 2:
                test_sn2.visible == False
            elif textarea_counter == 3:
                test_sn3.visible == False
            elif textarea_counter == 4:
                test_sn4.visible == False
            elif textarea_counter == 5:
                test_sn5.visible == False
            textarea_counter -= 1

            test_sn_height -= 200

            e.page.update()
        elif textarea_counter < 1:
            textarea_counter += 1
        else:
            print("error")


    add_btn = ft.IconButton(
        icon= ft.icons.ADD,
        on_click=lambda _:add_textarea(e, textarea_counter, test_sn_height)
    )
    
    del_btn = ft.IconButton(
        icon= ft.icons.REMOVE_ROUNDED,
        on_click=lambda _:del_textarea(e, textarea_counter, test_sn_height)
    )
    


    job = Stepper_qty()
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
                                    height=300,
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
                                    height=names_width + 50,
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
                                    height=600,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("Part Information", size=30, weight="bold", color="black"),
                                            ft.Text("Part description", size=20, color="black"),
                                            Description,
                                            ft.Text("Material specs", size=20, color="black"),
                                            material,
                                            ft.Text("Heat", size=20, color="black"),
                                            heat,
                                            ft.Text("Job Order", size=20, color="black"),
                                            job_order,
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
                                    width=400,
                                    height=165,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("UT Instrument", size=25, weight="bold", color="black"),
                                            ft.Text("Serial Number", size=20, ),
                                            uti_sn, #thiss
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=test_sn_height,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("Test calibration setup", text_align="center", size=25, weight="bold", color="black"),
                                            ft.Text("Serial Number", size=20),
                                            test_sn1,
                                            test_sn2,
                                            test_sn3,
                                            test_sn4,
                                            test_sn5 
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=165,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            del_btn,
                                            add_btn
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=490,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("Calibration blocks", text_align="center", size=25, weight="bold", color="black"),
                                            ft.Text("Distance calibration angle verification", size=20, text_align="center"),
                                            distance,
                                            ft.Text("Sensitivity Block", size=20),
                                            sensitivity,
                                            ft.Text("Notch Depth", size=20),
                                            notch,
                                            ft.Text("Recording Level", size=20),
                                            record, 
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=270,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("Scanning Direction", text_align="center", size=25, weight="bold", color="black"),
                                            ft.Text("Axial scanning", size=20, text_align="center"),
                                            axial_x,
                                            ft.Text("Circumferential/ Axial Scanning", size=20),
                                            circumferental_x,
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=370,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("Inspection Information", text_align="center", size=25, weight="bold", color="black"),
                                            ft.Text("Inspection Method", size=20, text_align="center"),
                                            inspection,
                                            ft.Text("coupling agent", size=20, text_align="center"),
                                            coupling,
                                            ft.Text("Inspection Stage", size=20),
                                            inspector_s,
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=750,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        alignment="center",
                                        controls=[
                                            ft.Text("Inspection Results", text_align="center", size=25, weight="bold", color="black"),
                                            ft.Text("SN", size=20),
                                            sn,
                                            ft.Container(
                                                padding=10,
                                                content=check,
                                            ),
                                            ft.Text("Remarks", size=20),
                                            textarea,
                                            ft.Text("NDT Activities", size=20),
                                            ndt_act
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