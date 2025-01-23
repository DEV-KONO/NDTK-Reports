#http://127.0.0.1:8000/?model_report["test"]=UT&report_num=UT-R-2024-234&client_name=Liebher&plant=garcia&contact_name=luis%20Gerardo&part_desc=descpartegenerica&material=acero&heat=colada%20generica&j_order=orden%20de%20trabajo&j_qty=2&od=23.5&id=24.5&width=22.9&height=33.5&NDE=normal%20spec&crit_accept=criterio%20base&rough=machined%20condition&uti_sn=289703&sn1=232739&sn2=223399&d_cal=cal%20distance&sens_block=astm%20flat&notch=model_report["test"]%20notch&rec_lvl=model_report["test"]%20rec%20lvl&ax_scanning=model_report["test"]%20ax%20scanning&circ_ax_scanning=circ%20ax&method=model_report["test"]%20method&coupling=model_report["test"]%20coupling&stage=model_report["test"]%20stage&remarks=model_report["test"]%20remark%20large%20data&&insp_name=Samuel%kono%peralta&cert_lvl=NDT%20Nivel%202&ndt_act=realizo%20y%20evaluo&cert_due=20%20mar%202025&rej_sn=223344from ast import Name
import datetime
import hashlib
import json
import secrets
import string
import traceback
import pdfkit
import os
from schemas import *
from sqlalchemy.orm import sessionmaker
from models import NDE, Acabado, Acceptance, Admins, Agent, Clients, Contacts, Instrument, Inspector, Method, Plants, Recording, Reports, Scanning, Sensitivity, Stage, engine, Distance, Notch, Probe, Sensitivity_Method, Ref_Size, Ref_Level, Trans_Corr, Scan_level, Screen_Range, Scan_Type
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pyrebase import *
from requests import HTTPError
#from playwright.sync_api import sync_playwright, Playwright 
#from jinja2 import Environment, FileSystemLoader

Session = sessionmaker(bind=engine)

session = Session()

app = FastAPI(template_folder = "plantillas")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="plantillas")

# template_loader = FileSystemLoader('plantllas')
# template_env = Environment(loader=template_loader)

# html_template = r"PRUT.html"
# template = template_env.get_template(html_template)

config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

load_dotenv()

pyrebase_config = {
    "apiKey": os.getenv("apiKey"),
    "authDomain": os.getenv("authDomain"),
    "databaseURL": os.getenv("databaseURL"),
    "storageBucket": os.getenv("storageBucket"),
    "serviceAccount": os.getenv("serviceAccount")
}

firebase = initialize_app(pyrebase_config)

auth = firebase.auth()

#date maker
def date():
    x = datetime.datetime.now()
    return x.strftime("%A %d %Y")

#Function that fills the report number
def report_num(test: str):
    year = datetime.datetime.now()
    last_report_number = session.query(Reports.Report_Num).all()

    report_number = last_report_number[-1][0] + 1
    
    try:
        return f"{test}-R-{year.strftime("%Y")}-{report_number:03}"
    except IndexError:
        return f"{test}-R-{year.strftime("%Y")}-1"
        

#Function that returns the data from the UT instrument DB
def retrieve_instrument_by_sn(serialnum: int):
    instrument = session.query(Instrument).filter_by(sn=serialnum).one_or_none()
    return instrument

#Function that returns the data from the calibration setup DB
def retrieve_setup_by_sn(serialnum: int):
    setup =  session.query(Probe).filter_by(sn=serialnum).one_or_none()
    return setup

def retun_all_instruments():
    return session.query(Instrument).all()

def ret_cert_lvl(inspector, test):
    if test == "UT":
        return session.query(Inspector.UT).filter_by(name=inspector).one_or_none()[0]

def ret_cert_due(inspector, test):
    if test == "UT":
        print(type(session.query(Inspector.UT_due).filter_by(name=inspector).one_or_none()[0].strftime('%Y-%m-%d')))
        return session.query(Inspector.UT_due).filter_by(name=inspector).one_or_none()[0].strftime('%Y-%m-%d')

def val_ins_fun(inspector: str):
    return session.query(Inspector).filter_by(name=inspector).one_or_none()

@app.get("/all_inspection_info")
async def inspection_info():
    method = session.query(Method).all()
    agent = session.query(Agent).all()
    stage = session.query(Stage).all()

    try:
        return {
            "method" : method,
            "agent" : agent,
            "stage" : stage
        }
    except AttributeError:
        return { "msg": "INSPECTION INFORMATION ERROR CHECK LINE 90 CALL AN ADMINISTRATOR" }


@app.get("/all_distances")
async def all_distances():
    distances = session.query(Distance).all()

    try:
        return distances
    except:
        return { "msg": "Something went wrong in line 108, contact an administrator. DISTANCE CALIBRATION ERROR." }
    
@app.get("/all_sensitivities")
async def all_sensitivities():
    sensitivity = session.query(Sensitivity).all()

    try:
        return sensitivity
    except:
        return { "msg": "Something went wrong in line 117, contact an administrator. SENSITIVITY ERROR." }

@app.get("/all_notches")
async def all_notches():
    notch = session.query(Notch).all()

    try:
        return notch
    except:
        return { "msg": "Something went wrong in line 126, contact an administrator. NOTCH ERROR." }

@app.get("/all_records")
async def all_records():
    recording = session.query(Recording).all()

    try:
        return recording
    except:
        return { "msg": "Something went wrong in line 135, contact an administrator. RECORDING ERROR." }

@app.get("/all_scannings")
async def all_scanning():
    scanning = session.query(Scanning).all()

    try:
        return scanning
    except:
        return { "msg": "Something went wrong in line 144, contact an administrator. SCANNING ERROR." }

