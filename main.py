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
client_name_var = ""
plant_name_var = ""
contact_name_var = ""
#plant_loc = ""

def main(page:ft.Page):
    api_url = os.getenv('api_url')

    names_width = 0

    test_sn_height = 450

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

    def nde_option_maker():
        client_data = { "name" : client_name.value }
        nde_json = requests.get(f"{api_url}all_client_nde", json=client_data)

        nde_list = json.loads(json.dumps(nde_json.json()))

        nde_list_parsed = []

        for nde in nde_list:
            if client_name.value != "Otro":
                try:
                    nde_list_parsed.append(str(nde["nde_spec"]))
                except TypeError:
                    print("No NDE Specification grabbed from DB")
    
        #plants_list_parsed.append("Otro")

        #print(plants_list_parsed)

        nde_val.options = list(map(ft.dropdown.Option, nde_list_parsed))

        try:
            nde_val.value = nde_list_parsed[0]
        except IndexError:
            nde_val.value = None

        page.update()

    def acabado_option_maker():
        client_data = { "name" : client_name.value }
        acabado_json = requests.get(f"{api_url}all_client_acabados", json=client_data)

        acabado_list = json.loads(json.dumps(acabado_json.json()))

        acabado_list_parsed = []

        for acab in acabado_list:
            if client_name.value != "Otro":
                try:
                    acabado_list_parsed.append(str(acab["acabado"]))
                except TypeError:
                    print("No NDE Specification grabbed from DB")
    
        #plants_list_parsed.append("Otro")

        #print(plants_list_parsed)

        acabado.options = list(map(ft.dropdown.Option, acabado_list_parsed))

        try:
            acabado.value = acabado_list_parsed[0]
        except IndexError:
            acabado.value = None

        page.update()

    def acc_crit_option_maker():
        data = { "client_name" : client_name.value,
                        "nde_spec" : nde_val.value }
        crit_json = requests.get(f"{api_url}all_nde_criteria", json=data)

        crit_list = json.loads(json.dumps(crit_json.json()))

        crit_list_parsed = []

        for criteria in crit_list:
            if client_name.value != "Otro":
                try:
                    crit_list_parsed.append(str(criteria["acceptance_criteria"]))
                except TypeError:
                    print("No criteria grabbed from DB")
    
        #plants_list_parsed.append("Otro")

        #print(plants_list_parsed)

        accept_val.options = list(map(ft.dropdown.Option, crit_list_parsed))

        try:
            accept_val.value = crit_list_parsed[0]
        except IndexError:
            accept_val.value = None

        page.update()

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

    clients_json = requests.get(f"{api_url}all_clients")
    clients_list = json.loads(json.dumps(clients_json.json()))

    clients_list_parsed = []

    for client in clients_list:
        clients_list_parsed.append(str(client["name"]))
    
    clients_list_parsed.append("Otro")

    #print(clients_list_parsed)

    plants_list = {}
    plants_list_parsed = []

    contacts_list = {}
    contacts_list_parsed = []

    def reload_clients():
        clients_json = requests.get(f"{api_url}all_clients")
        clients_list = json.loads(json.dumps(clients_json.json()))

        clients_list_parsed = []

        for client in clients_list:
            clients_list_parsed.append(str(client["name"]))

        clients_list_parsed.append("Otro")

        client_name.options = list(map(ft.dropdown.Option, clients_list_parsed))

        page.update()
    
    def reload_plants(client_data: dict):
        plants_json = requests.get(f"{api_url}all_client_plants/", json=client_data)
        nonlocal plants_list
        plants_list = {}
        plants_list = json.loads(json.dumps(plants_json.json()))

        nonlocal plants_list_parsed
        plants_list_parsed = []

        for plant in plants_list:
            if client_name.value != "Otro":
                try:
                    plants_list_parsed.append(str(plant["name"]))
                except TypeError:
                    print("No plant name grabbed from DB")
    
        plants_list_parsed.append("Otro")

        #print(plants_list_parsed)

        plant_name.options = list(map(ft.dropdown.Option, plants_list_parsed))

        page.update()

    def reload_contacts(client_data: dict):
        contacts_json = requests.get(f"{api_url}all_client_contacts/", json=client_data)
        nonlocal contacts_list
        contacts_list = {}
        contacts_list = json.loads(json.dumps(contacts_json.json()))

        nonlocal contacts_list_parsed
        contacts_list_parsed = []

        for contact in contacts_list:
            if client_name.value != "Otro":
                try:
                    contacts_list_parsed.append(str(contact["name"]))
                except TypeError:
                    print("No contact name grabbed from DB")
    
        contacts_list_parsed.append("Otro")

        contact_name.options = list(map(ft.dropdown.Option, contacts_list_parsed))

        page.update()

    def client_change(e):
        #print(e.control.value)

        reload_clients()

        if e.control.value == "Otro":
            other_client_name.visible = True
            other_plant_name.visible = True
            other_contact_name.visible = True
            plant_name.visible = False
            contact_name.visible = False
            send_all_btn.visible = True
            e.page.update()
        else:
            other_client_name.visible = False
            other_plant_name.visible = False
            other_contact_name.visible = False
            plant_name.visible = True
            contact_name.visible = True
            send_all_btn.visible = False

            e.page.update()

        client_data = {
            "name" : client_name.value
        }

        #plant reload section

        reload_plants(client_data)

        #contact reload section

        reload_contacts(client_data)

        plant_name.value = plants_list_parsed[0]

        contact_name.value = contacts_list_parsed[0]

        nde_option_maker()
        acc_crit_option_maker()
        acabado_option_maker()

        e.page.update()
    
    client_name = ft.Dropdown(
        label="Nombre del Cliente",
        bgcolor="white",
        border_radius=10,
        width=320,
        color="black",
        options=list(map(ft.dropdown.Option, clients_list_parsed)),
        on_change=client_change
    )

    other_client_name = ft.TextField(
        label="Otro Cliente",
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320,
        visible=False
    )

    #TODO añadir un boton para cada "OTRO" para que pueda agregar plantas y contactos a la base de datos

    def plant_change(e):
        print(e.control.value)
        if e.control.value == "Otro":
            other_plant_name.visible = True
            other_plant_button.visible = True
            e.page.update()
        else:
            other_plant_name.visible = False
            other_plant_button.visible = False
            e.page.update()

    def send_plant(e):
        if other_plant_name.value and client_name.value:

            print(other_plant_name.value)
            print(client_name.value)
            
            warning_text.visible = False

            plant_data = {
                "name" : other_plant_name.value,
                "client_name" : client_name.value
            }

            add_plant_request = requests.post(url=f"{api_url}add_plant/", json=plant_data)

            plant_name.value = other_plant_name.value

            other_plant_name.value = None

            other_plant_name.visible = False

            other_plant_button.visible = False

            page.update()

        else:
            warning_text.visible = True
            warning_text.value = "Faltó de rellenar algún dato"
            page.update()

        client_data = {
            "name" : client_name.value
        }
        
        reload_clients()
        reload_plants(client_data)

    def send_contact(e):
        if other_contact_name.value and client_name.value:

            print(other_contact_name.value)
            print(client_name.value)
            
            warning_text.visible = False

            contact_data = {
                "name" : other_contact_name.value,
                "client_name" : client_name.value
            }

            add_contact_request = requests.post(url=f"{api_url}add_contact/", json=contact_data)

            contact_name.value = other_contact_name.value

            other_contact_name.value = None

            other_contact_name.visible = False

            other_contact_button.visible = False

            page.update()

        else:
            warning_text.visible = True
            warning_text.value = "Faltó de rellenar algún dato"
            page.update()

        client_data = {
            "name" : client_name.value
        }
        
        reload_clients()
        reload_contacts(client_data)



    plant_name = ft.Dropdown(
        label="Nombre de la planta",
        bgcolor="white",
        border_radius=10,
        width=320,
        color="black",
        #options=list(map(ft.dropdown.Option, plants_list_parsed)),
        on_change=plant_change
    )

    other_plant_name = ft.TextField(
        label="Otra Planta",
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320,
        visible=False
    )

    other_plant_button = ft.ElevatedButton(
        text="Guardar Planta",
        color="white",
        bgcolor=ft.colors.PURPLE,
        visible=False,
        on_click=send_plant
    )
    
    def contact_change(e):
        print(e.control.value)
        if e.control.value == "Otro":
            other_contact_name.visible = True
            other_contact_button.visible = True
            e.page.update()
        else:
            other_contact_name.visible = False
            other_contact_button.visible = False
            e.page.update()

    contact_name = ft.Dropdown(
        label="Nombre del contacto",
        bgcolor="white",
        border_radius=10,
        width=320,
        color="black",
        #options=list(map(ft.dropdown.Option, plants_list_parsed)),
        on_change=contact_change
    )

    other_contact_name = ft.TextField(
        label="Otro Contacto",
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        width=320,
        visible=False
    )

    other_contact_button = ft.ElevatedButton(
        text="Guardar Contacto",
        color="white",
        bgcolor=ft.colors.PURPLE,
        visible=False,
        on_click=send_contact
    )

    warning_text =  ft.Text(visible=False)

    # ft.TextField(
    #     label="Nombre de cliente", 
    #     border_radius=10,
    #     keyboard_type=ft.KeyboardType.TEXT,
    #     width=320,
    #     #on_change=lambda _:Text_Grabber(var=client_name_var)
    # )
    
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

    # plant_location = None #ft.TextField(
    #     label="Ubicación de la Planta", 
    #     border_radius=10,
    #     keyboard_type=ft.KeyboardType.TEXT,
    #     width=320,
    #     #on_change=lambda _:Text_Grabber(var=client_name_var)
    # )
    
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

    #TODO hacer funciones para enviar nuevo cliente, planta y contacto respectvamente
    def send_all(e):
        # print(other_client_name.value + other_contact_name.value + other_plant_name.value)
        if other_client_name.value and other_contact_name.value and other_plant_name.value:
            print("text")
            warning_text.visible = False
            client_data = {
                "name" : other_client_name.value
            }
            plant_data = {
                "name" : other_plant_name.value,
                "client_name" : other_client_name.value
            }
            contact_data = {
                "name" : other_contact_name.value,
                "client_name" : other_client_name.value
            }

            add_client_request = requests.post(url=f"{api_url}add_client/", json=client_data)

            add_plant_request = requests.post(url=f"{api_url}add_plant/", json=plant_data)

            add_contact_request = requests.post(url=f"{api_url}add_contact/", json=contact_data)

            other_client_name.value = ""
            other_plant_name.value = ""
            other_contact_name.value = ""

            page.update()

            # print(add_client_request)
            # print(add_plant_request)
            # print(add_contact_request)

        else:
            warning_text.visible = True
            warning_text.value = "Faltó de rellenar algún dato"
            page.update()
        
        reload_clients()

    send_all_btn = ft.ElevatedButton(
        text="Guardar Cliente",
        color="white",
        bgcolor=ft.colors.PURPLE,
        visible=False,
        on_click=send_all
    )

    def if_int(x: list):
        for y in x:
            try:
                z = int(y)
                print(z)
                if type(z) is int:
                    return z
                else:
                    print("not int")
            except ValueError:
                print("Cant be converted into Int")

    async def click(e):
    #     print(box_group.value, inspectors_list)
    #     print(f"you click{job.value}")
        #hacer una función para que se guarde el reporte en la base de datos y se haga un numero de reporte
        #url = f"{api_url}?test={box_group.value}&report_num={box_group.value}-R-{year}-234&client_name={client_name_var}&plant={plant_name_var}&contact_name={contact.value}&part_desc={Description.value}&material={material.value}&heat={heat.value}&j_order={job_order.value}&j_qty={job.value}&od={od_val.value}&id={id_val.value}&width={thick_val.value}&height={height_val.value}&NDE={nde_val.value}&crit_accept={accept_val.value}&rough={surface_val.value}&uti_sn={uti_sn.value}&sn1={test_sn1.value}&d_cal={distance.value}&sens_block={sensitivity.value}&notch={notch.value}&rec_lvl={record.value}&ax_scanning={axial_x.value}&circ_ax_scanning={circumferental_x.value}&method={inspection.value}&coupling={coupling.value}&stage={inspector_s.value}&remarks={textarea.value}&insp_name={inspectors_list[0]}&ndt_act={ndt_act.value}"
        #print(url)

        data = {
            "test":box_group.value,
            "client_name":client_name.value,
            "plant":plant_name.value,
            "contact_name":contact_name.value,
            "part_desc":Description.value,
            "material":material.value,
            "heat":heat.value,
            "j_order":job_order.value,
            "j_qty":job_qty_txtbox.value,
            "od":float(od_txtbox.value),
            "id":float(id_txtbox.value),
            "width":float(thick_txtbox.value),
            "height":float(height_txtbox.value),
            "NDE":nde_val.value,
            "crit_accept":accept_val.value,
            #rehacer la parte de surface roughness para agregar el acabado superficial
            "rough":f"{acabado.value}, (≤{surface_val.value} {measure.value})",
            "uti_sn":int(uti_sn.value.split()[1]),
            "sn1": if_int(test_sn1.value.split()),
            "d_cal":distance.value,
            "sens_block":sensitivity.value,
            "notch":notch.value,
            "rec_lvl":record.value,
            "ax_scanning":axial_x.value,
            "circ_ax_scanning":circumferental_x.value,
            "method":inspection.value,
            "coupling":coupling.value,
            "stage":inspector_s.value,
            "remarks":textarea.value,
            "insp_name":inspectors_list[0],
            "ndt_act":ndt_act.value
        }

        if check.value:
            data["acc_sn"] = sn.value
        else:
            data["rej_sn"] = sn.value

        if test_sn2.value  != '':
            try:
                data["sn2"] = int(test_sn2.value)
            except TypeError:
                pass

        elif test_sn3.value != '':
            try:
                data["sn3"] = int(test_sn3.value)
            except TypeError:
                pass

        elif test_sn4.value != '':
            try:
                data["sn4"] = int(test_sn4.value)
            except TypeError:
                pass

        elif test_sn5.value != '':
            try:
                data["sn5"] = int(test_sn5.value)
            except TypeError:
                pass

        pdfurldownload = str(downloads_path) + "\\" + str(box_group.value) + "-R-" + str(year) + ".pdf"

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            #await page.goto(url)
            html = requests.get(api_url, json=data)
            no_new_line = html.content.decode("utf-8")
            await page.set_content(no_new_line)
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

    # contact = ft.TextField(
    #     width=320,
    #     border_radius=10,
    #     label="contact",
    #     color="black",
    #     border_color="black",
    #     label_style=ft.TextStyle(color="black"),
    #     border_width=1
        
    # )


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

    accept_val=ft.Dropdown(
        width=320,
        border_radius=10,
        label="Acceptance Criteria",
        color="black",
        label_style=ft.TextStyle(color="black"),
        border_color="black",
        border_width=1
        
    )

    nde_val=ft.Dropdown(
        width=320,
        border_radius=10,
        label="NDE",
        color="black",
        label_style=ft.TextStyle(color="black"),
        border_color="black",
        border_width=1,
        bgcolor="white",
        on_change=lambda _:acc_crit_option_maker()
    )

    acabado = ft.Dropdown(
        width=200,
        border_radius=10,
        label="Acabado Superficial",
        color="black",
        label_style=ft.TextStyle(color="black"),
        border_color="black",
        text_size=15,
        border_width=1
    )

    surface_val = ft.TextField(
        width=80,
        border_radius=10,
        label="Rough",
        color="black",
        label_style=ft.TextStyle(color="black"),
        border_color="black",
        input_filter=ft.NumbersOnlyInputFilter(),
        border_width=1,
        text_size=15,
        value=250
    )

    measure = ft.TextField(
        width=80,
        border_radius=10,
        label="Measure",
        color="black",
        label_style=ft.TextStyle(color="black"),
        border_color="black",
        border_width=1,
        text_size=15,
    )

    def uti_list_maker():
        uti_json = requests.get(f"{api_url}all_uti")
        uti_list = json.loads(json.dumps(uti_json.json()))

        uti_list_parsed = []

        for uti in uti_list:
            uti_list_parsed.append(f"{uti["model"]} {uti["sn"]}")


        return uti_list_parsed

    uti_list_parsed = uti_list_maker()
    
    def uti_change(e):

        sn = e.control.value.split()[1]

        UTI = requests.get(f"{api_url}uti_by_sn", json={"sn": sn})

        uti_dict = json.loads(json.dumps(UTI.json()))

        print(uti_dict)

        UTI_data.visible = True

        UTI_data.value = f"Brand: {uti_dict["brand"]}  Model: {uti_dict["model"]} \n SN: {uti_dict["sn"]} \n Calibration Date: {uti_dict["calibration_date"]} \n Calibration Due Date: {uti_dict["calibration_due_date"]}"

        page.update()

    uti_sn = ft.Dropdown(
        label="Modelo y N° de Serie",
        bgcolor="white",
        border_radius=10,
        width=320,
        color="black",
        options=list(map(ft.dropdown.Option, uti_list_parsed)),
        on_change=uti_change
    )

    UTI_data = ft.Text(
        visible=False,
        text_align= ft.TextAlign.CENTER
    )

    # uti_sn = ft.TextField(
    #     label="UT Instrument Serial Number", 
    #     border_radius=10,
    #     keyboard_type=ft.KeyboardType.TEXT,
    #     width=320
    # )

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
        keyboard_type=ft.KeyboardType.NUMBER,
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

    #aqui va la funcion de test sn list

    def test_sn_list_maker():
        test_json = requests.get(f"{api_url}all_setups")
        test_list = json.loads(json.dumps(test_json.json()))

        test_list_parsed = []

        for test in test_list:
            test_list_parsed.append(f"{test["brand"]} {test["model"]} {test["sn"]}")


        return test_list_parsed

    test_list_parsed = test_sn_list_maker()

    def test_change(e):
        pass

    test_sn1 = ft.Dropdown(
        label="Test Serial Number 1",
        bgcolor="white",
        border_radius=10,
        width=320,
        color="black",
        options=list(map(ft.dropdown.Option, test_list_parsed)),
        on_change=test_change
    )

    test_sn2 = ft.Dropdown(
        label="Test Serial Number 2",
        bgcolor="white",
        border_radius=10,
        width=320,
        color="black",
        options=list(map(ft.dropdown.Option, test_list_parsed)),
        visible=False,
        on_change=test_change
    )

    test_sn3 = ft.Dropdown(
        label="Test Serial Number 3",
        bgcolor="white",
        border_radius=10,
        width=320,
        color="black",
        options=list(map(ft.dropdown.Option, test_list_parsed)),
        visible=False,
        on_change=test_change
    )

    test_sn4 = ft.Dropdown(
        label="Test Serial Number 4",
        bgcolor="white",
        border_radius=10,
        width=320,
        color="black",
        options=list(map(ft.dropdown.Option, test_list_parsed)),
        visible=False,
        on_change=test_change
    )

    test_sn5 = ft.Dropdown(
        label="Test Serial Number 5",
        bgcolor="white",
        border_radius=10,
        width=320,
        color="black",
        options=list(map(ft.dropdown.Option, test_list_parsed)),
        visible=False,
        on_change=test_change
    )

    # test_sn1 = ft.TextField(
    #     label="Test Serial Number 1", 
    #     border_radius=10,
    #     keyboard_type=ft.KeyboardType.TEXT,
    #     width=320,
    # )

    # test_sn2 = ft.TextField(
    #     label="Test Serial Number 2", 
    #     border_radius=10,
    #     keyboard_type=ft.KeyboardType.TEXT,
    #     width=320,
    #     visible=False
    # )

    # test_sn3 = ft.TextField(
    #     label="Test Serial Number 3", 
    #     border_radius=10,
    #     keyboard_type=ft.KeyboardType.TEXT,
    #     width=320,
    #     visible=False
    # )

    # test_sn4 = ft.TextField(
    #     label="Test Serial Number 4", 
    #     border_radius=10,
    #     keyboard_type=ft.KeyboardType.TEXT,
    #     width=320,
    #     visible=False
    # )

    # test_sn5 = ft.TextField(
    #     label="Test Serial Number 5", 
    #     border_radius=10,
    #     keyboard_type=ft.KeyboardType.TEXT,
    #     width=320,
    #     visible=False
    # )

    textarea_counter = 1

    def add_textarea(e):
        nonlocal textarea_counter, test_sn_height
        
        if textarea_counter >= 1 and textarea_counter <= 5:
            textarea_counter = textarea_counter + 1
            if textarea_counter == 2:
                test_sn2.visible = True
            elif textarea_counter == 3:
                test_sn3.visible = True
            elif textarea_counter == 4:
                test_sn4.visible = True
            elif textarea_counter == 5:
                test_sn5.visible = True



            e.page.update()
        elif textarea_counter > 5:
            textarea_counter = textarea_counter - 1
        elif textarea_counter < 1:
            textarea_counter = textarea_counter + 1
        else:
            print("error +")

    def del_textarea(e):
        nonlocal textarea_counter, test_sn_height
        if textarea_counter >= 1 and textarea_counter <= 5:
            if textarea_counter == 2:
                test_sn2.visible = False
            elif textarea_counter == 3:
                test_sn3.visible = False
            elif textarea_counter == 4:
                test_sn4.visible = False
            elif textarea_counter == 5:
                test_sn5.visible = False
            textarea_counter = textarea_counter - 1

            e.page.update()
        elif textarea_counter < 1:
            textarea_counter = textarea_counter + 1
        elif textarea_counter > 5:
            textarea_counter = textarea_counter - 1
        else:
            print("error -")


    add_btn = ft.IconButton(
        icon= ft.icons.ADD,
        on_click=add_textarea
    )
    
    del_btn = ft.IconButton(
        icon= ft.icons.REMOVE_ROUNDED,
        on_click=del_textarea
    )
    


    # job = Stepper_qty()
    # od_val = Stepper()
    # id_val = Stepper()
    # thick_val = Stepper()
    # height_val = Stepper()

    job_qty_txtbox = ft.TextField(
        text_align="center",
        keyboard_type=ft.KeyboardType.NUMBER,
        label="qty",
        width=150,
        height=60,
        border_radius=10,
        show_cursor=False,
        color="black",
        input_filter=ft.NumbersOnlyInputFilter()
    )

    def od_validation(e):

        if  e.control.value == '' or float(e.control.value) <= 0:
            part_info_text.visible = True
            part_info_text.value = "El valor Tiene que ser mayor a 0"
            page.update()
        else:
            part_info_text.value = ""
            part_info_text.visible = False
            page.update()

    def id_validation(e):

        if float(e.control.value) >= float(od_txtbox.value):
            part_info_text.visible = True
            part_info_text.value = "El valor de id tiene que ser menor a od"
            page.update()
        elif float(e.control.value) <0:
            part_info_text.visible = True
            part_info_text.value = "El valor de id tiene que ser mayor a cero"
            page.update()
        else:
            part_info_text.value = ""
            part_info_text.visible = False
            page.update()


    def change_measure(e):

        if e.control.value == False:
            inch_or_mm.label = "Inch"
            page.update()
        else:
            inch_or_mm.label = "Milimeter"
            page.update()

    def thick_validation(e):
        if float(e.control.value) <= 0:
            part_info_text.visible = True
            part_info_text.value = "El valor de Thickness tiene que ser mayor a cero"
            page.update()
        else:
            part_info_text.value = ""
            part_info_text.visible = False
            page.update()
        
    def height_validation(e):
        if e.control.value == "" or float(e.control.value) <= 0:
            part_info_text.visible = True
            part_info_text.value = "El valor de Height tiene que ser mayor a cero"
            page.update()
        else:
            part_info_text.value = ""
            part_info_text.visible = False
            page.update()
        
    inch_or_mm = ft.Switch(
        label="Inch",
        value=False,
        on_change=change_measure
    )

    od_txtbox = ft.TextField(
        text_align="center",
        keyboard_type=ft.KeyboardType.NUMBER,
        label="OD",
        width=150,
        height=60,
        border_radius=10,
        show_cursor=False,
        color="black",
        input_filter=ft.InputFilter(allow=True, regex_string=r"^\d*\.?\d*$", replacement_string=""),
        on_change=od_validation
    )

    id_txtbox = ft.TextField(
        text_align="center",
        keyboard_type=ft.KeyboardType.NUMBER,
        label="ID",
        width=150,
        height=60,
        border_radius=10,
        show_cursor=False,
        color="black",
        input_filter=ft.InputFilter(allow=True, regex_string=r"^\d*\.?\d*$", replacement_string=""),
        on_change=id_validation
    )

    height_txtbox = ft.TextField(
        text_align="center",
        keyboard_type=ft.KeyboardType.NUMBER,
        label="Height",
        width=150,
        height=60,
        border_radius=10,
        show_cursor=False,
        color="black",
        input_filter=ft.InputFilter(allow=True, regex_string=r"^\d*\.?\d*$", replacement_string=""),
        on_change=height_validation
    )

    thick_txtbox = ft.TextField(
        text_align="center",
        keyboard_type=ft.KeyboardType.NUMBER,
        label="Thickness",
        width=150,
        height=60,
        border_radius=10,
        show_cursor=False,
        color="black",
        input_filter=ft.InputFilter(allow=True, regex_string=r"^\d*\.?\d*$", replacement_string=""),
        on_change=thick_validation
    )

    part_info_text = ft.Text(value="", visible=False)

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
                                            ft.Text("Tipo de Prueba", size=20, weight="bold", color="black"),
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
                                    height=650,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("Client Name", size=20, weight="bold", color="black"),
                                            client_name,
                                            other_client_name,
                                            ft.Container(height=50),
                                            plant_name,
                                            other_plant_name,
                                            ft.Container(height=10),
                                            other_plant_button,
                                            ft.Container(height=50),
                                            contact_name,
                                            other_contact_name,
                                            ft.Container(height=10),
                                            other_contact_button,
                                            ft.Container(height=50),
                                            warning_text,
                                            send_all_btn
                                        ]
                                    )
                                ),
                                # ft.Container(
                                #     width=400,
                                #     height=120,
                                #     padding=ft.padding.only(top=10),
                                #     bgcolor=ft.colors.WHITE,
                                #     content=ft.Column(
                                #         horizontal_alignment="center",
                                #         controls=[
                                #             ft.Text("Planta/plant", size=20, color="black"),
                                #             plant_location,
                                #         ]
                                #     )
                                # ),
                                # ft.Container(
                                #     width=400,
                                #     height=120,
                                #     padding=ft.padding.only(top=10),
                                #     bgcolor=ft.colors.WHITE,
                                #     content=ft.Column(
                                #         horizontal_alignment="center",
                                #         controls=[
                                #             ft.Text("Contact name", size=20, color="black"),
                                #             contact,
                                #         ]
                                #     )
                                # ),
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
                                            ft.Text("Material Spec", size=20, color="black"),
                                            material,
                                            ft.Text("Heat", size=20, color="black"),
                                            heat,
                                            ft.Text("Job Order", size=20, color="black"),
                                            job_order,
                                            ft.Text("Job qty", size=20, color="black"),
                                            job_qty_txtbox

                                            # ft.Container(
                                            # content=job
                                            # ),
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=700,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        spacing=6,
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("Part information", size=30, weight="bold", color="black"),
                                            ft.Text("Dimensions", size=25),
                                            inch_or_mm,
                                            ft.Container(
                                            content=ft.Column(
                                                horizontal_alignment="center",
                                                controls=[
                                                    ft.Text("OD:", size=25, color="black"),
                                                    od_txtbox
                                                ]
                                            )
                                        ),
                                        ft.Container(
                                            content=ft.Column(
                                                horizontal_alignment="center",
                                                controls=[
                                                    ft.Text("ID:", size=25, color="black"),
                                                    id_txtbox
                                                ]
                                            )
                                        ),
                                        ft.Container(
                                            content=ft.Column(
                                                horizontal_alignment="center",
                                                controls=[
                                                    ft.Text("Thickness:", size=25, color="black"),
                                                    thick_txtbox
                                                ]
                                            )
                                        ),
                                        ft.Container(
                                            content=ft.Column(
                                                horizontal_alignment="center",
                                                controls=[
                                                    ft.Text("Height:", size=25, color="black"),
                                                    height_txtbox
                                                ]
                                            )
                                        ),
                                        part_info_text
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
                                           ft.Text("NDE Specification", size=20, weight="bold", color="black"),
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
                                           ft.Row(
                                            controls=[acabado, surface_val, measure],
                                            alignment="center"
                                           )
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=315,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("UT Instrument", size=25, weight="bold", color="black"),
                                            ft.Text("Serial Number", size=20, ),
                                            uti_sn, #thiss
                                            UTI_data
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=test_sn_height + 40,
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
                                            test_sn5,
                                            ft.Row(
                                                alignment=MainAxisAlignment.END,
                                                controls=[
                                                    del_btn,
                                                    add_btn
                                                ]
                                            )
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
                                    #padding=ft.padding.only(top=10),
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




