import flet as ft
import json

'''
pasos para leer, mostrar y editar el json desde la app
1.- leer el json 
2.- guardar el json
3.- mostrar una tabla en pantalla por cada "tabla" del json
4.- cuando se edite algun dato, se guarda en el json del programa y se reescribe el archivo
5.- actualizar la pantalla, y recargar los datos
'''

inspector_column_names = ["delete", "id", "Name", "VT", "VT_due", "PT", "PT_due", "UT", "UT_due", "ET", "ET_due", "MT", "MT_due"]
client_column_names = ["delete", "id", "name", "plantas", "contactos"]

with open(r"data\data.json", "r", encoding="utf-8") as jsonfile:
    data_json = json.load(jsonfile)
    # print(data_json["Inspectores"][0]["Name"])

def reload_inspector_table():
    inspectors_table.rows = [ft.DataRow(cells=[ft.DataCell(ft.Row([ft.Text(data_json["Inspectores"][row][f"{col}"]), ft.IconButton(ft.Icons.EDIT, on_click=edit_inspector)])) if data_json["Inspectores"][row][f"{col}"] != None else ft.DataCell(ft.Row([ft.Text("NONE"), ft.IconButton(ft.Icons.EDIT, on_click=edit_inspector)])) for col in data_json["Inspectores"][0].keys()]) for row in range(0,len(data_json["Inspectores"]))]
    for row in inspectors_table.rows:
        row.cells.insert(0, ft.DataCell(ft.IconButton(ft.Icons.DELETE, on_click=delete_inspector)))
        # print(row.cells[2].content)
        row.cells[1].content.controls[1].visible = False
    
    inspectors_container.height = (len(inspectors_table.rows) * 50) + 200

def reload_clients_table():
    clients_table.rows = [ft.DataRow(cells=[ft.DataCell(ft.Row([ft.Text(data_json["clientes"][row][f"{col}"]), ft.IconButton(ft.Icons.EDIT, on_click=edit_clients)]) if col not in ("plantas", "contactos") else ft.Row(controls=[ft.Column([ft.Dropdown(options=list(map(ft.dropdown.Option, data_json["clientes"][row][f"{col}"])), width=300, height=50, text_size=15, on_click=lambda e: print(e.control.parent))]), ft.IconButton(ft.Icons.EDIT, on_click=edit_clients)]) ) if data_json["clientes"][row][f"{col}"] != None else ft.DataCell(ft.Row([ft.Text("NONE"), ft.IconButton(ft.Icons.EDIT, on_click=edit_clients)])) for col in data_json["clientes"][0].keys()]) for row in range(0,len(data_json["clientes"]))]
    for row in clients_table.rows:
        row.cells.insert(0, ft.DataCell(ft.IconButton(ft.Icons.DELETE, on_click=delete_client)))
        # print(row.cells[2].content)
        row.cells[1].content.controls[1].visible = False
        
        for i in [3,4]:
            row.cells[i].content.controls[0].width = 200
            row.cells[i].content.controls[0].controls[0].value = row.cells[i].content.controls[0].controls[0].options[0].key
    
    clients_container.height = (len(clients_table.rows) * 50) + 200

def accept_inspectors(e):
    # print(e.control.parent.controls[2].value) #text area value
    # print(e.control.parent.parent.parent.cells[1].content.controls[0].value) #id
    # print(e.control.parent.parent.parent.cells.index(e.control.parent.parent)) #column number
    text_area_value = e.control.parent.controls[2].value
    column_number = e.control.parent.parent.parent.cells.index(e.control.parent.parent)
    inspector_id = e.control.parent.parent.parent.cells[1].content.controls[0].value
    for inspector in data_json["Inspectores"]:
        if inspector["id"] == inspector_id:
            #cambiar el valor en el dict
            inspector[f"{inspector_column_names[column_number]}"] = text_area_value
            # print(f"data_json[f\"{inspectors_table.columns[column_number]}\"] = {data_json[f"{inspectors_table.columns[column_number]}"]}")
            # print(inspector)
    
    # print(data_json)

    for i in [0,1]:
        e.control.parent.controls[i].visible = True
    for i in [2,3,4]:
        e.control.parent.controls[i].visible = False

    reload_inspector_table()

    # inspectors_table.rows = [ft.DataRow(cells=[ft.DataCell(ft.Row([ft.Text(data_json["Inspectores"][row][f"{col}"]), ft.IconButton(ft.Icons.EDIT, on_click=edit_inspector)])) if data_json["Inspectores"][row][f"{col}"] != None else ft.DataCell(ft.Row([ft.Text("NONE"), ft.IconButton(ft.Icons.EDIT, on_click=edit_inspector)])) for col in data_json["Inspectores"][0].keys()]) for row in range(0,len(data_json["Inspectores"]))]
    # for row in inspectors_table.rows:
    #     row.cells.insert(0, ft.DataCell(ft.IconButton(ft.Icons.DELETE, on_click=delete_inspector)))
    #     print(row.cells[2].content)
    #     row.cells[1].content.controls[1].visible = False
    
    with open(r"data\data.json", "w", encoding="utf-8") as jsonfile:
        json.dump(data_json, jsonfile, indent=4)

    e.page.update()