@app.put("/change_admin")
async def changeAdminStatus(schema_email: Schema_Email):
    email_dump = schema_email.model_dump()
    email = email_dump["email"]
    admin = session.query(Admins).filter_by(email=email).one_or_none()

    admin.admin = not admin.admin

    session.commit()

    admin = session.query(Admins).filter_by(email=email).one_or_none()

    return admin.admin

@app.get("/all_admins")
async def getAllAdmins():
    return  session.query(Admins).all()

@app.get("/inspector_exists")
async def val_ins(inspector: str):
    if val_ins_fun(inspector):
        return True
    else:
        return False
    
@app.post("/add_inspector")
async def add_ins(schemainspector: Schema_Inspector):
    inspector = schemainspector.model_dump()
    
    if not val_ins_fun(inspector=inspector["name"]):

        new_ins = Inspector(name=inspector["name"])

        session.add(new_ins)
        session.commit()

        return { 
            "error" : False, 
            "msg" : f"Inspector {inspector["name"]} added correctly"
            }
    else:
        return {
            "error" : True,
            "msg" : f"Inspector {inspector["name"]} already exists"
        }

@app.get("/validate_admin")
async def validate(email: Schema_Email):
    email_dump =  email.model_dump()["email"]
    admin_user_query = session.query(Admins).filter_by(email=email_dump).one_or_none()

    return admin_user_query


@app.get("/login")
async def login(schemauser: Schema_User):

    h = hashlib.new(os.getenv("hash"))

    user = schemauser.model_dump()
    error_msg = ""
    try:
        admin_query = session.query(Admins).filter_by(email=user["email"]).one_or_none()

        salt = admin_query.salt

        h.update(user["password"].encode())
        h.update(salt.encode())

        hashed_password = h.hexdigest()

        userlogin = auth.sign_in_with_email_and_password(user["email"], hashed_password)

        return {
            "error": False,
            "mail": userlogin["email"]
            }
    
    except HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        #traceback.print_exc()

        if error == "INVALID_LOGIN_CREDENTIALS":
            # login_text.visible = True
            error_msg = "El usuario o contraseña son invalidos"
        elif error == "MISSING_PASSWORD":
            # login_text.visible = True
            error_msg = "Ingrese una contraseña"
        elif error == "INVALID_EMAIL":
            # login_text.visible = True
            error_msg = "Ingrese un correo valido"
        elif error == "TOO_MANY_ATTEMPTS_TRY_LATER : Access to this account has been temporarily disabled due to many failed login attempts. You can immediately restore it by resetting your password or you can try again later.":
            error_msg = "Demasiados intentos, intente nuevamente"

        return {
            "error": True,
            "visible" : True,
            "error_msg" : error_msg
        }   
    
    except AttributeError:
        return {
            "error": True,
            "visible" : True,
            "error_msg" : "El correo no existe, si el error persiste, contacte a soporte"
        }

@app.post("/register")
async def register(schemaregister: Schema_Register):

    h = hashlib.new(os.getenv("hash"))

    register = schemaregister.model_dump()

    h.update(register["password"].encode())

    salt = ''.join(secrets.choice(string.ascii_letters + string.punctuation + string.digits) for i in range(64))

    h.update(salt.encode())
    password_hash = h.hexdigest()

    try:
        if register["password"] != register["confpassword"]:
            error_msg = "Las contraseñas no coinciden"
            return {
                "error": True,
                "visible" : True,
                "error_msg" : error_msg
            }
        else:
            registerUser = auth.create_user_with_email_and_password(register["email"], password_hash)
            msg = "Usuario Creado correctamente, puede regresar para loggearse"

            new_user = Admins(email=register["email"], username=register["user"], salt=salt)

            session.add(new_user)
            session.commit()

            return {
                "error": False,
                "visible" : True,
                "message" : msg
            }

    except HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        # traceback.print_exc()
        if error == "WEAK_PASSWORD : Password should be at least 6 characters":
            #print("weak password")
            error_msg = "la contraseña debe tener más de 6 caracteres"
            
            return {
                "error": True,
                "visible" : True,
                "error_msg" : error_msg
            }

        elif error == "EMAIL_EXISTS":
            error_msg = "El correo ingresado ya existe"
            return {
                "error": True,
                "visible" : True,
                "error_msg" : error_msg
            }
        elif error == "INVALID_EMAIL":
            error_msg = "El correo es invalido"
            return {
                "error": True,
                "visible" : True,
                "error_msg" : error_msg
            }
    except Exception:
        traceback.print_exc()

@app.post("/add_criteria")
async def add_acc_criteria(acceptance: Schema_Acceptance):
    model_acc = acceptance.model_dump()
    acceptance_criteria = model_acc["acceptance"]
    nde_spec = model_acc["nde_spec"]

    new_acc_crit = Acceptance(acceptance_criteria=acceptance_criteria)

    nde_query = session.query(NDE).filter_by(nde_spec=nde_spec).one_or_none()
    nde_query.acceptance.append(new_acc_crit)
    session.add(new_acc_crit)

    session.commit()

    return {"msg" : f"{acceptance_criteria} added into {nde_spec}"}

@app.post("/add_nde")
async def add_nde(nde: Schema_NDE):
    model_nde = nde.model_dump()
    nde_spec = model_nde["nde_spec"]
    client_name = model_nde["client_name"]

    new_nde = NDE(nde_spec=nde_spec)

    client = session.query(Clients).filter_by(name=client_name).one_or_none()
    client.nde.append(new_nde)
    session.add(new_nde)

    session.commit()

    return {"msg": f"nde spec:{nde_spec} was submitted correctly to client: {client_name}"}

