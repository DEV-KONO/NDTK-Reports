import os
import string
from unittest import TestLoader
from flet import*
from pathlib import Path
import jinja2
from playwright.sync_api import sync_playwright
import flet as ft
import json
import datetime
from LIBS import Wiski64
from Views import data

year = datetime.datetime.now().year
downloads_path = str(Path.home() / "Downloads")

print(f"Directorio actual: {os.getcwd()}")
print(f"Descargas: {downloads_path}")

#test = ""
client_name_var = ""
plant_name_var = ""
contact_name_var = ""
#plant_loc = ""

# load_dotenv(".api.env")

def main(page:ft.Page):
    # api_url = "https://ndtk-reports.onrender.com/" #os.getenv("api_url")

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
    page.go("/main_screen")

    inspectors_list = []

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

    def json_searcher(json: json, table: str, param: str = "", search_param: str = "", search: str = ""):
        
        if param:
            for entry in json[f"{table}"]:
                try:
                    return entry[f"{param}"]
                except:
                    print("Json Searcher Error: Parameter not found")
        elif bool(search_param) and bool(search):
            for entry in json[f"{table}"]:
                try:
                    return entry[f"{search_param}"]
                except:
                    print("Json Searcher Error: Parameter not found")
        elif bool(search_param) != bool(search):
            print("Json Searcher Error: The function need both search and search param to be filled with the property to be searched and the data to be found.")
        else:
            return json[f"{table}"]


        # for json in json["Tables"]:
        #     if json["Name"] == table:
        #         if param:
        #             for entry in json["Data"]:
        #                 try:
        #                     return entry[f"{param}"]
        #                 except:
        #                     print("Json Searcher Error: Parameter not found")
        #         elif bool(search_param) and bool(search):
        #             for entry in json["Data"]:
        #                 if entry[f"{search_param}"] == search:
        #                     try:
        #                         return entry
        #                     except:
        #                         print("Json Searcher Error: Parameter not found")
        #                 else:
        #                     print("Json Searcher Error: Term not found")
        #         elif bool(search_param) != bool(search):
        #             print("Json Searcher Error: The function need both search and search param to be filled with the property to be searched and the data to be found.")
        #         else:
        #             return json["Data"]

    def nde_option_maker():
        # nde_json = requests.get(f"{api_url}all_nde")

        # nde_list = nde_json.json()
        with open(r"data\data.json", "r") as file:
            nde_list = json.load(file)
            nde_list = json_searcher(nde_list, "NDE Specification")

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
    
        nde_val.options = list(map(ft.dropdown.Option, nde_list_parsed))

        try:
            nde_val.value = nde_list_parsed[0]
        except IndexError:
            nde_val.value = None

        page.update()

    def acabado_option_maker():
        # acabado_json = requests.get(f"{api_url}all_acabados")

        # acabado_list = acabado_json.json()
        with open(r"data\data.json", "r") as file:
            acabado_list = json.load(file)
            acabado_list = json_searcher(acabado_list, "Acabado Superficial")

        acabado_list_parsed = []

        for acab in acabado_list:
            if client_name.value != "Otro":
                try:
                    acabado_list_parsed.append(str(acab["acabado"]))
                except TypeError:
                    print("Type Error!!")
                    print("No NDE Specification grabbed from DB")

        acabado.options = list(map(ft.dropdown.Option, acabado_list_parsed))

        try:
            acabado.value = acabado_list_parsed[0]
        except IndexError:
            acabado.value = None

        page.update()

    def acc_crit_option_maker():
        # data = { "nde_spec" : nde_val.value }
        # crit_json = requests.get(f"{api_url}all_nde_criteria", json=data)

        # crit_list = crit_json.json()

        with open(r"data\data.json", "r") as file:
            crit_list = json.load(file)
            crit_list = json_searcher(crit_list, "NDE Specification", "acceptance_criteria")

        crit_list_parsed = []
        if type(crit_list) == list:
            for criteria in crit_list:
                if client_name.value != "Otro":
                    try:
                        if criteria["crit"]:
                            crit_list_parsed.append(str(criteria["crit"]))
                        else:
                            crit_list_parsed.append("No Acceptance Criteria Yet!!!!")
                    except TypeError:
                        crit_list_parsed.append("No criteria yet")
                        print("Type Error!!")
                        print("No criteria grabbed from DB")

        accept_val.options = list(map(ft.dropdown.Option, crit_list_parsed))

        try:
            accept_val.value = crit_list_parsed[0]
        except IndexError:
            accept_val.value = None

        page.update()


    def reload_inspectors():

        in_name = []       

        # response = requests.get(f"{api_url}all_inspectors")

        # inspectors = response.json()

        with open(r"data\data.json", "r") as file:
            inspectors = json.load(file)
            inspectors = json_searcher(inspectors, "Inspectores")

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
                    label=inspector["Name"],
                    label_style=ft.TextStyle(color="black"),
                    on_change=ins_adder
                )
            )
        return in_name

    # clients_json = requests.get(f"{api_url}all_clients")
    # clients_list = clients_json.json()

    with open(r"./data/data.json", "r") as file:
            clients_list = json.load(file)
            clients_list = json_searcher(json=clients_list, table="clientes")

    clients_list_parsed = []

    for client in clients_list:
        clients_list_parsed.append(str(client["name"]))
    
    clients_list_parsed.append("Otro")

    plants_list = {}
    plants_list_parsed = []

    contacts_list = {}
    contacts_list_parsed = []

    def reload_clients():
        # clients_json = requests.get(f"{api_url}all_clients")

        # print("clients_json: ", clients_json)

        # clients_list = clients_json.json()

        with open(r"data\data.json", "r") as file:
            clients_list = json.load(file)
            clients_list = json_searcher(clients_list, "clientes")
            

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
        # plants_json = requests.get(f"{api_url}all_client_plants/", json=client_data)
        nonlocal plants_list
        plants_list = {}

        # plants_list = plants_json.json()

        with open(r"data\data.json", "r") as file:
            plants_list = json.load(file)
            plants_list = json_searcher(plants_list, "clientes", "plantas")

        nonlocal plants_list_parsed
        plants_list_parsed = []

        for plant in plants_list:
            if client_name.value != "Otro":
                try:
                    plants_list_parsed.append(plant)
                except TypeError:
                    print("Type Error!!")
                    print("No plant name grabbed from DB")
    
        plants_list_parsed.append("Otro")

        plant_name.options = list(map(ft.dropdown.Option, plants_list_parsed))

        page.update()

    def reload_contacts(client_data: dict):
        # contacts_json = requests.get(f"{api_url}all_client_contacts/", json=client_data)

        nonlocal contacts_list
        contacts_list = {}
        
        # contacts_list = contacts_json.json()

        with open(r"data\data.json", "r") as file:
            contacts_list = json.load(file)
            contacts_list = json_searcher(contacts_list, "clientes", "contactos")

        nonlocal contacts_list_parsed
        contacts_list_parsed = []

        for contact in contacts_list:
            if client_name.value != "Otro":
                try:
                    contacts_list_parsed.append(contact)
                except TypeError:
                    print("Type Error!!")
                    print("No contact name grabbed from DB")
    
        contacts_list_parsed.append("Otro")

        contact_name.options = list(map(ft.dropdown.Option, contacts_list_parsed))

        page.update()

    def client_change(e):

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

            # add_plant_request = requests.post(url=f"{api_url}add_plant/", json=plant_data)

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

            # add_contact_request = requests.post(url=f"{api_url}add_contact/", json=contact_data)

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

    def send_all(e):
        # print(other_client_name.value + other_contact_name.value + other_plant_name.value)
        if other_client_name.value and other_contact_name.value and other_plant_name.value:
            # print("text")
            warning_text.visible = False
            # client_data = {
            #     "name" : other_client_name.value
            # }
            # plant_data = {
            #     "name" : other_plant_name.value,
            #     "client_name" : other_client_name.value
            # }
            # contact_data = {
            #     "name" : other_contact_name.value,
            #     "client_name" : other_client_name.value
            # }

            with open("data/data.json", "r", encoding="utf-8") as f:
                json_data = json.load(f)

            new_client_id = int(json_searcher(json_data, "clientes", "id")) + 1
            
            new_client_data = {
                "id": new_client_id,
                "name": other_client_name.value,
                "plantas": [other_plant_name.value],
                "contactos": [other_contact_name.value]
            }

            for Table in json_data["Tables"]:
                if Table["Name"] == "clientes":
                    Table["Data"].append(new_client_data)
            
            with open("data/data.json", "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=4)

            # add_client_request = requests.post(url=f"{api_url}add_client/", json=client_data)

            # add_plant_request = requests.post(url=f"{api_url}add_plant/", json=plant_data)

            # add_contact_request = requests.post(url=f"{api_url}add_contact/", json=contact_data)

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

    def click(e):
    #     print(box_group.value, inspectors_list)
    #     print(f"you click{job.value}")
        #hacer una función para que se guarde el reporte en la base de datos y se haga un numero de reporte
        #url = f"{api_url}?test={box_group.value}&report_num={box_group.value}-R-{year}-234&client_name={client_name_var}&plant={plant_name_var}&contact_name={contact.value}&part_desc={Description.value}&material={material.value}&heat={heat.value}&j_order={job_order.value}&j_qty={job.value}&od={od_val.value}&id={id_val.value}&width={thick_val.value}&height={height_val.value}&NDE={nde_val.value}&crit_accept={accept_val.value}&rough={surface_val.value}&uti_sn={uti_sn.value}&sn1={test_sn1.value}&d_cal={distance.value}&sens_block={sensitivity.value}&notch={notch.value}&rec_lvl={record.value}&ax_scanning={axial_x.value}&circ_ax_scanning={circumferental_x.value}&method={inspection.value}&coupling={coupling.value}&stage={inspector_s.value}&remarks={textarea.value}&insp_name={inspectors_list[0]}&ndt_act={ndt_act.value}"
        #print(url)

        with open(r"data/last_report.json", "r+", encoding="utf-8") as file:
            last_rep = json.load(file)
            last_rep["Last Report"] += 1
            file.seek(0)
            json.dump(last_rep, file)
            file.truncate()

        with open(r"data/data.json", "r+", encoding="utf-8") as file:
            db_json = json.load(file)

        try:
            data = {
                "parameters": {
                    "date":datetime.date.today(),
                    "report_num":last_rep["Last Report"],
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
                    "firma": f'<img src="data:image/png;base64, {firma}" alt="Firma" width="100%" height="100%"/>'
                    # "sens_meth1":test_sn_table.rows[0].cells[6].content.value,
                    # "ref_size1":(test_sn_table.rows[0].cells[7].content.controls[0].value + " " + test_sn_table.rows[0].cells[7].content.controls[1].value + test_sn_table.rows[0].cells[7].content.controls[1].suffix_text),
                    # "ref_level1": test_sn_table.rows[0].cells[8].content.value + " dB",
                    # "trans_cor1": test_sn_table.rows[0].cells[9].content.value + " dB",
                    # "scan_lev1": test_sn_table.rows[0].cells[10].content.value + " dB",
                    # "screen_range1": test_sn_table.rows[0].cells[11].content.value + '"',
                    # "scan_type1": test_sn_table.rows[0].cells[12].content.value
                }
            }
        except IndexError:
            print("Index Error in line 698, sn1")

        if check.value:
            data["parameters"]["acc_sn"] = sn.value
        else:
            data["parameters"]["rej_sn"] = sn.value

        uti_by_sn = json_searcher(db_json, "ut_instruments", search_param="sn", search=str(uti_sn.value.split()[1]))

        data["parameters"]["uti_brand"] = uti_by_sn["brand"]

        data["parameters"]["uti_model"] = uti_by_sn["model"]

        data["parameters"]["cal_date"] = uti_by_sn["calibration_date"]

        data["parameters"]["cal_due"] = uti_by_sn["calibration_due_date"]

        data["parameters"]["cert_lvl"] = json_searcher(db_json, "Inspectores", search_param="Name", search=inspectors_list[0])[f"{box_group.value}"]

        data["parameters"]["cert_due"] = json_searcher(db_json, "Inspectores", search_param="Name", search=inspectors_list[0])[f"{box_group.value}_due"]

        for i in test_sn_table.rows:
            data["parameters"]["calibrations"].append(
                {
                    "brand":i.cells[0].content.value,
                    "model":i.cells[1].content.value,
                    "sn":i.cells[2].content.value,
                    "freq":i.cells[3].content.value,
                    "size":i.cells[4].content.value,
                    "deg":i.cells[5].content.value,
                    "sens":i.cells[6].content.value, #formerly sens_meth
                    "ref":(i.cells[7].content.controls[0].value + " " + i.cells[7].content.controls[1].value + i.cells[7].content.controls[1].suffix_text), #formerly ref_size
                    "ref_l":i.cells[8].content.value + " dB", #formerly ref_level
                    "cor":i.cells[9].content.value + " dB", #formerly trans_cor
                    "scan":i.cells[10].content.value + " dB", #formerly scan_lev
                    "screen":i.cells[11].content.value + '"', #formerly screen_range
                    "scan_t":i.cells[12].content.value #formerly scan_type
                }
            )

        # print(requests.get(f"{api_url}Report_Number").text)

        #pdfurldownload = str(downloads_path) + "\\" + "Inspection_Report_" + str(box_group.value) + "-R-" + str(year) + "-" + str(db_json["Last Report"]) + ".pdf" #f"{downloads_path}\\Inspection Report {box_group.value}-R-{year}-{requests.get(f"{api_url}Report_Number")}.pdf"

        pdfurldownload = f"{downloads_path}\\Inspection_Report_{str(box_group.value)}-R-{str(year)}-{str(last_rep["Last Report"])}.pdf"

        print(pdfurldownload)

        
        environment = jinja2.Environment(loader=jinja2.FileSystemLoader(r"Templates/"))
        template = environment.get_template("PRUT.html")
        rendered_html = template.render(data)
        # print(template.render(data))
        # print(type(template.render(data)))
        relative_path = r"temp/temp_report.html"

        # html_path = os.path.abspath(relative_path).replace("\\", "/")
        # file_url = f"file:///{html_path}"

        print(f"URL Cargada: {relative_path}")
        print(f"Directorio actual: {os.getcwd()}")

        with open(relative_path, "w", encoding="utf-8") as file:
            file.write(rendered_html)

        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe")
            page = browser.new_page()
            
            #read html file
            with open(relative_path, "r", encoding="utf-8") as file:
                html_content = file.read()
            
            page.set_content(html_content)

            # page.goto(file_url)
            page.pdf(path=pdfurldownload, print_background=True)
            browser.close()

        # async with async_playwright() as p:
        #     browser = await p.chromium.launch()
        #     page = await browser.new_page()
        #     await page.goto(file_url)
        #     # html = requests.get(api_url, json=data)
        #     # no_new_line = html.content.decode("utf-8")
        #     # await page.set_content(no_new_line)
        #     await page.pdf(path=pdfurldownload, print_background=True)
        #     await browser.close()

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
        # uti_json = requests.get(f"{api_url}all_uti")
        # uti_list = uti_json.json()

        with open(r"data\data.json", "r") as file:
            uti_list = json.load(file)
            uti_list = json_searcher(uti_list, "ut_instruments")

        uti_list_parsed = []

        for uti in uti_list:
            uti_list_parsed.append(f"{uti["model"]} {uti["sn"]}")


        return uti_list_parsed

    uti_list_parsed = uti_list_maker()
    
    def uti_change(e):

        sn = e.control.value.split()[1]
        print(sn)

        # UTI = requests.get(f"{api_url}uti_by_sn", json={"sn": sn})

        # uti_dict = UTI.json()

        with open(r"data\data.json", "r") as file:
            uti_dict = json.load(file)
            uti_dict = json_searcher(json=uti_dict, table="ut_instruments", search_param="sn", search=sn)

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

    def distance_list_maker():
        # distance_json = requests.get(f"{api_url}all_distances")
        # distance_list = distance_json.json()
        # print(distance_list)

        with open(r"data\data.json", "r") as file:
            distance_list = json.load(file)
            for i in distance_list["Tables"]:
                if i["Name"] == "Distance Calibration":
                    distance_list = i["Data"]

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
        # sens_json = requests.get(f"{api_url}all_sensitivities")
        # sens_list = sens_json.json()

        with open(r"data\data.json", "r") as file:
            sens_list = json.load(file)
            for i in sens_list["Tables"]:
                if i["Name"] == "Sensitivity Block":
                    sens_list = i["Data"]

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
        # notch_json = requests.get(f"{api_url}all_notches")
        # notch_list = notch_json.json()

        with open(r"data\data.json", "r") as file:
            notch_list = json.load(file)
            for i in notch_list["Tables"]:
                if i["Name"] == "Notch Depth":
                    notch_list = i["Data"]

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
        # record_json = requests.get(f"{api_url}all_records")
        # record_list = record_json.json()

        with open(r"data\data.json", "r") as file:
            record_list = json.load(file)
            record_list = json_searcher(record_list, "Recording Level")

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
        # scanning_json = requests.get(f"{api_url}all_scannings")
        # scanning_list = scanning_json.json()

        with open(r"data\data.json", "r") as file:
            scanning_list = json.load(file)
            scanning_list = json_searcher(scanning_list, "Scanning Direction")

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
        # ins_json = requests.get(f"{api_url}all_inspection_info")
        # inspection_info = ins_json.json()

        with open(r"data\data.json", "r") as file:
            inspection_info = json.load(file)
            inspection_info = json_searcher(inspection_info, "Inspection Info")

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
    def test_sn_list_maker():
        # test_json = requests.get(f"{api_url}all_probes")
        # test_list = test_json.json()

        with open(r"data\data.json", "r") as file:
            test_list = json.load(file)
            test_list = test_list["Probe Data"]
            # for i in test_list["Tables"]:
            #     if i["Name"] == "Probe Data":
            #         test_list = i["Data"]

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
            # probe_sn_json = requests.get(f"{api_url}probes_by_sn", json={"sn" : sn})
            # probe_sn = probe_sn_json.json()

            with open(r"data\data.json", "r") as file:
                probe_sn = json.load(file)
                probe_sn = json_searcher(json=probe_sn, table="Probe Data", search_param="sn", search=sn)

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
        # SM_json = requests.get(f"{api_url}all_SM")
        # SM_list = SM_json.json()

        with open(r"data\data.json", "r") as file:
            SM_list = json.load(file)
            SM_list = SM_list["Sensitivity Method"]
            # for i in SM_list["Tables"]:
            #     if i["Name"] == "Sensitivity Method":
            #         SM_list = i["Data"]

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
        rows=[]
    )

    test_sn_table_column = ft.Column(
        controls=[
            ft.Container(content=ft.Column([ft.Row([test_sn_table], scroll=ft.ScrollMode.ALWAYS)], scroll=ft.ScrollMode.ALWAYS))
        ]
    )

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

    firma = ""

    def pick_files_result(e: ft.FilePickerResultEvent):
        nonlocal firma
        selected_files.value = (", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!")
        selected_files.update()
        # print(e.files[0].path)
        # print(Wiski64.Whiskey(str(e.files[0].path)))
        firma = Wiski64.Whiskey(e.files[0].path)


    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)

    page.overlay.append(pick_files_dialog)

    selected_files = ft.Text(size=12)

    # def bar_change(e):
    #     index = e.control.selected_index
    #     if index == 0:
    #         e.page.go(f"/main_screen")
    #     if index == 1:
    #         e.page.go(f"/admin")
    #     if index == 2:
    #         e.page.go(f"/")
    #     page.update()

    # NAV = ft.NavigationBar(
    #     destinations=[
    #         ft.NavigationBarDestination(icon=ft.Icons.EDIT_NOTE, label="Reporte"),
    #         ft.NavigationBarDestination(icon=ft.Icons.ADMIN_PANEL_SETTINGS, label="Admin"),
    #         ft.NavigationBarDestination(icon=ft.Icons.EXIT_TO_APP_SHARP, label="Exit")
    #     ],
    #     on_change=bar_change
    # )

    part_info_text = ft.Text(value="", visible=False)

    error_msg_text = ft.Text(value="", visible=False)

    def fab_action(e):
        e.page.go("/data")
        page.update()

    def route_chnage(route):

        page.views.clear()

        if page.route == "/main_screen":
            ins_control = reload_inspectors()
            page.views.append(
                ft.View(
                    "/main_screen",
                    scroll="always",
                    floating_action_button= ft.FloatingActionButton(
                        icon=ft.Icons.EDIT,
                        bgcolor=ft.Colors.PURPLE,
                        on_click=fab_action
                    ),   
                    horizontal_alignment="center",
                    vertical_alignment="center",
                    padding=0,
                    bgcolor=ft.Colors.BLUE_50,
                    controls=[
                        # NAV,
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
                                    height=180,
                                    width=400,
                                    content=ft.Column(
                                        horizontal_alignment="center",
                                        controls=[
                                            ft.ElevatedButton(
                                                content=ft.Text("Firmar",size=9),
                                                width=105,
                                                height=30,
                                                color="white",
                                                bgcolor='#924fcc',
                                                on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=False),
                                            ),
                                            selected_files,
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
        elif page.route == "/data":
            page.views.append(
                data.data_page()
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