def accept_clients(e):
    # print(e.control.parent.controls[2].value) #text area value
    # print(e.control.parent.parent.parent.cells[1].content.controls[0].value) #id
    # print(e.control.parent.parent.parent.cells.index(e.control.parent.parent)) #column number
    text_area_value = e.control.parent.controls[2].value
    column_number = e.control.parent.parent.parent.cells.index(e.control.parent.parent)
    client_id = e.control.parent.parent.parent.cells[1].content.controls[0].value
    for client in data_json["clientes"]:
        if client["id"] == client_id:
            #cambiar el valor en el dict
            client[f"{client_column_names[column_number]}"] = text_area_value
            # print(f"data_json[f\"{inspectors_table.columns[column_number]}\"] = {data_json[f"{inspectors_table.columns[column_number]}"]}")
            # print(inspector)
    
    # print(data_json)

    for i in [0,1]:
        e.control.parent.controls[i].visible = True
    for i in [2,3,4]:
        e.control.parent.controls[i].visible = False

    reload_clients_table()

    # inspectors_table.rows = [ft.DataRow(cells=[ft.DataCell(ft.Row([ft.Text(data_json["Inspectores"][row][f"{col}"]), ft.IconButton(ft.Icons.EDIT, on_click=edit_inspector)])) if data_json["Inspectores"][row][f"{col}"] != None else ft.DataCell(ft.Row([ft.Text("NONE"), ft.IconButton(ft.Icons.EDIT, on_click=edit_inspector)])) for col in data_json["Inspectores"][0].keys()]) for row in range(0,len(data_json["Inspectores"]))]
    # for row in inspectors_table.rows:
    #     row.cells.insert(0, ft.DataCell(ft.IconButton(ft.Icons.DELETE, on_click=delete_inspector)))
    #     print(row.cells[2].content)
    #     row.cells[1].content.controls[1].visible = False
    
    with open(r"data\data.json", "w", encoding="utf-8") as jsonfile:
        json.dump(data_json, jsonfile, indent=4)

    e.page.update()

def cancel(e):
    # print(e.control.parent)
    for i in [0,1]:
        e.control.parent.controls[i].visible = True
    for i in [2,3,4]:
        e.control.parent.controls[i].visible = False
    
    e.page.update()

def editing_box(value: str):
    return [ft.TextField(value=value, width=200), ft.IconButton(ft.Icons.CHECK, on_click=accept_inspectors), ft.IconButton(ft.Icons.CLOSE, on_click=cancel)]

def edit_inspector(e):
    # print(e.control)
    e.control.parent.width = 300
    text_value = e.control.parent.controls[0].value
    text_control = e.control.parent.controls[0]
    icon_control = e.control.parent.controls[1]
    text_control.visible = False
    icon_control.visible = False

    # print(len(e.control.parent.controls))
    if len(e.control.parent.controls) == 2:

        for control in editing_box(text_value):
            e.control.parent.controls.append(control)
    else:
        for i in [2,3,4]:
            e.control.parent.controls[i].visible = True
        pass

    e.page.update()

def edit_clients(e):
    print(e.control.parent)
    e.control.parent.width = 300
    text_value = e.control.parent.controls[0].value
    text_control = e.control.parent.controls[0]
    icon_control = e.control.parent.controls[1]
    text_control.visible = False
    icon_control.visible = False

    # print(len(e.control.parent.controls))
    if len(e.control.parent.controls) == 2:

        for control in editing_box(text_value):
            e.control.parent.controls.append(control)
    else:
        for i in [2,3,4]:
            e.control.parent.controls[i].visible = True
        pass

    e.page.update()