@app.post("/add_acabado")
async def add_nde(acabado: Schema_Acabado):
    model_acabado = acabado.model_dump()
    acabado_superficial = model_acabado["acabado"]

    new_acabado = Acabado(acabado=acabado_superficial)

    session.add(new_acabado)

    session.commit()

    return {"msg": f"Acabado Superficial: {acabado_superficial} was submitted correctly."}

@app.get("/all_acabados")
async def return_all_roughnesses():
    rough = session.query(Acabado).all()

    try:
        return rough
    except:
        return { "msg": "ROUGHNESS ERROR CHECK LINE 374" }

@app.get("/all_nde")
async def return_nde():
    nde = session.query(NDE).all()

    try:
        return nde
    except AttributeError:
        return { "msg": "Check the name, it may be wrong" }    

@app.get("/all_nde_criteria")
async def return_criteria_by_nde(nde: Schema_NDE):
    model_nde = nde.model_dump()
    nde_spec = model_nde["nde_spec"]

    nde_query = session.query(NDE).filter_by(nde_spec=nde_spec).one_or_none()

    try:
        return nde_query.acceptance
    except AttributeError:
        return { "msg": "Check the name, it may be wrong" }


@app.get("/all_probes")
async def return_probes():
    probes = session.query(Probe).all()
    return probes

# @app.get("/all_setups")
# async def return_setups():
#     setups = session.query(Calibration).all()

#     return setups

@app.get("/probes_by_sn")
async def return_probes_by_sn(sn: Schema_Just_UTI_SN):
    model_sn = sn.model_dump()
    sn = model_sn["sn"]

    probe = session.query(Probe).filter_by(sn=sn).one_or_none()
    return probe

# @app.get("/setups_by_sn")
# async def return_setups_by_sn(sn: Schema_Just_UTI_SN):
#     model_sn = sn.model_dump()
#     sn = model_sn["sn"]

#     setup = session.query(Calibration).filter_by(sn=sn).one_or_none()

#     return setup

@app.get("/all_inspectors")
async def return_inspectores():
    #return jsonable_encoder(session.query(Inspector).all())

    inspectors = session.query(Inspector).all()

    return inspectors

@app.get("/all_SM")
async def all_sensitivity_methods():

    SM = session.query(Sensitivity_Method).all()

    return SM

@app.post("/add_contact/")
async def add_contact(Contact: Schema_Contacts):
    model_contact = Contact.model_dump()
    contact_name = model_contact["name"]
    client_name = model_contact["client_name"]

    new_contact = Contacts(name=contact_name)
    client = session.query(Clients).filter_by(name=client_name).one_or_none()
    client.contacts.append(new_contact)
    session.add(new_contact)

    session.commit()

    return {"msg": f"{contact_name} contact was submitted correctly to client {client_name}"} #client.contacts

@app.get("/all_client_contacts/")
async def return_client_contacts(Client: Schema_Client):
    model_client = Client.model_dump()
    client_name = model_client["name"]

    client = session.query(Clients).filter_by(name=client_name).one_or_none()

    try:
        return client.contacts
    except AttributeError:
        return { "msg": "Check the name, it may be wrong" }
    
@app.get("/uti_by_sn")
async def get_uti_by_sn(serial_number: Schema_Just_UTI_SN):
    model_just_uti_sn = serial_number.model_dump()
    sn = model_just_uti_sn["sn"]

    uti = session.query(Instrument).filter_by(sn=sn).one_or_none()

    return uti

@app.post("/add_plant/")
async def add_plant(Plant: Schema_Plants):
    model_plant = Plant.model_dump()
    plant_name = model_plant["name"]
    client_name = model_plant["client_name"]

    new_plant = Plants(name=plant_name)
    client = session.query(Clients).filter_by(name=client_name).one_or_none()
    print(client)
    client.plants.append(new_plant)
    session.add(new_plant)

    session.commit()

    return {"msg": f"{plant_name} plant was submitted correctly to client {client_name}"} #client.plants

@app.get("/all_uti")
async def return_all_UTI():
    uti = session.query(Instrument).all()

    return uti

@app.get("/all_client_plants/")
async def return_client_plants(Client: Schema_Client):
    model_client = Client.model_dump()
    client_name = model_client["name"]
    client = session.query(Clients).filter_by(name=client_name).one_or_none()

    try:
        return client.plants
    except AttributeError:
        return { "msg": "Check the name, it may be wrong" }

@app.post("/add_client/")
async def add_client(Client: Schema_Client):
    model_client = Client.model_dump()
    name = model_client["name"]

    if not session.query(Clients).filter_by(name=name).one_or_none():
        new_client = Clients(name=name)
        session.add(new_client)
        session.commit()
    else:
        return { "error" : "Client already exists!!"}


    if not name:
        return { "error" : "No client name provided"}
    elif name == "nt":
        return { "error" : "nt as client name, something might had gone wrong"}
    else:
        try:
            return {
                "msg" : f"Client {name} added successfully",
                "error" : False
            }
        except:
            return { "error": "error name"}

@app.get("/all_clients")
async def return_clientes():
    clients = session.query(Clients).all() #jsonable_encoder(session.query(Client).all())
    return clients

@app.get('/Report_Number')
async def return_last_report_num():
    report_number = session.query(Reports.Report_Num).all()[-1][0] + 1
    return f"{report_number:03}"

