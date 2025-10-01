from importlib.machinery import OPTIMIZED_BYTECODE_SUFFIXES
import string
from dotenv import load_dotenv
from flet import*
from pathlib import Path
from playwright.async_api import async_playwright
from admin_App import admin_page
import flet as ft 
import os
import requests
import datetime

year = datetime.datetime.now().year
downloads_path = str(Path.home() / "Downloads")


#test = ""
client_name_var = ""
plant_name_var = ""
contact_name_var = ""
#plant_loc = ""

# load_dotenv(".api.env")

def main(page:ft.Page):
    api_url = "https://ndtk-reports.onrender.com/" #os.getenv("api_url")

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
    inspectors_list = []

    # def ins_grabber(e):
    #     nonlocal inspectors_list

    #     if e.control.value:
    #         inspectors_list.append(e.control.label)
    #     else:
    #         inspectors_list.remove(e.control.label)
    #     page.update()
    #     # print(inspectors_list)

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


    # {"id": 1, "name": "abdul"},
    # {"id": 2, "name": "sam"},
    # {"id": 3, "name": "nana"},
    # {"id": 4, "name": "zahra"},
    # {"id": 5, "name": "ahra"},

    def nde_option_maker():
        nde_json = requests.get(f"{api_url}all_nde")

        nde_list = nde_json.json()

        nde_list_parsed = []

        for nde in nde_list:
            if client_name.value != "Otro":
                try:
                    if nde["nde_spec"]:
                        nde_list_parsed.append(str(nde["nde_spec"]))
                    else:
                        nde_list_parsed.append("No NDE Assigned Yet!!!!")
                except TypeError:
                    print("Type Error!!")
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
        acabado_json = requests.get(f"{api_url}all_acabados")

        acabado_list = acabado_json.json()

        acabado_list_parsed = []

        for acab in acabado_list:
            if client_name.value != "Otro":
                try:
                    acabado_list_parsed.append(str(acab["acabado"]))
                except TypeError:
                    print("Type Error!!")
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
        data = { "nde_spec" : nde_val.value }
        crit_json = requests.get(f"{api_url}all_nde_criteria", json=data)

        crit_list = crit_json.json()

        # print(crit_list)
        # print(type(crit_list) == dict)

        crit_list_parsed = []
        if type(crit_list) == list:
            for criteria in crit_list:
                if client_name.value != "Otro":
                    try:
                        if criteria["acceptance_criteria"]:
                            crit_list_parsed.append(str(criteria["acceptance_criteria"]))
                        else:
                            crit_list_parsed.append("No Acceptance Criteria Yet!!!!")
                    except TypeError:
                        crit_list_parsed.append("No criteria yet")
                        print("Type Error!!")
                        print("No criteria grabbed from DB")
    
        #plants_list_parsed.append("Otro")

        #print(plants_list_parsed)

        accept_val.options = list(map(ft.dropdown.Option, crit_list_parsed))

        try:
            accept_val.value = crit_list_parsed[0]
        except IndexError:
            accept_val.value = None

        page.update()


    def reload_inspectors():

        in_name = []       

        response = requests.get(f"{api_url}all_inspectors")

        inspectors = response.json()

        nonlocal names_width
        names_width = 0

        def ins_adder(e):
            if e.control.value:
                inspectors_list.append(str(e.control.label))
                print(inspectors_list)
            else:
                inspectors_list.pop()
                print(inspectors_list)

        for inspector in inspectors:
            names_width += 50
            in_name.append(
                ft.Checkbox(
                    label=inspector["name"],
                    label_style=ft.TextStyle(color="black"),
                    on_change=ins_adder
                    #on_change=ins_grabber
                )
            )
        return in_name
    
    # in_name = reload_inspectors

    print(f"{api_url}all_clients")
    clients_json = requests.get(f"{api_url}all_clients")
    clients_list = clients_json.json()

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

        print("clients_json: ", clients_json)

        clients_list = clients_json.json()

        print("clients_list:", clients_list)

        clients_list_parsed = []

        print("clients_list_parsed: ", clients_list_parsed)

        for client in clients_list:
            clients_list_parsed.append(str(client["name"]))
            print("Appended client name: ", client["name"])

        clients_list_parsed.append("Otro")

        print("Clients_list_parsed: ", clients_list_parsed)

        client_name.options = list(map(ft.dropdown.Option, clients_list_parsed))

        page.update()
    
    def reload_plants(client_data: dict):
        plants_json = requests.get(f"{api_url}all_client_plants/", json=client_data)
        nonlocal plants_list
        plants_list = {}
        plants_list = plants_json.json()

        nonlocal plants_list_parsed
        plants_list_parsed = []

        for plant in plants_list:
            if client_name.value != "Otro":
                try:
                    plants_list_parsed.append(str(plant["name"]))
                except TypeError:
                    print("Type Error!!")
                    print("No plant name grabbed from DB")
    
        plants_list_parsed.append("Otro")

        #print(plants_list_parsed)

        plant_name.options = list(map(ft.dropdown.Option, plants_list_parsed))

        page.update()

    def reload_contacts(client_data: dict):
        contacts_json = requests.get(f"{api_url}all_client_contacts/", json=client_data)
        nonlocal contacts_list
        contacts_list = {}
        contacts_list = contacts_json.json()

        nonlocal contacts_list_parsed
        contacts_list_parsed = []

        for contact in contacts_list:
            if client_name.value != "Otro":
                try:
                    contacts_list_parsed.append(str(contact["name"]))
                except TypeError:
                    print("Type Error!!")
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
            page.update()
        else:
            other_client_name.visible = False
            other_plant_name.visible = False
            other_contact_name.visible = False
            plant_name.visible = True
            contact_name.visible = True
            send_all_btn.visible = False

            page.update()

        client_data = {
            "name" : client_name.value
        }

        #plant reload section

        reload_plants(client_data)

        #contact reload section

        reload_contacts(client_data)

        plant_name.value = plants_list_parsed[0]

        contact_name.value = contacts_list_parsed[0]

        #testing each one of the list/option makers to check which one causes the error of 
        #the app not updating

        nde_option_maker() #tested, the app works with this single one enabled
        acc_crit_option_maker() #tested, the app works with this single one enabled
        acabado_option_maker() #tested, the app works with this single one enabled
        distance_list_maker() #tested, the app works with this single one enabled
        sensitivity_list_maker() #tested, the app works with this single one enabled
        notch_list_maker() #tested, the app works with this single one enabled
        record_list_maker() #tested, the app works with this single one enabled
        scanning_list_maker() #tested, the app won´t work with this single one enabled, checking what caused the failure
        #^ i think i corrected it, it the control values referenced to the other control value and both referenced to the value that it should've had
        inspection_info_list_maker() #tested, the app works with this single one enabled

        page.update()
    
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

    def plant_change(e):
        # print(e.control.value)
        if e.control.value == "Otro":
            other_plant_name.visible = True
            other_plant_button.visible = True
            page.update()
        else:
            other_plant_name.visible = False
            other_plant_button.visible = False
            page.update()

    def send_plant(e):
        if other_plant_name.value and client_name.value:

            # print(other_plant_name.value)
            # print(client_name.value)
            
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

            # print(other_contact_name.value)
            # print(client_name.value)
            
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
        bgcolor=ft.Colors.PURPLE,
        visible=False,
        on_click=send_plant
    )
    
    def contact_change(e):
        # print(e.control.value)
        if e.control.value == "Otro":
            other_contact_name.visible = True
            other_contact_button.visible = True
            page.update()
        else:
            other_contact_name.visible = False
            other_contact_button.visible = False
            page.update()

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
        bgcolor=ft.Colors.PURPLE,
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

    def send_all(e):
        # print(other_client_name.value + other_contact_name.value + other_plant_name.value)
        if other_client_name.value and other_contact_name.value and other_plant_name.value:
            # print("text")
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
        bgcolor=ft.Colors.PURPLE,
        visible=False,
        on_click=send_all
    )

    def if_int(x: list):
        for y in x:
            try:
                z = int(y)
                # print(z)
                if type(z) is int:
                    return z
                else:
                    print("not int")
            except ValueError:
                print(f"{y} Cant be converted into Int")

    async def click(e):
    #     print(box_group.value, inspectors_list)
    #     print(f"you click{job.value}")
        #hacer una función para que se guarde el reporte en la base de datos y se haga un numero de reporte
        #url = f"{api_url}?test={box_group.value}&report_num={box_group.value}-R-{year}-234&client_name={client_name_var}&plant={plant_name_var}&contact_name={contact.value}&part_desc={Description.value}&material={material.value}&heat={heat.value}&j_order={job_order.value}&j_qty={job.value}&od={od_val.value}&id={id_val.value}&width={thick_val.value}&height={height_val.value}&NDE={nde_val.value}&crit_accept={accept_val.value}&rough={surface_val.value}&uti_sn={uti_sn.value}&sn1={test_sn1.value}&d_cal={distance.value}&sens_block={sensitivity.value}&notch={notch.value}&rec_lvl={record.value}&ax_scanning={axial_x.value}&circ_ax_scanning={circumferental_x.value}&method={inspection.value}&coupling={coupling.value}&stage={inspector_s.value}&remarks={textarea.value}&insp_name={inspectors_list[0]}&ndt_act={ndt_act.value}"
        #print(url)
        try:
            data = {
                "test":box_group.value,
                "client_name":client_name.value,
                "plant":plant_name.value,
                "contact_name":contact_name.value,
                "part_desc":Description.value,
                "material":material.value,
                "heat":heat.value,
                "j_order":job_order.value + f" {job_order.suffix_text}",
                "j_qty":job_qty_txtbox.value + " Pieces",
                "od":f"{float(od_txtbox.value)} {od_txtbox.suffix_text}",
                "id":f"{float(id_txtbox.value)} {od_txtbox.suffix_text}",
                "width":f"{float(thick_txtbox.value)} {od_txtbox.suffix_text}",
                "height":f"{float(height_txtbox.value)} {od_txtbox.suffix_text}",
                "NDE":nde_val.value,
                "crit_accept":accept_val.value,
                #rehacer la parte de surface roughness para agregar el acabado superficial
                "rough":f"{acabado.value}, (≤{surface_val.value} {measure.value})",
                "uti_sn":int(uti_sn.value.split()[1]),
                "calibrations":[],
                # "sn1": int(test_sn_table.rows[0].cells[2].content.value),
                "d_cal":distance_dropdown.value,
                "sens_block":sensitivity_dropdown.value,
                "notch":notch_dropdown.value,
                "rec_lvl":record_dropdown.value,
                "ax_scanning":axial_x.value,
                "circ_ax_scanning":circumferential_x.value,
                "method":ins_method_dropdown.value,
                "coupling":agent_dropdown.value,
                "stage":stage_dropdown.value,
                "remarks":textarea.value,
                "insp_name":inspectors_list[0],
                "ndt_act":ndt_act.value,
                # "sens_meth1":test_sn_table.rows[0].cells[6].content.value,
                # "ref_size1":(test_sn_table.rows[0].cells[7].content.controls[0].value + " " + test_sn_table.rows[0].cells[7].content.controls[1].value + test_sn_table.rows[0].cells[7].content.controls[1].suffix_text),
                # "ref_level1": test_sn_table.rows[0].cells[8].content.value + " dB",
                # "trans_cor1": test_sn_table.rows[0].cells[9].content.value + " dB",
                # "scan_lev1": test_sn_table.rows[0].cells[10].content.value + " dB",
                # "screen_range1": test_sn_table.rows[0].cells[11].content.value + '"',
                # "scan_type1": test_sn_table.rows[0].cells[12].content.value
            }
        except IndexError:
            print("Index Error in line 698, sn1")

        if check.value:
            data["acc_sn"] = sn.value
        else:
            data["rej_sn"] = sn.value

        for i in test_sn_table.rows:
            data["calibrations"].append(
                {
                    "sn":i.cells[2].content.value,
                    "sens":i.cells[6].content.value, #formerly sens_meth
                    "ref":(i.cells[7].content.controls[0].value + " " + i.cells[7].content.controls[1].value + i.cells[7].content.controls[1].suffix_text), #formerly ref_size
                    "ref_l":i.cells[8].content.value + " dB", #formerly ref_level
                    "cor":i.cells[9].content.value + " dB", #formerly trans_cor
                    "scan":i.cells[10].content.value + " dB", #formerly scan_lev
                    "screen":i.cells[11].content.value + '"', #formerly screen_range
                    "scan_t":i.cells[12].content.value #formerly scan_type
                }
            )

        #changing from if to try except

        # # if test_sn2.value  != '':
        # try:
        #     data["sn2"] = if_int(test_sn_table.rows[1].cells[2].content.value)
        # except TypeError:
        #     print("Type Error!!")
        # except AttributeError:
        #     print("No Value")
        # except IndexError:
        #     print("no value in the second place of the rows array from test_sn_table")

        # # if test_sn3.value != '':
        # try:
        #     data["sn3"] = if_int(test_sn_table.rows[2].cells[2].content.value)
        # except TypeError:
        #     print("Type Error!!")
        # except AttributeError:
        #     print("No Value")
        # except IndexError:
        #     print("no value in the third place of the rows array from test_sn_table")

        # # if test_sn4.value != '':
        # try:
        #     data["sn4"] = if_int(test_sn_table.rows[3].cells[2].content.value)
        # except TypeError:
        #     print("Type Error!!")
        # except AttributeError:
        #     print("No Value")
        # except IndexError:
        #     print("no value in the fourth place of the rows array from test_sn_table")

        # # if test_sn5.value != '':
        # try:
        #     data["sn5"] = if_int(test_sn_table.rows[4].cells[2].content.value)
        # except TypeError:
        #     print("Type Error!!")
        # except AttributeError:
        #     print("No Value")
        # except IndexError:
        #     print("no value in the fifth place of the rows array from test_sn_table")

        print(requests.get(f"{api_url}Report_Number").text)

        pdfurldownload = str(downloads_path) + "\\" + "Inspection_Report_" + str(box_group.value) + "-R-" + str(year) + "-" + requests.get(f"{api_url}Report_Number").text.replace('"', "") + ".pdf" #f"{downloads_path}\\Inspection Report {box_group.value}-R-{year}-{requests.get(f"{api_url}Report_Number")}.pdf"

        print(pdfurldownload)

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

    def change_area(e):
        if check.value:
            textarea.value = "No Recordable Indications Found"
            page.update()
        else:
            textarea.value = "Rejectable Indications Were Found"
            page.update()

    ndt_act = ft.TextField(
        width=320,
        border_radius=10,
        label="NDT Activities",
        value="Perform and Evaluate",
        color="black",
        border_color="black",
        label_style=ft.TextStyle(color="black"),
        border_width=1
    )

    check = ft.CupertinoCheckbox(
        label="Accept?",
        value=True,
        on_change=change_area
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
        value="rms"
    )

    def uti_list_maker():
        uti_json = requests.get(f"{api_url}all_uti")
        uti_list = uti_json.json()

        uti_list_parsed = []

        for uti in uti_list:
            uti_list_parsed.append(f"{uti["model"]} {uti["sn"]}")


        return uti_list_parsed

    uti_list_parsed = uti_list_maker()
    
    def uti_change(e):

        sn = e.control.value.split()[1]

        UTI = requests.get(f"{api_url}uti_by_sn", json={"sn": sn})

        uti_dict = UTI.json()

        # print(uti_dict)

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

    def distance_list_maker():
        distance_json = requests.get(f"{api_url}all_distances")
        distance_list = distance_json.json()
        print(distance_list)

        distance_list_parsed = []

        for distance in distance_list:
            distance_list_parsed.append(str(distance["distance"]))

        distance_dropdown.options = list(map(ft.dropdown.Option, distance_list_parsed))
        
        distance_dropdown.value = distance_list_parsed[0]

    distance_dropdown = ft.Dropdown(
        label="Distance", 
        border_radius=10,
        width=320,
    )

    def sensitivity_list_maker():
        sens_json = requests.get(f"{api_url}all_sensitivities")
        sens_list = sens_json.json()

        sens_list_parsed = []

        for sens in sens_list:
            sens_list_parsed.append(str(sens["sensitivity"]))

        sensitivity_dropdown.options = list(map(ft.dropdown.Option, sens_list_parsed))

        sensitivity_dropdown.value = sens_list_parsed[0]

    sensitivity_dropdown = ft.Dropdown(
        label="sensitivity", 
        border_radius=10,
        width=320
    )

    def notch_list_maker():
        notch_json = requests.get(f"{api_url}all_notches")
        notch_list = notch_json.json()

        notch_list_parsed = []

        for notch in notch_list:
            notch_list_parsed.append(str(notch["notch_depth"]))

        notch_dropdown.options = list(map(ft.dropdown.Option, notch_list_parsed))

        notch_dropdown.value = notch_list_parsed[0]

    notch_dropdown = ft.Dropdown(
        label="notch", 
        border_radius=10,
        width=320
    )

    def record_list_maker():
        record_json = requests.get(f"{api_url}all_records")
        record_list = record_json.json()

        record_list_parsed = []

        for record in record_list:
            record_list_parsed.append(str(record["recording_level"]))

        record_dropdown.options = list(map(ft.dropdown.Option, record_list_parsed))

        record_dropdown.value = record_list_parsed[0]

    record_dropdown = ft.Dropdown(
        label="recording", 
        border_radius=10,
        width=320
    )

    def scanning_list_maker():
        #work in progress
        scanning_json = requests.get(f"{api_url}all_scannings")
        scanning_list = scanning_json.json()

        scanning_list_parsed = []

        for scanning in scanning_list:
            scanning_list_parsed.append(str(scanning["scanning_direction"]))

        circumferential_x.options = list(map(ft.dropdown.Option, scanning_list_parsed))
        
        axial_x.options = list(map(ft.dropdown.Option, scanning_list_parsed))

        circumferential_x.value = scanning_list_parsed[0]
        axial_x.value = scanning_list_parsed[0]

    axial_x = ft.Dropdown(
        label="axial scanning", 
        border_radius=10,
        width=320
    )

    circumferential_x = ft.Dropdown(
        label="circumferential / axial Scanning", 
        border_radius=10,
        width=320
    )

    def inspection_info_list_maker():
        ins_json = requests.get(f"{api_url}all_inspection_info")
        inspection_info = ins_json.json()

        method_list_parsed = []

        stage_list_parsed = []

        agent_list_parsed = []

        for method in inspection_info["method"]:
            method_list_parsed.append(str(method["ins_method"]))

        for agent in inspection_info["agent"]:
            agent_list_parsed.append(str(agent["coupling_agent"]))

        for stage in inspection_info["stage"]:
            stage_list_parsed.append(str(stage["ins_stage"]))

        ins_method_dropdown.options = list(map(ft.dropdown.Option, method_list_parsed))

        ins_method_dropdown.value = method_list_parsed[0]

        agent_dropdown.options = list(map(ft.dropdown.Option, agent_list_parsed))

        agent_dropdown.value = agent_list_parsed[0]

        stage_dropdown.options = list(map(ft.dropdown.Option, stage_list_parsed))

        stage_dropdown.value = stage_list_parsed[0]

    ins_method_dropdown = ft.Dropdown(
        label="inspection method", 
        border_radius=10,
        width=320
    )

    agent_dropdown = ft.Dropdown(
        label="coupling agent", 
        border_radius=10,
        width=320,
    )

    stage_dropdown = ft.Dropdown(
        label="Inspection stage", 
        border_radius=10,
        width=320
    )

    sn = ft.TextField(
        label="sn", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.NumbersOnlyInputFilter(),
        width=320
    )

    textarea = ft.TextField(
        width=300,
        height=350,
        multiline=True,
        min_lines=6,
        max_lines=6,
        border_radius=10,
        value="No Recordable Indications Found"
    )

    #aqui va la funcion de test sn list

    # def test_sn_list_maker():
    #     test_json = requests.get(f"{api_url}all_setups")
    #     test_list = test_json.json()

    #     test_list_parsed = []

    #     for test in test_list:
    #         test_list_parsed.append(f"{test["brand"]} {test["model"]} {test["sn"]}")


    #     return test_list_parsed

    # test_list_parsed = test_sn_list_maker()

    # def test1_change(e):
    #     # sn = e.control.value.split()[2]
    #     for i in e.control.value.split():
    #         try:
    #             if type(int(i)) == int:
    #                 sn = i
    #                 print(f"{i} is int")
    #             print(i)
    #         except:
    #             print("no int in test_sn1")

    #     setup = requests.get(f"{api_url}setups_by_sn", json={"sn": sn})

    #     setup_dict = setup.json()

    #     # print(uti_dict)

    #     # setup1_data.visible = True

    #     # setup1_data.value = f"Brand: {setup_dict["brand"]}  Model: {setup_dict["model"]} \n SN: {setup_dict["sn"]} \n Frequency: {setup_dict["frequency"]} \n Size: {setup_dict["size"]} \n Angle: {setup_dict["angle"]} \n Sensitivity: {setup_dict["sensitivity"]} \n Reference Size: {setup_dict["reference_size"]} \n Reference level: {setup_dict["reference_level"]} \n Transfer correction: {setup_dict["transfer_correction"]} \n Scanning Level: {setup_dict["scanning_level"]} \n Screen Range: {setup_dict["screen_range"]} \n Scan type: {setup_dict["scan_type"]}"

    #     test_calibration_container.height += 250

    #     page.update()
    
    # def test2_change(e):
    #     # sn = e.control.value.split()[2]
    #     for i in e.control.value.split():
    #         try:
    #             if type(int(i)) == int:
    #                 sn = i
    #                 print(f"{i} is int")
    #             print(i)
    #         except:
    #             print("no int in test_sn2")

    #     setup = requests.get(f"{api_url}setups_by_sn", json={"sn": sn})

    #     setup_dict = setup.json()

    #     # print(uti_dict)

    #     # setup2_data.visible = True

    #     # setup2_data.value = f"Brand: {setup_dict["brand"]}  Model: {setup_dict["model"]} \n SN: {setup_dict["sn"]} \n Frequency: {setup_dict["frequency"]} \n Size: {setup_dict["size"]} \n Angle: {setup_dict["angle"]} \n Sensitivity: {setup_dict["sensitivity"]} \n Reference Size: {setup_dict["reference_size"]} \n Reference level: {setup_dict["reference_level"]} \n Transfer correction: {setup_dict["transfer_correction"]} \n Scanning Level: {setup_dict["scanning_level"]} \n Screen Range: {setup_dict["screen_range"]} \n Scan type: {setup_dict["scan_type"]}"

    #     test_calibration_container.height += 250

    #     page.update()

    # def test3_change(e):
    #     # sn = e.control.value.split()[2]
    #     for i in e.control.value.split():
    #         try:
    #             if type(int(i)) == int:
    #                 sn = i
    #                 print(f"{i} is int")
    #             print(i)
    #         except:
    #             print("no int in test_sn3")

    #     setup = requests.get(f"{api_url}setups_by_sn", json={"sn": sn})

    #     setup_dict = setup.json()

    #     # print(uti_dict)

    #     # setup3_data.visible = True

    #     # setup3_data.value = f"Brand: {setup_dict["brand"]}  Model: {setup_dict["model"]} \n SN: {setup_dict["sn"]} \n Frequency: {setup_dict["frequency"]} \n Size: {setup_dict["size"]} \n Angle: {setup_dict["angle"]} \n Sensitivity: {setup_dict["sensitivity"]} \n Reference Size: {setup_dict["reference_size"]} \n Reference level: {setup_dict["reference_level"]} \n Transfer correction: {setup_dict["transfer_correction"]} \n Scanning Level: {setup_dict["scanning_level"]} \n Screen Range: {setup_dict["screen_range"]} \n Scan type: {setup_dict["scan_type"]}"

    #     test_calibration_container.height += 250

    #     page.update()

    # def test4_change(e):
    #     # sn = e.control.value.split()[2]
    #     for i in e.control.value.split():
    #         try:
    #             if type(int(i)) == int:
    #                 sn = i
    #                 print(f"{i} is int")
    #             print(i)
    #         except:
    #             print("no int in test_sn4")

    #     setup = requests.get(f"{api_url}setups_by_sn", json={"sn": sn})

    #     setup_dict = setup.json()

    #     # print(uti_dict)

    #     # setup4_data.visible = True

    #     # setup4_data.value = f"Brand: {setup_dict["brand"]}  Model: {setup_dict["model"]} \n SN: {setup_dict["sn"]} \n Frequency: {setup_dict["frequency"]} \n Size: {setup_dict["size"]} \n Angle: {setup_dict["angle"]} \n Sensitivity: {setup_dict["sensitivity"]} \n Reference Size: {setup_dict["reference_size"]} \n Reference level: {setup_dict["reference_level"]} \n Transfer correction: {setup_dict["transfer_correction"]} \n Scanning Level: {setup_dict["scanning_level"]} \n Screen Range: {setup_dict["screen_range"]} \n Scan type: {setup_dict["scan_type"]}"

    #     test_calibration_container.height += 250

    #     page.update()

    # def test5_change(e):
    #     # sn = e.control.value.split()[2]
    #     for i in e.control.value.split():
    #         try:
    #             if type(int(i)) == int:
    #                 sn = i
    #                 print(f"{i} is int")
    #             print(i)
    #         except:
    #             print("no int in test_sn5")

    #     setup = requests.get(f"{api_url}setups_by_sn", json={"sn": sn})

    #     setup_dict = setup.json()

    #     # print(uti_dict)

    #     # setup5_data.visible = True

    #     # setup5_data.value = f"Brand: {setup_dict["brand"]}  Model: {setup_dict["model"]} \n SN: {setup_dict["sn"]} \n Frequency: {setup_dict["frequency"]} \n Size: {setup_dict["size"]} \n Angle: {setup_dict["angle"]} \n Sensitivity: {setup_dict["sensitivity"]} \n Reference Size: {setup_dict["reference_size"]} \n Reference level: {setup_dict["reference_level"]} \n Transfer correction: {setup_dict["transfer_correction"]} \n Scanning Level: {setup_dict["scanning_level"]} \n Screen Range: {setup_dict["screen_range"]} \n Scan type: {setup_dict["scan_type"]}"

    #     test_calibration_container.height += 250

    #     page.update()

    # test_sn1 = ft.Dropdown(
    #     label="Test Serial Number 1",
    #     bgcolor="white",
    #     border_radius=10,
    #     width=320,
    #     color="black",
    #     options=list(map(ft.dropdown.Option, test_list_parsed)),
    #     on_change=test1_change
    # )

    # setup1_data = ft.Text(
    #     visible=False,
    #     text_align=ft.TextAlign.CENTER
    # )

    # test_sn2 = ft.Dropdown(
    #     label="Test Serial Number 2",
    #     bgcolor="white",
    #     border_radius=10,
    #     width=320,
    #     color="black",
    #     options=list(map(ft.dropdown.Option, test_list_parsed)),
    #     visible=False,
    #     on_change=test2_change
    # )

    # setup2_data = ft.Text(
    #     visible=False,
    #     text_align=ft.TextAlign.CENTER
    # )

    # test_sn3 = ft.Dropdown(
    #     label="Test Serial Number 3",
    #     bgcolor="white",
    #     border_radius=10,
    #     width=320,
    #     color="black",
    #     options=list(map(ft.dropdown.Option, test_list_parsed)),
    #     visible=False,
    #     on_change=test3_change
    # )

    # setup3_data = ft.Text(
    #     visible=False,
    #     text_align=ft.TextAlign.CENTER
    # )

    # test_sn4 = ft.Dropdown(
    #     label="Test Serial Number 4",
    #     bgcolor="white",
    #     border_radius=10,
    #     width=320,
    #     color="black",
    #     options=list(map(ft.dropdown.Option, test_list_parsed)),
    #     visible=False,
    #     on_change=test4_change
    # )

    # setup4_data = ft.Text(
    #     visible=False,
    #     text_align=ft.TextAlign.CENTER
    # )

    # test_sn5 = ft.Dropdown(
    #     label="Test Serial Number 5",
    #     bgcolor="white",
    #     border_radius=10,
    #     width=320,
    #     color="black",
    #     options=list(map(ft.dropdown.Option, test_list_parsed)),
    #     visible=False,
    #     on_change=test5_change
    # )

    # setup5_data = ft.Text(
    #     visible=False,
    #     text_align=ft.TextAlign.CENTER
    # )

    
    # textarea_counter = 1

    # def add_textarea(e):
    #     nonlocal textarea_counter, test_sn_height, test_calibration_container
        
    #     if textarea_counter >= 1 and textarea_counter <= 5:
    #         textarea_counter = textarea_counter + 1
    #         if textarea_counter == 2:
    #             test_sn2.visible = True
    #             test_calibration_container.height += 70
    #         elif textarea_counter == 3:
    #             test_sn3.visible = True
    #             test_calibration_container.height += 70
    #         elif textarea_counter == 4:
    #             test_sn4.visible = True
    #             test_calibration_container.height += 70
    #         elif textarea_counter == 5:
    #             test_sn5.visible = True
    #             test_calibration_container.height += 70

    #         page.update()
    #     elif textarea_counter > 5:
    #         textarea_counter = textarea_counter - 1
    #     elif textarea_counter < 1:
    #         textarea_counter = textarea_counter + 1
    #     else:
    #         print("error +")

    # def del_textarea(e):
    #     nonlocal textarea_counter, test_sn_height, test_calibration_container
    #     if textarea_counter >= 1 and textarea_counter <= 5:
    #         if textarea_counter == 2:
    #             test_sn2.visible = False
    #             test_sn2.value = ""
    #             # setup2_data.visible = False
    #             test_calibration_container.height -= 70
    #         elif textarea_counter == 3:
    #             test_sn3.visible = False
    #             test_sn3.value = ""
    #             # setup3_data.visible = False
    #             test_calibration_container.height -= 70
    #         elif textarea_counter == 4:
    #             test_sn4.visible = False
    #             test_sn4.value = ""
    #             # setup4_data.visible = False
    #             test_calibration_container.height -= 70
    #         elif textarea_counter == 5:
    #             test_sn5.visible = False
    #             test_sn5.value = ""
    #             # setup5_data.visible = False
    #             test_calibration_container.height -= 70
    #         textarea_counter = textarea_counter - 1

    #         if textarea_counter != 0:
    #             test_calibration_container.height = (300 * (textarea_counter-1)) + 250
    #         else:
    #             test_calibration_container.height = 250

    #         page.update()
    #     elif textarea_counter < 1:
    #         textarea_counter = textarea_counter + 1
    #     elif textarea_counter > 5:
    #         textarea_counter = textarea_counter - 1
    #     else:
    #         print("error -")


    # add_btn = ft.IconButton(
    #     icon= ft.Icons.ADD,
    #     on_click=add_textarea
    # )
    
    # del_btn = ft.IconButton(
    #     icon= ft.Icons.REMOVE_ROUNDED,
    #     on_click=del_textarea
    # )

    #aqui va la funcion de test sn list
    def test_sn_list_maker():
        test_json = requests.get(f"{api_url}all_probes")
        test_list = test_json.json()
        test_list_parsed = []
        for test in test_list:
            test_list_parsed.append(f"{test["sn"]}")
        return test_list_parsed
    
    test_list_parsed = test_sn_list_maker()

    test_sn_dropdown = ft.Dropdown(
        label="Probe SN",
        width=200,
        bgcolor="white",
        color="black",
        options=list(map(ft.dropdown.Option, test_list_parsed)),
        value=test_list_parsed[0]
    )

    def del_row(e):
        test_sn_table.rows.pop()
        page.update()

    test_sn_cell_del_btn = ft.IconButton(
        icon=ft.Icons.DELETE_FOREVER_ROUNDED,
        on_click=del_row
    )

    hole_list = ["FBH", "SDH"]
    scan_list = ["OD", "Axial", "Radial"]

    #https://ideone.com/ItifKv

    def convert_to_float(frac_str):
        try:
            return float(frac_str)
        except ValueError:
            num, denom = frac_str.split('/')
            try:
                leading, num = num.split(' ')
                whole = float(leading)
            except ValueError:
                whole = 0
            frac = float(num) / float(denom)
            return whole - frac if whole < 0 else whole + frac

    def nvalF(e):

        #this lets the string be in the fraction format (4/5) without any other character

        for i in e.control.value:
            print(i)
            if (i in (string.digits + '/')) and e.control.value.count('/') <= 1:
                print("Value within parameters")
                e.control.suffix_text = f'" ({round(convert_to_float(e.control.value)*25.4, 2)} mm)'
            else:
                e.control.value = e.control.value[:-1]
                print("Value not within parameters")

        page.update()

    def test_sn_adder(e):
        sn = test_sn_dropdown.value
        if sn is not None:
            probe_sn_json = requests.get(f"{api_url}probes_by_sn", json={"sn" : sn})
            probe_sn = probe_sn_json.json()
            if len(test_sn_table.rows) < 5:
                test_sn_table.rows.append(
                    ft.DataRow(
                        cells=
                        [
                            ft.DataCell(
                                ft.Text(f"{probe_sn["brand"]}")
                            ),
                            ft.DataCell(
                                ft.Text(f"{probe_sn["model"]}")
                            ),
                            ft.DataCell(
                                ft.Text(f"{probe_sn["sn"]}")
                            ),
                            ft.DataCell(
                                ft.Text(f"{probe_sn["freq"]}")
                            ),
                            ft.DataCell(
                                ft.Text(f"{probe_sn["size"]}")
                            ),
                            ft.DataCell(
                                ft.Text(f"{probe_sn["angle"]}")
                            ),
                            ft.DataCell(
                                ft.Dropdown(
                                    label="Sensitivity Method",
                                    width=200,
                                    bgcolor="white",
                                    color="black",
                                    options=list(map(ft.dropdown.Option, SM_list_parsed)),
                                    value=SM_list_parsed[0]
                                )
                            ),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.Dropdown(
                                            label="Hole",
                                            width=80,
                                            bgcolor="white",
                                            color="black",
                                            options=list(map(ft.dropdown.Option, hole_list)),
                                            value=hole_list[0]
                                        ),
                                        ft.TextField(
                                            label="Size",
                                            width=200,
                                            bgcolor="white",
                                            color="black",
                                            input_filter=ft.InputFilter(allow=True, regex_string=r'^(\d{1,2}(/(\d{1,2})?)?|/(\d{1,2})?)?$', replacement_string=""),
                                            on_change=nvalF
                                        )
                                    ],
                                    width=300
                                ),  
                            ),
                            ft.DataCell(
                                ft.TextField(
                                    label="Reference Level",
                                    width=100,
                                    bgcolor="white",
                                    color="black",
                                    input_filter=ft.InputFilter(allow=True, regex_string=r"^(\d{1,2}(\.\d?)?|\.\d)?$", replacement_string=""),
                                    suffix_text="dB"
                                    # on_change=NFilter
                                )
                            ),
                            ft.DataCell(
                                ft.TextField(
                                    label="Transfer Correction",
                                    width=100,
                                    bgcolor="white",
                                    color="black",
                                    input_filter=ft.InputFilter(allow=True, regex_string=r"^(\d{1,2}(\.\d?)?|\.\d)?$", replacement_string=""),
                                    suffix_text="dB",
                                    prefix_text="+"
                                )
                            ),
                            ft.DataCell(
                                ft.TextField(
                                    label="Scanning Level",
                                    width=100,
                                    bgcolor="white",
                                    color="black",
                                    input_filter=ft.InputFilter(allow=True, regex_string=r"^(\d{1,2}(\.\d?)?|\.\d)?$", replacement_string=""),
                                    suffix_text="dB",
                                    prefix_text="+"
                                )
                            ),
                            ft.DataCell(
                                ft.TextField(
                                    label="Screen Range",
                                    width=100,
                                    bgcolor="white",
                                    color="black",
                                    input_filter=ft.InputFilter(allow=True, regex_string=r"^(\d{1,2}(\.\d?)?|\.\d)?$", replacement_string=""),
                                    suffix_text='"'
                                )
                            ),
                            ft.DataCell(
                                ft.Dropdown(
                                    width=100,
                                    bgcolor="white",
                                    color="black",
                                    options=list(map(ft.dropdown.Option, scan_list)),
                                    value=scan_list[0]
                                )
                            ),
                        ]
                    )
                )
            

        page.update()

        # print(test_sn_table.rows[-1].cells[0].content.value)
        # print(test_sn_table.rows[-1].cells[2].content.value)
        # print(test_sn_table.rows[0].cells[6].content.value)
        # print(test_sn_table.rows[0].cells[7].content.controls[0].value)# Reference Size Hole
        # print(test_sn_table.rows[0].cells[7].content.controls[1].value)# Reference Size Size
        # print(test_sn_table.rows[0].cells[7].content.controls[1].suffix_text)# Reference Size Size Suffix Text
        # print(len(test_sn_table.rows))

    test_sn_add_btn = ft.IconButton(
        icon=ft.Icons.ADD,
        on_click=test_sn_adder
    )

    test_sn_adder_space = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    test_sn_dropdown,
                    test_sn_add_btn,
                    test_sn_cell_del_btn
                ],
                alignment="center"
            )
        ],
        horizontal_alignment="center"
    )

    def SM_list_maker():
        SM_json = requests.get(f"{api_url}all_SM")
        SM_list = SM_json.json()
        SM_list_parsed = []
        for SM in SM_list:
            SM_list_parsed.append(f"{SM["method"]}")
        return SM_list_parsed
    
    SM_list_parsed = SM_list_maker()

    test_sn_table = ft.DataTable(
        show_checkbox_column=True,
        columns=[
            ft.DataColumn(
                ft.Text("Brand"),
            ),
            ft.DataColumn(
                ft.Text("Model"),
            ),
            ft.DataColumn(
                ft.Text("SN"),
            ),
            ft.DataColumn(
                 ft.Text("Freq"),
            ),
            ft.DataColumn(
                ft.Text("Size"),
            ),
            ft.DataColumn(
                ft.Text("Angle"),
            ),
            ft.DataColumn(
                ft.Text("Sensitivity Method")
            ),
            ft.DataColumn(
                ft.Text("Reference Size")
            ),
            ft.DataColumn(
                ft.Text("Reference Level")
            ),
            ft.DataColumn(
                ft.Text("Transfer Correction")
            ),
            ft.DataColumn(
                ft.Text("Scanning Level")
            ),
            ft.DataColumn(
                ft.Text("Screen Range")
            ),
            ft.DataColumn(
                ft.Text("Scan Type")
            )
        ],
        rows=[
            # ft.DataRow(
            #     cells=[
            #         ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE_FOREVER_ROUNDED)),
            #         ft.DataCell(ft.Text("OLYMPUS")),
            #         ft.DataCell(ft.Text("OLYMPUS")),
            #         ft.DataCell(ft.Text("OLYMPUS")),
            #         ft.DataCell(ft.Text("OLYMPUS")),
            #         ft.DataCell(ft.Text("OLYMPUS")),
            #         ft.DataCell(ft.Text("OLYMPUS"))
            #     ]
            # )
        ]
    )

    test_sn_table_column = ft.Column(
        controls=[
            ft.Container(content=ft.Column([ft.Row([test_sn_table], scroll=ft.ScrollMode.ALWAYS)], scroll=ft.ScrollMode.ALWAYS))
        ]
    )

    # test_sn_table1 = ft.DataTable(
    #     width=390,
    #     show_checkbox_column=True,
    #     columns=[
    #         ft.DataColumn(
    #             ft.Text("Selección")
    #         ),
    #         ft.DataColumn(
    #             ft.Text("Brand"),
    #         ),
    #         ft.DataColumn(
    #             ft.Text("Model"),
    #         ),
    #         ft.DataColumn(
    #             ft.Text("SN"),
    #         )
    #     ],
    #     rows=[
    #         ft.DataRow(
    #             cells=[
    #                 ft.DataCell(ft.Checkbox()),
    #                 ft.DataCell(ft.Text("OLYMPUS")),
    #                 ft.DataCell(ft.Text("OLYMPUS")),
    #                 ft.DataCell(ft.Text("OLYMPUS"))
    #             ]
    #         )
    #     ]
    # )

    # test_sn_table2 = ft.DataTable(
    #     width=390,
    #     show_checkbox_column=True,
    #     columns=[
    #         ft.DataColumn(
    #             ft.Text("Freq"),
    #         ),
    #         ft.DataColumn(
    #             ft.Text("Size"),
    #         ),
    #         ft.DataColumn(
    #             ft.Text("Angle"),
    #         )
    #     ],
    #     rows=[
    #         ft.DataRow(
    #             cells=[
    #                 ft.DataCell(ft.Text("OLYMPUS")),
    #                 ft.DataCell(ft.Text("OLYMPUS")),
    #                 ft.DataCell(ft.Text("OLYMPUS"))
    #             ]
    #         )
    #     ]
    # )

    test_calibration_container = ft.Container(
        width=400,
        height=500,
        padding=ft.padding.only(top=10),
        bgcolor=ft.Colors.WHITE,
        content=ft.Column(
            horizontal_alignment="center",
            controls=[
                ft.Text("Test calibration setup", text_align="center", size=25, weight="bold", color="black"),
                ft.Text("Serial Number", size=20),
                test_sn_adder_space,
                test_sn_table_column,
                # test_sn1,
                # setup1_data,
                # test_sn2,
                # setup2_data,
                # test_sn3,
                # setup3_data,
                # test_sn4,
                # setup4_data,
                # test_sn5,
                # setup5_data,
                # ft.Row(
                    # alignment=MainAxisAlignment.END,
                    # controls=[
                        # # del_btn,
                        # # add_btn
                    # ]
                # )
            ]
        )
    )

    def jqty_c(e):
        job_order.suffix_text = f"({e.control.value} pcs)"
        page.update()

    job_qty_txtbox = ft.TextField(
        text_align="center",
        keyboard_type=ft.KeyboardType.NUMBER,
        label="qty",
        width=150,
        height=60,
        border_radius=10,
        show_cursor=False,
        color="black",
        input_filter=ft.NumbersOnlyInputFilter(),
        on_change=jqty_c,
        suffix_text="Pieces"
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
            od_txtbox.suffix_text = '"'
            id_txtbox.suffix_text = '"'
            thick_txtbox.suffix_text = '"'
            height_txtbox.suffix_text = '"'
            inch_or_mm.label = "Inch"
            page.update()
        else:
            od_txtbox.suffix_text = 'mm'
            id_txtbox.suffix_text = 'mm'
            thick_txtbox.suffix_text = 'mm'
            height_txtbox.suffix_text = 'mm'
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
        input_filter=ft.InputFilter(allow=True, regex_string=r"^(\d{1,2}(\.\d?)?|\.\d)?$", replacement_string=""),
        on_change=od_validation,
        suffix_text='"'
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
        input_filter=ft.InputFilter(allow=True, regex_string=r"^(\d{1,2}(\.\d?)?|\.\d)?$", replacement_string=""),
        on_change=id_validation,
        suffix_text='"'
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
        input_filter=ft.InputFilter(allow=True, regex_string=r"^(\d{1,2}(\.\d?)?|\.\d)?$", replacement_string=""),
        on_change=height_validation,
        suffix_text='"'
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
        input_filter=ft.InputFilter(allow=True, regex_string=r"^(\d{1,2}(\.\d?)?|\.\d)?$", replacement_string=""),
        on_change=thick_validation,
        suffix_text='"'
    )

    def bar_change(e):
        index = e.control.selected_index
        if index == 0:
            e.page.go(f"/main_screen")
        if index == 1:
            e.page.go(f"/admin")
        if index == 2:
            e.page.go(f"/")
            user_mail = None 
        page.update()

    NAV = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.EDIT_NOTE, label="Reporte"),
            ft.NavigationBarDestination(icon=ft.Icons.ADMIN_PANEL_SETTINGS, label="Admin"),
            ft.NavigationBarDestination(icon=ft.Icons.EXIT_TO_APP_SHARP, label="Exit")
        ],
        on_change=bar_change
    )

    part_info_text = ft.Text(value="", visible=False)

    error_msg_text = ft.Text(value="", visible=False)

    user_mail = ""

    username_reg = ft.TextField(
        label="Username", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.NAME,
        width=320

    )
    email_reg = ft.TextField(
        label="email", 
        border_radius=10,
        keyboard_type=ft.KeyboardType.EMAIL,
        width=320
    )
    password_reg = ft.TextField(
        label="password",
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        password=True,
        can_reveal_password=True,
        width=320
    )
    conf_pass_reg = ft.TextField(
        label="password",
        border_radius=10,
        keyboard_type=ft.KeyboardType.TEXT,
        password=True,
        can_reveal_password=True,
        width=320
    )

    def login_fun():
        
        data = {
            "email":user_log.value,
            "password":user_psw.value
        }

        register_req = requests.get(f"{api_url}login", json=data)

        if register_req.json()["error"]:
            error_msg_text.visible = register_req.json()["visible"]
            error_msg_text.value = register_req.json()["error_msg"]
        else:
            error_msg_text.visible = False
            user_log.value = None
            user_psw.value = None
            nonlocal user_mail 
            user_mail = register_req.json()["mail"]
            page.go(f"/main_screen")

        page.update()

    def register_fun():
        data = {
            "email":email_reg.value,
            "user":username_reg.value,
            "password":password_reg.value,
            "confpassword":conf_pass_reg.value
        }

        register_req = requests.post(f"{api_url}register", json=data)

        if register_req.json()["error"]:
            error_msg_text.visible = register_req.json()["visible"]
            error_msg_text.value = register_req.json()["error_msg"]
        else:
            error_msg_text.visible = False
            page.go(f"/")

        page.update()


    def route_chnage(route):
        nonlocal user_mail

        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                bgcolor=ft.Colors.BLUE_50,
                controls=[
                    ft.Container(
                        width=400,
                        expand=True,
                        content=ft.Column(
                            alignment="center",
                            horizontal_alignment="center",
                            controls=[
                                ft.Icon(name=ft.Icons.PERSON, size=250, color="black"),
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
                                            error_msg_text,
                                            ft.ElevatedButton(
                                                "login",
                                                elevation=30,
                                                width=200,
                                                height=50,
                                                bgcolor=ft.Colors.PURPLE,
                                                color="white",
                                                on_click=lambda _:login_fun()
                                            ),
                                            ft.Column(
                                                alignment="center",
                                                controls=[
                                                    ft.Row(
                                                        alignment="center",
                                                        controls=[
                                                            ft.Text("No tienes usuario?,"),
                                                            ft.TextButton("Registrate Aqui!", on_click=lambda _:page.go("/register"))
                                                        ]
                                                    )
                                                ]
                                            ),
                                        ],
                                      
                                    )
                                )
                            ]
                        )
                    ) 
                ],
            )
        ),

        if page.route == "/register":
            page.window.height = 770
            page.views.append(
                ft.View(
                    "/register",
                    bgcolor=ft.Colors.BLUE_50,
                    controls=[
                        ft.Container(
                            width=400,
                            expand=True,
                            content=ft.Column(
                                alignment="center",
                                horizontal_alignment="center",
                                controls=[
                                    ft.Icon(name=ft.Icons.PERSON, size=250, color="black"),
                                    ft.Container(
                                        content=ft.Column(
                                            alignment="center",
                                            horizontal_alignment="center",
                                            spacing=15,
                                            controls=[
                                                username_reg,
                                                email_reg,
                                                password_reg,
                                                conf_pass_reg,
                                                ft.Container(
                                                    height=10
                                                ),
                                                error_msg_text,
                                                ft.ElevatedButton(
                                                    "Registrarse",
                                                    elevation=30,
                                                    width=200,
                                                    height=50,
                                                    bgcolor=ft.Colors.PURPLE,
                                                    color="white",
                                                    on_click=lambda _:register_fun()
                                                ),
                                                ft.Column(
                                                    alignment="center",
                                                    controls=[
                                                        ft.Row(
                                                            alignment="center",
                                                            controls=[
                                                                ft.TextButton("Regresar", on_click=lambda _:page.go("/"))
                                                            ]
                                                        )
                                                    ]
                                                ),
                                            ],

                                        )
                                    )
                                ]
                            )
                        )
                    ]
                )
            )

        if page.route == "/main_screen":
            ins_control = reload_inspectors()
            page.views.append(
                ft.View(
                    "/main_screen",
                    scroll="always",
                    horizontal_alignment="center",
                    vertical_alignment="center",
                    padding=0,
                    bgcolor=ft.Colors.BLUE_50,
                    controls=[
                        NAV,
                        ft.SafeArea(
                            ft.Container(
                                height=10,
                                expand=True,
                                bgcolor=ft.Colors.PURPLE,
                            ),
                        ),
                        ft.Column(
                            controls=[
                                ft.Container(
                                    width=400,
                                    height=300,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.Colors.WHITE,
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
                                    bgcolor=ft.Colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("inspector", size=20, weight="bold", color="black"),
                                            ft.Container(
                                            padding=ft.padding.only(top=10),
                                            content=ft.Column(
                                                spacing=5,
                                                controls=ins_control # here, the problem, in?name is a list, so remove this, look
                                                    
                                                ) 
                                            ),
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=650,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.Colors.WHITE,
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
                                #     bgcolor=ft.Colors.WHITE,
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
                                #     bgcolor=ft.Colors.WHITE,
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
                                    bgcolor=ft.Colors.WHITE,
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
                                    bgcolor=ft.Colors.WHITE,
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
                                    bgcolor=ft.Colors.WHITE,
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
                                    bgcolor=ft.Colors.WHITE,
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
                                    bgcolor=ft.Colors.WHITE,
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
                                    bgcolor=ft.Colors.WHITE,
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
                                test_calibration_container,
                                # ft.Container(
                                #     width=400,
                                #     height=test_sn_height + 40,
                                #     padding=ft.padding.only(top=10),
                                #     bgcolor=ft.Colors.WHITE,
                                #     content=ft.Column(
                                #         horizontal_alignment="center",
                                #         controls=[
                                #             ft.Text("Test calibration setup", text_align="center", size=25, weight="bold", color="black"),
                                #             ft.Text("Serial Number", size=20),
                                #             test_sn1,
                                #             setup1_data,
                                #             test_sn2,
                                #             test_sn3,
                                #             test_sn4,
                                #             test_sn5,
                                #             ft.Row(
                                #                 alignment=MainAxisAlignment.END,
                                #                 controls=[
                                #                     del_btn,
                                #                     add_btn
                                #                 ]
                                #             )
                                #         ]
                                #     ),
                                # ),
                                ft.Container(
                                    width=400,
                                    height=490,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.Colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("Calibration blocks", text_align="center", size=25, weight="bold", color="black"),
                                            ft.Text("Distance calibration angle verification", size=20, text_align="center"),
                                            distance_dropdown,
                                            ft.Text("Sensitivity Block", size=20),
                                            sensitivity_dropdown,
                                            ft.Text("Notch Depth", size=20),
                                            notch_dropdown,
                                            ft.Text("Recording Level", size=20),
                                            record_dropdown, 
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=270,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.Colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("Scanning Direction", text_align="center", size=25, weight="bold", color="black"),
                                            ft.Text("Axial scanning", size=20, text_align="center"),
                                            axial_x,
                                            ft.Text("Circumferential/ Axial Scanning", size=20),
                                            circumferential_x,
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=370,
                                    padding=ft.padding.only(top=10),
                                    bgcolor=ft.Colors.WHITE,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.Text("Inspection Information", text_align="center", size=25, weight="bold", color="black"),
                                            ft.Text("Inspection Method", size=20, text_align="center"),
                                            ins_method_dropdown,
                                            ft.Text("coupling agent", size=20, text_align="center"),
                                            agent_dropdown,
                                            ft.Text("Inspection Stage", size=20),
                                            stage_dropdown,
                                        ]
                                    )
                                ),
                                ft.Container(
                                    width=400,
                                    height=750,
                                    #padding=ft.padding.only(top=10),
                                    bgcolor=ft.Colors.WHITE,
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
                                                bgcolor=ft.Colors.PURPLE,
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
     
        if page.route == "/admin":
            page.views.append(
                ft.View(
                    "/admin",
                    scroll="always",
                    horizontal_alignment="center",
                    vertical_alignment="center",
                    padding=0,
                    bgcolor=ft.Colors.BLUE_50,
                    controls=[
                        NAV,
                        ft.SafeArea(
                            ft.Container(
                                height=10,
                                expand=True,
                                bgcolor=ft.Colors.PURPLE,
                            ),
                        ),
                        ft.Column(
                            controls=[
                                admin_page(page, user_mail),
                            ]
                        )
                    ]
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