inspectors_table = ft.DataTable(
    show_checkbox_column=True,
    columns=[
        ft.DataColumn(
            ft.Text("Delete")
        ),
        ft.DataColumn(
            ft.Text("Id"),
        ),
        ft.DataColumn(
            ft.Text("Name"),
        ),
        ft.DataColumn(
            ft.Text("VT"),
        ),
        ft.DataColumn(
            ft.Text("VT Due"),
        ),
        ft.DataColumn(
             ft.Text("PT"),
        ),
        ft.DataColumn(
            ft.Text("PT Due"),
        ),
        ft.DataColumn(
            ft.Text("UT"),
        ),
        ft.DataColumn(
            ft.Text("UT Due")
        ),
        ft.DataColumn(
            ft.Text("ET")
        ),
        ft.DataColumn(
            ft.Text("ET Due")
        ),
        ft.DataColumn(
            ft.Text("MT")
        ),
        ft.DataColumn(
            ft.Text("MT Due")
        )
    ], 
        rows = [ft.DataRow(cells=[ft.DataCell(ft.Row([ft.Text(data_json["Inspectores"][row][f"{col}"]), ft.IconButton(ft.Icons.EDIT, on_click=edit_inspector)])) if data_json["Inspectores"][row][f"{col}"] != None else ft.DataCell(ft.Row([ft.Text("NONE"), ft.IconButton(ft.Icons.EDIT, on_click=edit_inspector)])) for col in data_json["Inspectores"][0].keys()]) for row in range(0,len(data_json["Inspectores"]))]
)

clients_table = ft.DataTable(
    show_checkbox_column=True,
    columns=[
        ft.DataColumn(
            ft.Text("Delete")
        ),
        ft.DataColumn(
            ft.Text("Id"),
        ),
        ft.DataColumn(
            ft.Text("Name"),
        ),
        ft.DataColumn(
            ft.Text("Plantas"),
        ),
        ft.DataColumn(
            ft.Text("Contactos"),
        )
    ], 
        rows = [ft.DataRow(cells=[ft.DataCell(ft.Row([ft.Text(data_json["clientes"][row][f"{col}"]), ft.IconButton(ft.Icons.EDIT, on_click=edit_clients)]) if col not in ("plantas", "contactos") else ft.Row(controls=[ft.Column([ft.Dropdown(options=list(map(ft.dropdown.Option, data_json["clientes"][row][f"{col}"])), width=300, height=50, text_size=15, on_click=lambda e: print(e.control.parent))]), ft.IconButton(ft.Icons.EDIT, on_click=edit_clients)]) ) if data_json["clientes"][row][f"{col}"] != None else ft.DataCell(ft.Row([ft.Text("NONE"), ft.IconButton(ft.Icons.EDIT, on_click=edit_clients)])) for col in data_json["clientes"][0].keys()]) for row in range(0,len(data_json["clientes"]))]
)

def delete_inspector(e):
    # print(e.control.parent.parent.cells[1].content.value)
    # for inspector in data_json["Inspectores"]:
    #     if inspector["id"] ==  e.control.parent.parent.cells[1].content.value:
    data_json["Inspectores"] = [ins for ins in data_json["Inspectores"] if ins["id"] != e.control.parent.parent.cells[1].content.controls[0].value]
    reload_inspector_table()
    # inspectors_table.rows = [ft.DataRow(cells=[ft.DataCell(ft.Row([ft.Text(data_json["Inspectores"][row][f"{col}"]), ft.IconButton(ft.Icons.EDIT, on_click=edit_inspector)])) if data_json["Inspectores"][row][f"{col}"] != None else ft.DataCell(ft.Row([ft.Text("NONE"), ft.IconButton(ft.Icons.EDIT, on_click=edit_inspector)])) for col in data_json["Inspectores"][0].keys()]) for row in range(0,len(data_json["Inspectores"]))]
    # for row in inspectors_table.rows:
    #     row.cells.insert(0, ft.DataCell(ft.IconButton(ft.Icons.DELETE, on_click=delete_inspector)))
    #     print(row.cells[2].content)
    #     row.cells[1].content.controls[1].visible = False

    with open(r"data\data.json", "w", encoding="utf-8") as jsonfile:
        json.dump(data_json, jsonfile, indent=4)
    e.page.update()

