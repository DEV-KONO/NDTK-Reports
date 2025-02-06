from datetime import date
from pydantic import BaseModel

class Schema_ClientBase(BaseModel):
    name: str

class Schema_Probe(BaseModel):
    sn: int
    brand: str
    model: str
    freq: str
    size: str
    angle: str

class Schema_Plants(Schema_ClientBase):
    client_name: str

class Schema_Contacts(Schema_ClientBase):
    client_name: str

class Schema_Acceptance(BaseModel):
    acceptance_criteria: str
    nde_id: int

class Schema_NDE(BaseModel):
    nde_spec: str

class Schema_Acabado(BaseModel):
    acabado: str


class Schema_Client(Schema_ClientBase):

    plantas: Schema_Plants | None = None
    contactos: Schema_Contacts | None = None

    class config:
        orm_mode = True

class Schema_User(BaseModel):
    email: str
    password: str

class Schema_Register(BaseModel):
    email: str
    user: str 
    password: str
    confpassword: str

class Schema_Email(BaseModel):
    email: str

class Schema_Inspector(BaseModel):
    name: str
    vt: str | None=None
    vt_due: str | None=None
    pt: str | None=None
    pt_due: str | None=None
    ut: str | None=None
    ut_due: str | None=None
    et: str | None=None
    et_due: str | None=None
    mt: str | None=None
    mt_due: str | None=None

class Schema_UTI(BaseModel):
    sn: int
    brand: str
    model: str
    calibration_date: date
    calibration_due_date: date

class Schema_Probe(BaseModel):
    sn :int
    brand :str
    model :str
    freq :str
    size :str
    angle :str

# class Schema_Acceptance(BaseModel):
#     id: int
#     acceptance_criteria: str

class Schema_Just_UTI_SN(BaseModel):
    sn: int

class Schema_Calibration(BaseModel):
    sn: int
    sens_meth: str
    ref_size: str
    ref_level: str
    trans_cor: str
    scan_lev: str
    screen_range: str
    scan_type: str

class Schema_Report(BaseModel):

    test: str | None=None 
    client_name: str  | None=None
    plant: str | None=None 
    contact_name: str  | None=None
    part_desc: str 
    material: str 
    heat: str | None=None 
    j_order: str  | None=None
    j_qty: str 
    od: str 
    id: str 
    width: str
    height: str
    NDE: str 
    crit_accept: str | None=None 
    rough: str | None=None
    uti_sn: int
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
    ndt_act: str | None=None
    cert_lvl: str | None = None
    cert_due: str| None = None
    acc_sn: int | None = None
    rej_sn: int | None = None
    calibrations: list

# class Schema_Report(BaseModel):

#     test: str | None=None 
#     client_name: str  | None=None
#     plant: str | None=None 
#     contact_name: str  | None=None
#     part_desc: str 
#     material: str 
#     heat: str | None=None 
#     j_order: str  | None=None
#     j_qty: str 
#     od: str 
#     id: str 
#     width: str
#     height: str
#     NDE: str 
#     crit_accept: str | None=None 
#     rough: str | None=None
#     uti_sn: int
#     sn1: int
#     d_cal: str
#     sens_block: str
#     notch: str
#     rec_lvl: str
#     ax_scanning: str
#     circ_ax_scanning: str
#     method: str
#     coupling: str
#     stage: str
#     remarks: str
#     insp_name: str
#     ndt_act: str | None=None
#     cert_lvl: str | None = None
#     cert_due: str| None = None
#     acc_sn: int | None = None
#     rej_sn: int | None = None
#     sn2: int | None = None
#     sn3: int | None = None
#     sn4: int | None = None
#     sn5: int | None = None
#     sens_meth1: str
#     sens_meth2: str | None = None
#     sens_meth3: str | None = None
#     sens_meth4: str | None = None
#     sens_meth5: str | None = None
#     ref_size1: str
#     ref_size2: str | None = None
#     ref_size3: str | None = None
#     ref_size4: str | None = None
#     ref_size5: str | None = None
#     ref_level1: str
#     ref_level2: str | None = None
#     ref_level3: str | None = None
#     ref_level4: str | None = None
#     ref_level5: str | None = None
#     trans_cor1: str
#     trans_cor2: str | None = None
#     trans_cor3: str | None = None
#     trans_cor4: str | None = None
#     trans_cor5: str | None = None
#     scan_lev1: str
#     scan_lev2: str | None = None
#     scan_lev3: str | None = None
#     scan_lev4: str | None = None
#     scan_lev5: str | None = None
#     screen_range1: str
#     screen_range2: str | None = None
#     screen_range3: str | None = None
#     screen_range4: str | None = None
#     screen_range5: str | None = None
#     scan_type1: str
#     scan_type2: str | None = None
#     scan_type3: str | None = None
#     scan_type4: str | None = None
#     scan_type5: str | None = None