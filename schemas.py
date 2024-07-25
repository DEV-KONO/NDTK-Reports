from datetime import date
from httpx import stream
from pydantic import BaseModel
from typing import Optional

class Schema_ClientBase(BaseModel):
    name: str

class Schema_Plants(Schema_ClientBase):
    client_name: str

class Schema_Contacts(Schema_ClientBase):
    client_name: str

class Schema_Acceptance(BaseModel):
    acceptance: str
    nde_spec: str

class Schema_NDE(BaseModel):
    nde_spec: str
    client_name: str
    acceptance: Schema_Acceptance | None = None

class Schema_Acabado(BaseModel):
    acabado: str
    client_name: str


class Schema_Client(Schema_ClientBase):

    plantas: Schema_Plants | None = None
    contactos: Schema_Contacts | None = None
    nde: Schema_NDE | None = None

    class config:
        orm_mode = True

class Schema_UTI(BaseModel):
    sn: int
    brand: str
    model: str
    calibration_date: date
    calibration_due_date: date

# class Schema_Acceptance(BaseModel):
#     id: int
#     acceptance_criteria: str

class Schema_Just_UTI_SN(BaseModel):
    sn: int

class Schema_Report(BaseModel):

    test: str 
    client_name: str 
    plant: str 
    contact_name: str 
    part_desc: str 
    material: str 
    heat: str 
    j_order: str 
    j_qty: str 
    od: float 
    id: float 
    width: float 
    height: float 
    NDE: str 
    crit_accept: str 
    rough: str
    uti_sn: int
    sn1: int
    d_cal: str
    sens_block: str
    notch: str
    rec_lvl: str
    ax_scanning: str
    circ_ax_scanning: str
    method: str
    coupling: str
    stage: str
    remarks: str
    insp_name: str
    ndt_act: str
    cert_lvl: str | None = None
    cert_due: str| None = None
    acc_sn: int | None = None
    rej_sn: int | None = None
    sn2: int | None = None
    sn3: int | None = None
    sn4: int | None = None
    sn5: int | None = None
    