def delete_client(e):
    # print(e.control.parent.parent.cells[1].content.value)
    # for inspector in data_json["Inspectores"]:
    #     if inspector["id"] ==  e.control.parent.parent.cells[1].content.value:
    data_json["clientes"] = [client for client in data_json["clientes"] if client["id"] != e.control.parent.parent.cells[1].content.controls[0].value]
    reload_clients_table()
    # inspectors_table.rows = [ft.DataRow(cells=[ft.DataCell(ft.Row([ft.Text(data_json["Inspectores"][row][f"{col}"]), ft.IconButton(ft.Icons.EDIT, on_click=edit_inspector)])) if data_json["Inspectores"][row][f"{col}"] != None else ft.DataCell(ft.Row([ft.Text("NONE"), ft.IconButton(ft.Icons.EDIT, on_click=edit_inspector)])) for col in data_json["Inspectores"][0].keys()]) for row in range(0,len(data_json["Inspectores"]))]
    # for row in inspectors_table.rows:
    #     row.cells.insert(0, ft.DataCell(ft.IconButton(ft.Icons.DELETE, on_click=delete_inspector)))
    #     print(row.cells[2].content)
    #     row.cells[1].content.controls[1].visible = False

    with open(r"data\data.json", "w", encoding="utf-8") as jsonfile:
        json.dump(data_json, jsonfile, indent=4)
    e.page.update()

#fill inspectors table with delete button
for row in inspectors_table.rows:
    row.cells.insert(0, ft.DataCell(ft.IconButton(ft.Icons.DELETE, on_click=delete_inspector)))
    # print(row.cells[1].content.controls[1].visible)
    row.cells[1].content.controls[1].visible = False

#fill clients table with delete button
for row in clients_table.rows:
    row.cells.insert(0, ft.DataCell(ft.IconButton(ft.Icons.DELETE, on_click=delete_client)))
    # print(row.cells[1].content.controls[1].visible)
    row.cells[1].content.controls[1].visible = False
    for i in [3,4]:
        # print(row.cells[i].content)#column
        row.cells[i].content.controls[0].width = 200
        # print(row.cells[i].content.controls[0])#dropdown
        # row.cells[i].content.width = 600
        # print(row.cells[i].content.controls[0].options)#options
        # print(row.cells[i].content.controls[0])#dropdown
        # print(row.cells[i].content.controls[0].value)#dropdown value
        row.cells[i].content.controls[0].controls[0].value = row.cells[i].content.controls[0].controls[0].options[0].key



def new_inspector(e):
    id_list = []
    for row in inspectors_table.rows:
        id_list.append(row.cells[1].content.controls[0].value)
    max_id = max(id_list) if id_list else 0
        # print(row.cells[1].content.controls[0].value)
    data_json["Inspectores"].append({
            "id": max_id + 1,
            "Name": None,
            "VT": None,
            "VT_due": None,
            "PT": None,
            "PT_due": None,
            "UT": None,
            "UT_due": None,
            "ET": None,
            "ET_due": None,
            "MT": None,
            "MT_due": None
        })
    reload_inspector_table()
    e.page.update()

inspectors_table_column = ft.Column(
    controls=[
        ft.Container(content=ft.Column([ft.Row([inspectors_table], scroll=ft.ScrollMode.ALWAYS), ft.Row([ft.IconButton(ft.Icons.ADD, on_click=new_inspector)])], scroll=ft.ScrollMode.ALWAYS))
    ]
)

inspectors_container = ft.Container(
    width=400,
    height=(50 * len(inspectors_table.rows)) + 200,
    padding=ft.padding.only(top=10),
    bgcolor=ft.Colors.WHITE,
    content=ft.Column(
        horizontal_alignment="center",
        controls=[
            ft.Text("Inspectors", text_align="center", size=25, weight="bold", color="black"),
            inspectors_table_column,
        ]
    )
)

clients_table_column = ft.Column(
    controls=[
        ft.Container(content=ft.Column([ft.Row([clients_table], scroll=ft.ScrollMode.ALWAYS), ft.Row([ft.IconButton(ft.Icons.ADD, on_click=new_inspector)])], scroll=ft.ScrollMode.ALWAYS))
    ]
)

clients_container = ft.Container(
    width=400,
    height=(50 * len(clients_table.rows)) + 200,
    padding=ft.padding.only(top=10),
    bgcolor=ft.Colors.WHITE,
    content=ft.Column(
        horizontal_alignment="center",
        controls=[
            ft.Text("Clients", text_align="center", size=25, weight="bold", color="black"),
            clients_table_column,
        ]
    )
)

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
        controls=[
            ft.SafeArea(
                ft.Container(
                    height=10,
                    expand=True,
                    bgcolor=ft.Colors.PURPLE,
                ),
            ),
            inspectors_container,
            clients_container
        ]
    )