@app.get('/')
async def template(request: Request, Report: Schema_Report):

    model_report = Report.model_dump()
    print(type(model_report))

    #year date
    year = datetime.datetime.now().year

    # environment = Environment(loader=FileSystemLoader("plantillas"))
    results_filename = model_report["test"] + "-R-" + str(year)
    # results_template = environment.get_template("PRUT.html")

    cert_lvl = ret_cert_lvl(model_report["insp_name"], model_report["test"])
    cert_due = ret_cert_due(model_report["insp_name"], model_report["test"])

    if model_report["test"] == "UT":
        instrument = retrieve_instrument_by_sn(model_report["uti_sn"])
        print(instrument.calibration_date, instrument.calibration_due_date)
        # setup1 = retrieve_setup_by_sn(model_report["sn1"])
        # setup2 = retrieve_setup_by_sn(model_report["sn2"])
        # setup3 = retrieve_setup_by_sn(model_report["sn3"])
        # setup4 = retrieve_setup_by_sn(model_report["sn4"])
        # setup5 = retrieve_setup_by_sn(model_report["sn5"])

        if model_report["acc_sn"]:
            model_report["rej_sn"] = ""
        else:
            model_report["acc_sn"] = ""

        parameters = {
            "request": request, 
            "test":model_report["test"], 
            "report_num":report_num(model_report["test"]), 
            "date":date(), 
            "client_name":model_report["client_name"], 
            "plant":model_report["plant"],
            "contact_name":model_report["contact_name"],
            "part_desc":model_report["part_desc"],
            "material":model_report["material"],
            "heat":model_report["heat"],
            "j_order":model_report["j_order"],
            "j_qty":model_report["j_qty"],
            "od":model_report["od"],
            "id":model_report["id"],
            "width":model_report["width"],
            "height":model_report["height"],
            "NDE":model_report["NDE"],
            "crit_accept":model_report["crit_accept"],
            "rough":model_report["rough"],
            "uti_brand":instrument.brand,
            "uti_model":instrument.model,
            "uti_sn":model_report["uti_sn"],
            "cal_date":instrument.calibration_date.strftime('%Y-%m-%d'),
            "cal_due":instrument.calibration_due_date.strftime('%Y-%m-%d'),
            "calibrations":model_report["calibrations"],
            # "sn1":model_report["sn1"],
            # "brand1":setup1.brand,
            # "model1":setup1.model,
            # "freq1":setup1.frequency,
            # "size1":setup1.size,
            # "deg1":setup1.angle,
            # "sens1":setup1.sensitivity,
            # "ref1":setup1.reference_size,
            # "ref_l1":setup1.reference_level,
            # "cor1":setup1.transfer_correction,
            # "scan1":setup1.scanning_level,
            # "screen1":setup1.screen_range,
            # "scan_t1":setup1.scan_type,
            "d_cal":model_report["d_cal"],
            "sens_block":model_report["sens_block"],
            "notch":model_report["notch"],
            "rec_lvl":model_report["rec_lvl"],
            "ax_scanning":model_report["ax_scanning"],
            "circ_ax_scanning":model_report["circ_ax_scanning"],
            "method":model_report["method"],
            "coupling":model_report["coupling"],
            "stage":model_report["stage"],
            "remarks":model_report["remarks"],
            "insp_name":model_report["insp_name"],
            "cert_lvl":cert_lvl,
            "ndt_act":model_report["ndt_act"],
            "cert_due":cert_due,
            "acc_sn":model_report["acc_sn"],
            "rej_sn":model_report["rej_sn"],
            # "sn2":model_report["sn2"],
            # "brand2":setup2.brand,
            # "model2":setup2.model,
            # "freq2":setup2.frequency,
            # "size2":setup2.size,
            # "deg2":setup2.angle,
            # "sens2":setup2.sensitivity,
            # "ref2":setup2.reference_size,
            # "ref_l2":setup2.reference_level,
            # "cor2":setup2.transfer_correction,
            # "scan2":setup2.scanning_level,
            # "screen2":setup2.screen_range,
            # "scan_t2":setup2.scan_type,
            # "sn3":model_report["sn3"],
            # "brand3":setup3.brand,
            # "model3":setup3.model,
            # "freq3":setup3.frequency,
            # "size3":setup3.size,
            # "deg3":setup3.angle,
            # "sens3":setup3.sensitivity,
            # "ref3":setup3.reference_size,
            # "ref_l3":setup3.reference_level,
            # "cor3":setup3.transfer_correction,
            # "scan3":setup3.scanning_level,
            # "screen3":setup3.screen_range,
            # "scan_t3":setup3.scan_type,
            # "sn4":model_report["sn4"],
            # "brand4":setup4.brand,
            # "model4":setup4.model,
            # "freq4":setup4.frequency,
            # "size4":setup4.size,
            # "deg4":setup4.angle,
            # "sens4":setup4.sensitivity,
            # "ref4":setup4.reference_size,
            # "ref_l4":setup4.reference_level,
            # "cor4":setup4.transfer_correction,
            # "scan4":setup4.scanning_level,
            # "screen4":setup4.screen_range,
            # "scan_t4":setup4.scan_type,
            # "sn5":model_report["sn5"],
            # "brand5":setup5.brand,
            # "model5":setup5.model,
            # "freq5":setup5.frequency,
            # "size5":setup5.size,
            # "deg5":setup5.angle,
            # "sens5":setup5.sensitivity,
            # "ref5":setup5.reference_size,
            # "ref_l5":setup5.reference_level,
            # "cor5":setup5.transfer_correction,
            # "scan5":setup5.scanning_level,
            # "screen5":setup5.screen_range,
            # "scan_t5":setup5.scan_type,
        }    

                # with open(results_filename, mode="w", encoding="utf-8") as results:
                #     results.write(results_template.render(parameters_5))

        for i in parameters["calibrations"]:
            setup = retrieve_setup_by_sn(i["sn"])
            i["brand"] = setup.brand
            i["model"] = setup.model
            i["freq"] = setup.freq
            i["size"] = setup.size
            i["deg"] = setup.angle
            # i["sens"] = model_report["sens_meth"]
            # i["ref"] = model_report["ref_size"]
            # i["ref_l"] = model_report["ref_level"]
            # i["cor"] = model_report["trans_cor"]
            # i["scan"] = model_report["scan_lev"]
            # i["screen"] = model_report["screen_range"]
            # i["scan_t]"] = model_report["sens_meth"]

        parameters_copy = parameters.copy()

        del parameters_copy["request"]
        new_report = Reports(Inspection_Type=model_report["test"], Report_Info=json.dumps(parameters_copy))
        session.add(new_report)
        session.commit()

        return templates.TemplateResponse("PRUT.html", {"request":request, "parameters":parameters})

        # try:
        #     if model_report["sn1"] and model_report["sn2"] and model_report["sn3"] and model_report["sn4"] and model_report["sn5"]:

        #         parameters_5 = {
        #             "request": request, 
        #             "test":model_report["test"], 
        #             "report_num":report_num(model_report["test"]), 
        #             "date":date(), 
        #             "client_name":model_report["client_name"], 
        #             "plant":model_report["plant"],
        #             "contact_name":model_report["contact_name"],
        #             "part_desc":model_report["part_desc"],
        #             "material":model_report["material"],
        #             "heat":model_report["heat"],
        #             "j_order":model_report["j_order"],
        #             "j_qty":model_report["j_qty"],
        #             "od":model_report["od"],
        #             "id":model_report["id"],
        #             "width":model_report["width"],
        #             "height":model_report["height"],
        #             "NDE":model_report["NDE"],
        #             "crit_accept":model_report["crit_accept"],
        #             "rough":model_report["rough"],
        #             "uti_brand":instrument.brand,
        #             "uti_model":instrument.model,
        #             "uti_sn":model_report["uti_sn"],
        #             "cal_date":instrument.calibration_date,
        #             "cal_due":instrument.calibration_due_date,
        #             "sn1":model_report["sn1"],
        #             "brand1":setup1.brand,
        #             "model1":setup1.model,
        #             "freq1":setup1.frequency,
        #             "size1":setup1.size,
        #             "deg1":setup1.angle,
        #             "sens1":setup1.sensitivity,
        #             "ref1":setup1.reference_size,
        #             "ref_l1":setup1.reference_level,
        #             "cor1":setup1.transfer_correction,
        #             "scan1":setup1.scanning_level,
        #             "screen1":setup1.screen_range,
        #             "scan_t1":setup1.scan_type,
        #             "d_cal":model_report["d_cal"],
        #             "sens_block":model_report["sens_block"],
        #             "notch":model_report["notch"],
        #             "rec_lvl":model_report["rec_lvl"],
        #             "ax_scanning":model_report["ax_scanning"],
        #             "circ_ax_scanning":model_report["circ_ax_scanning"],
        #             "method":model_report["method"],
        #             "coupling":model_report["coupling"],
        #             "stage":model_report["stage"],
        #             "remarks":model_report["remarks"],
        #             "insp_name":model_report["insp_name"],
        #             "cert_lvl":cert_lvl,
        #             "ndt_act":model_report["ndt_act"],
        #             "cert_due":cert_due,
        #             "acc_sn":model_report["acc_sn"],
        #             "rej_sn":model_report["rej_sn"],
        #             "sn2":model_report["sn2"],
        #             "brand2":setup2.brand,
        #             "model2":setup2.model,
        #             "freq2":setup2.frequency,
        #             "size2":setup2.size,
        #             "deg2":setup2.angle,
        #             "sens2":setup2.sensitivity,
        #             "ref2":setup2.reference_size,
        #             "ref_l2":setup2.reference_level,
        #             "cor2":setup2.transfer_correction,
        #             "scan2":setup2.scanning_level,
        #             "screen2":setup2.screen_range,
        #             "scan_t2":setup2.scan_type,
        #             "sn3":model_report["sn3"],
        #             "brand3":setup3.brand,
        #             "model3":setup3.model,
        #             "freq3":setup3.frequency,
        #             "size3":setup3.size,
        #             "deg3":setup3.angle,
        #             "sens3":setup3.sensitivity,
        #             "ref3":setup3.reference_size,
        #             "ref_l3":setup3.reference_level,
        #             "cor3":setup3.transfer_correction,
        #             "scan3":setup3.scanning_level,
        #             "screen3":setup3.screen_range,
        #             "scan_t3":setup3.scan_type,
        #             "sn4":model_report["sn4"],
        #             "brand4":setup4.brand,
        #             "model4":setup4.model,
        #             "freq4":setup4.frequency,
        #             "size4":setup4.size,
        #             "deg4":setup4.angle,
        #             "sens4":setup4.sensitivity,
        #             "ref4":setup4.reference_size,
        #             "ref_l4":setup4.reference_level,
        #             "cor4":setup4.transfer_correction,
        #             "scan4":setup4.scanning_level,
        #             "screen4":setup4.screen_range,
        #             "scan_t4":setup4.scan_type,
        #             "sn5":model_report["sn5"],
        #             "brand5":setup5.brand,
        #             "model5":setup5.model,
        #             "freq5":setup5.frequency,
        #             "size5":setup5.size,
        #             "deg5":setup5.angle,
        #             "sens5":setup5.sensitivity,
        #             "ref5":setup5.reference_size,
        #             "ref_l5":setup5.reference_level,
        #             "cor5":setup5.transfer_correction,
        #             "scan5":setup5.scanning_level,
        #             "screen5":setup5.screen_range,
        #             "scan_t5":setup5.scan_type,
        #         }

        #         # with open(results_filename, mode="w", encoding="utf-8") as results:
        #         #     results.write(results_template.render(parameters_5))

        #         return templates.TemplateResponse("PRUT.html", parameters_5)

        #     elif model_report["sn1"] and model_report["sn2"] and model_report["sn3"] and model_report["sn4"]:

        #         parameters_4 = {
        #             "request": request, 
        #             "test":model_report["test"], 
        #             "report_num":report_num(model_report["test"]), 
        #             "date":date(), 
        #             "client_name":model_report["client_name"], 
        #             "plant":model_report["plant"],
        #             "contact_name":model_report["contact_name"],
        #             "part_desc":model_report["part_desc"],
        #             "material":model_report["material"],
        #             "heat":model_report["heat"],
        #             "j_order":model_report["j_order"],
        #             "j_qty":model_report["j_qty"],
        #             "od":model_report["od"],
        #             "id":model_report["id"],
        #             "width":model_report["width"],
        #             "height":model_report["height"],
        #             "NDE":model_report["NDE"],
        #             "crit_accept":model_report["crit_accept"],
        #             "rough":model_report["rough"],
        #             "uti_brand":instrument.brand,
        #             "uti_model":instrument.model,
        #             "uti_sn":model_report["uti_sn"],
        #             "cal_date":instrument.calibration_date,
        #             "cal_due":instrument.calibration_due_date,
        #             "sn1":model_report["sn1"],
        #             "brand1":setup1.brand,
        #             "model1":setup1.model,
        #             "freq1":setup1.frequency,
        #             "size1":setup1.size,
        #             "deg1":setup1.angle,
        #             "sens1":setup1.sensitivity,
        #             "ref1":setup1.reference_size,
        #             "ref_l1":setup1.reference_level,
        #             "cor1":setup1.transfer_correction,
        #             "scan1":setup1.scanning_level,
        #             "screen1":setup1.screen_range,
        #             "scan_t1":setup1.scan_type,
        #             "d_cal":model_report["d_cal"],
        #             "sens_block":model_report["sens_block"],
        #             "notch":model_report["notch"],
        #             "rec_lvl":model_report["rec_lvl"],
        #             "ax_scanning":model_report["ax_scanning"],
        #             "circ_ax_scanning":model_report["circ_ax_scanning"],
        #             "method":model_report["method"],
        #             "coupling":model_report["coupling"],
        #             "stage":model_report["stage"],
        #             "remarks":model_report["remarks"],
        #             "insp_name":model_report["insp_name"],
        #             "cert_lvl":cert_lvl,
        #             "ndt_act":model_report["ndt_act"],
        #             "cert_due":cert_due,
        #             "acc_sn":model_report["acc_sn"],
        #             "rej_sn":model_report["rej_sn"],
        #             "sn2":model_report["sn2"],
        #             "brand2":setup2.brand,
        #             "model2":setup2.model,
        #             "freq2":setup2.frequency,
        #             "size2":setup2.size,
        #             "deg2":setup2.angle,
        #             "sens2":setup2.sensitivity,
        #             "ref2":setup2.reference_size,
        #             "ref_l2":setup2.reference_level,
        #             "cor2":setup2.transfer_correction,
        #             "scan2":setup2.scanning_level,
        #             "screen2":setup2.screen_range,
        #             "scan_t2":setup2.scan_type,
        #             "sn3":model_report["sn3"],
        #             "brand3":setup3.brand,
        #             "model3":setup3.model,
        #             "freq3":setup3.frequency,
        #             "size3":setup3.size,
        #             "deg3":setup3.angle,
        #             "sens3":setup3.sensitivity,
        #             "ref3":setup3.reference_size,
        #             "ref_l3":setup3.reference_level,
        #             "cor3":setup3.transfer_correction,
        #             "scan3":setup3.scanning_level,
        #             "screen3":setup3.screen_range,
        #             "scan_t3":setup3.scan_type,
        #             "sn4":model_report["sn4"],
        #             "brand4":setup4.brand,
        #             "model4":setup4.model,
        #             "freq4":setup4.frequency,
        #             "size4":setup4.size,
        #             "deg4":setup4.angle,
        #             "sens4":setup4.sensitivity,
        #             "ref4":setup4.reference_size,
        #             "ref_l4":setup4.reference_level,
        #             "cor4":setup4.transfer_correction,
        #             "scan4":setup4.scanning_level,
        #             "screen4":setup4.screen_range,
        #             "scan_t4":setup4.scan_type,
        #         }


        #         # with open(results_filename, mode="w", encoding="utf-8") as results:
        #         #     results.write(results_template.render(parameters_4))

        #         return templates.TemplateResponse("PRUT.html", parameters_4)

        #     elif model_report["sn1"] and model_report["sn2"] and model_report["sn3"]:

        #         parameters_3 = {
        #             "request": request, 
        #             "test":model_report["test"], 
        #             "report_num":report_num(model_report["test"]), 
        #             "date":date(), 
        #             "client_name":model_report["client_name"], 
        #             "plant":model_report["plant"],
        #             "contact_name":model_report["contact_name"],
        #             "part_desc":model_report["part_desc"],
        #             "material":model_report["material"],
        #             "heat":model_report["heat"],
        #             "j_order":model_report["j_order"],
        #             "j_qty":model_report["j_qty"],
        #             "od":model_report["od"],
        #             "id":model_report["id"],
        #             "width":model_report["width"],
        #             "height":model_report["height"],
        #             "NDE":model_report["NDE"],
        #             "crit_accept":model_report["crit_accept"],
        #             "rough":model_report["rough"],
        #             "uti_brand":instrument.brand,
        #             "uti_model":instrument.model,
        #             "uti_sn":model_report["uti_sn"],
        #             "cal_date":instrument.calibration_date,
        #             "cal_due":instrument.calibration_due_date,
        #             "sn1":model_report["sn1"],
        #             "brand1":setup1.brand,
        #             "model1":setup1.model,
        #             "freq1":setup1.frequency,
        #             "size1":setup1.size,
        #             "deg1":setup1.angle,
        #             "sens1":setup1.sensitivity,
        #             "ref1":setup1.reference_size,
        #             "ref_l1":setup1.reference_level,
        #             "cor1":setup1.transfer_correction,
        #             "scan1":setup1.scanning_level,
        #             "screen1":setup1.screen_range,
        #             "scan_t1":setup1.scan_type,
        #             "d_cal":model_report["d_cal"],
        #             "sens_block":model_report["sens_block"],
        #             "notch":model_report["notch"],
        #             "rec_lvl":model_report["rec_lvl"],
        #             "ax_scanning":model_report["ax_scanning"],
        #             "circ_ax_scanning":model_report["circ_ax_scanning"],
        #             "method":model_report["method"],
        #             "coupling":model_report["coupling"],
        #             "stage":model_report["stage"],
        #             "remarks":model_report["remarks"],
        #             "insp_name":model_report["insp_name"],
        #             "cert_lvl":cert_lvl,
        #             "ndt_act":model_report["ndt_act"],
        #             "cert_due":cert_due,
        #             "acc_sn":model_report["acc_sn"],
        #             "rej_sn":model_report["rej_sn"],
        #             "sn2":model_report["sn2"],
        #             "brand2":setup2.brand,
        #             "model2":setup2.model,
        #             "freq2":setup2.frequency,
        #             "size2":setup2.size,
        #             "deg2":setup2.angle,
        #             "sens2":setup2.sensitivity,
        #             "ref2":setup2.reference_size,
        #             "ref_l2":setup2.reference_level,
        #             "cor2":setup2.transfer_correction,
        #             "scan2":setup2.scanning_level,
        #             "screen2":setup2.screen_range,
        #             "scan_t2":setup2.scan_type,
        #             "sn3":model_report["sn3"],
        #             "brand3":setup3.brand,
        #             "model3":setup3.model,
        #             "freq3":setup3.frequency,
        #             "size3":setup3.size,
        #             "deg3":setup3.angle,
        #             "sens3":setup3.sensitivity,
        #             "ref3":setup3.reference_size,
        #             "ref_l3":setup3.reference_level,
        #             "cor3":setup3.transfer_correction,
        #             "scan3":setup3.scanning_level,
        #             "screen3":setup3.screen_range,
        #             "scan_t3":setup3.scan_type,
        #         }


        #         # with open(results_filename, mode="w", encoding="utf-8") as results:
        #         #     results.write(results_template.render(parameters_3))

        #         return templates.TemplateResponse("PRUT.html", parameters_3)
        #     elif model_report["sn1"] and model_report["sn2"]:

        #         parameters_2 = {
        #             "request": request, 
        #             "test":model_report["test"], 
        #             "report_num":report_num(model_report["test"]), 
        #             "date":date(), 
        #             "client_name":model_report["client_name"], 
        #             "plant":model_report["plant"],
        #             "contact_name":model_report["contact_name"],
        #             "part_desc":model_report["part_desc"],
        #             "material":model_report["material"],
        #             "heat":model_report["heat"],
        #             "j_order":model_report["j_order"],
        #             "j_qty":model_report["j_qty"],
        #             "od":model_report["od"],
        #             "id":model_report["id"],
        #             "width":model_report["width"],
        #             "height":model_report["height"],
        #             "NDE":model_report["NDE"],
        #             "crit_accept":model_report["crit_accept"],
        #             "rough":model_report["rough"],
        #             "uti_brand":instrument.brand,
        #             "uti_model":instrument.model,
        #             "uti_sn":model_report["uti_sn"],
        #             "cal_date":instrument.calibration_date,
        #             "cal_due":instrument.calibration_due_date,
        #             "sn1":model_report["sn1"],
        #             "brand1":setup1.brand,
        #             "model1":setup1.model,
        #             "freq1":setup1.frequency,
        #             "size1":setup1.size,
        #             "deg1":setup1.angle,
        #             "sens1":setup1.sensitivity,
        #             "ref1":setup1.reference_size,
        #             "ref_l1":setup1.reference_level,
        #             "cor1":setup1.transfer_correction,
        #             "scan1":setup1.scanning_level,
        #             "screen1":setup1.screen_range,
        #             "scan_t1":setup1.scan_type,
        #             "d_cal":model_report["d_cal"],
        #             "sens_block":model_report["sens_block"],
        #             "notch":model_report["notch"],
        #             "rec_lvl":model_report["rec_lvl"],
        #             "ax_scanning":model_report["ax_scanning"],
        #             "circ_ax_scanning":model_report["circ_ax_scanning"],
        #             "method":model_report["method"],
        #             "coupling":model_report["coupling"],
        #             "stage":model_report["stage"],
        #             "remarks":model_report["remarks"],
        #             "insp_name":model_report["insp_name"],
        #             "cert_lvl":cert_lvl,
        #             "ndt_act":model_report["ndt_act"],
        #             "cert_due":cert_due,
        #             "acc_sn":model_report["acc_sn"],
        #             "rej_sn":model_report["rej_sn"],
        #             "sn2":model_report["sn2"],
        #             "brand2":setup2.brand,
        #             "model2":setup2.model,
        #             "freq2":setup2.frequency,
        #             "size2":setup2.size,
        #             "deg2":setup2.angle,
        #             "sens2":setup2.sensitivity,
        #             "ref2":setup2.reference_size,
        #             "ref_l2":setup2.reference_level,
        #             "cor2":setup2.transfer_correction,
        #             "scan2":setup2.scanning_level,
        #             "screen2":setup2.screen_range,
        #             "scan_t2":setup2.scan_type,
        #         }


        #         # with open(results_filename, mode="w", encoding="utf-8") as results:
        #         #     results.write(results_template.render(parameters_2))

        #         return templates.TemplateResponse("PRUT.html", parameters_2)
        #     elif model_report["sn1"]:
        #         parameters_1 = {
        #             "request": request, 
        #             "test":model_report["test"], 
        #             "report_num":report_num(model_report["test"]), 
        #             "date":date(), 
        #             "client_name":model_report["client_name"], 
        #             "plant":model_report["plant"],
        #             "contact_name":model_report["contact_name"],
        #             "part_desc":model_report["part_desc"],
        #             "material":model_report["material"],
        #             "heat":model_report["heat"],
        #             "j_order":model_report["j_order"],
        #             "j_qty":model_report["j_qty"],
        #             "od":model_report["od"],
        #             "id":model_report["id"],  
        #             "width":model_report["width"],
        #             "height":model_report["height"],
        #             "NDE":model_report["NDE"],
        #             "crit_accept":model_report["crit_accept"],
        #             "rough":model_report["rough"],
        #             "uti_brand":instrument.brand,
        #             "uti_model":instrument.model,
        #             "uti_sn":model_report["uti_sn"],
        #             "cal_date":instrument.calibration_date,
        #             "cal_due":instrument.calibration_due_date,
        #             "sn1":model_report["sn1"],
        #             "brand1":setup1.brand,
        #             "model1":setup1.model,
        #             "freq1":setup1.freq,
        #             "size1":setup1.size,
        #             "deg1":setup1.angle,
        #             "sens1":model_report["sens_meth1"],#setup1.sensitivity,
        #             "ref1":model_report["ref_size1"],#setup1.reference_size,
        #             "ref_l1":model_report["ref_level1"],#setup1.reference_level,
        #             "cor1":model_report["trans_cor1"],#setup1.transfer_correction,
        #             "scan1":model_report["scan_lev1"],#setup1.scanning_level,
        #             "screen1":model_report["screen_range1"],#setup1.screen_range,
        #             "scan_t1":model_report["scan_type1"],#setup1.scan_type,
        #             "d_cal":model_report["d_cal"],
        #             "sens_block":model_report["sens_block"],
        #             "notch":model_report["notch"],
        #             "rec_lvl":model_report["rec_lvl"],
        #             "ax_scanning":model_report["ax_scanning"],
        #             "circ_ax_scanning":model_report["circ_ax_scanning"],
        #             "method":model_report["method"],
        #             "coupling":model_report["coupling"],
        #             "stage":model_report["stage"],
        #             "remarks":model_report["remarks"],
        #             "insp_name":model_report["insp_name"],
        #             "cert_lvl":cert_lvl,
        #             "ndt_act":model_report["ndt_act"],
        #             "cert_due":cert_due,
        #             "acc_sn":model_report["acc_sn"],
        #             "rej_sn":model_report["rej_sn"]
        #         }

        #         return templates.TemplateResponse("PRUT.html", parameters_1)

        #         # output_text = template.render(parameters_1)

        #         # output_pdf = results_filename + '.pdf'
        #         # pdfkit.from_string(output_text, output_pdf, configuration=config, css='styles/style.css')  

        #         # with open(results_filename + ".html", mode="w", encoding="utf-8") as results:
        #         #     results.write(results_template.render(parameters_1))
        #         #     pdf = pdfkit.from_file(results_filename + ".html", configuration=config)
        #         #     headers = {'Content-Disposition': f'attachment; filename="{results_filename}.pdf"'}
        #         #     return Response(pdf, headers=headers, media_type='application/pdf')

        #         # html_response = templates.TemplateResponse("PRUT.html", parameters_1)

        #         # #print(html_response.body.decode("utf-8"))

        #         # no_new_line = html_response.body.decode("utf-8")
                
        #         # print(no_new_line)

        #         # with open(r"static\buffer\buffer.html", "w") as file:
        #         #     file.write(no_new_line)

        #         # #pdfurldownload = str(downloads_path) + "\\" + str(box_group.value) + "-R-" + str(year) + ".pdf"
                    
        #         # #browser = await p.chromium.launch()
        #         # #p = sync_playwright().start()

        #         # # async with async_playwright() as p:
        #         # #     browser = await p.chromium.launch()

        #         # #     page = await browser.new_page()

        #         # #     #page = await browser.new_page()
        #         # #     #await page.goto(url)}

        #         # #     #await page.set_content(no_new_line)
        #         # #     # pdf = await page.pdf()#path=pdfurldownload)
        #         # #     #await browser.close()

        #         # #     await page.set_content(no_new_line)

        #         # #     await page.pdf(r"static\buffer\buffer.pdf")

        #         # #     await browser.close()

        #         # pdfkit.from_file(r"static\buffer\buffer.html", r"static\buffer\buffer.pdf")
    
        #         # headers = {'Content-Disposition': 'inline; filename="out.pdf"'}
    
        #         # return FileResponse(path=r"static\buffer\buffer.pdf",headers=headers, media_type='aplication/pdf')
    
        #         #return templates.TemplateResponse("PRUT.html", parameters_1)

        # except NameError:
        #     return {"error": "NameError"}
        
    elif model_report["test"] != "UT":
        return {"test":model_report["test"]}