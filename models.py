from pyparsing import col
from sqlalchemy import JSON, Boolean, Null, Nullable, column,create_engine, Column, Integer, String, BigInteger, Date, Float, ForeignKey, false, null, true
from sqlalchemy.orm import declarative_base, relationship
from urllib.parse import quote
from dotenv import load_dotenv
import os

load_dotenv()

DB_PASS = os.getenv("DB_PASS")

postgres_url = "postgresql://root:yfWhkVsscKSCV50EtUztP6CPSVGSwPsF@dpg-cu97vid2ng1s73f13nf0-a/ndtk_reports:yfWhkVsscKSCV50EtUztP6CPSVGSwPsF" #% quote(DB_PASS)

engine = create_engine(postgres_url)

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

class Reports(Base):
    __tablename__ = "Reports"

    Report_Num = Column(Integer, primary_key=True)
    Inspection_Type = Column(String, nullable=False)
    Report_Info = Column(JSON, nullable=False)


class Plants(BaseModel):
    __tablename__ = "plantas"

    client_id = Column(ForeignKey("clientes.id"))
    client = relationship("Clients", back_populates="plants")

    def __repr__(self):
        return f"<Plant(id={self.id}, Name={self.name}, CID={self.client_id})>"

class Contacts(BaseModel):
    __tablename__ = "contactos"

    client_id = Column(ForeignKey("clientes.id"))
    client = relationship("Clients", back_populates="contacts")

    def __repr__(self):
        return f"<Contact(id={self.id}, Name={self.name}, CID={self.client_id})>"
    
class Acceptance(Base):
    __tablename__ = "Acceptance Criteria"

    id = Column(Integer, primary_key=True, nullable=False)
    acceptance_criteria = Column(String, nullable=False)
    nde_id = Column(ForeignKey("NDE Specification.id"))
    nde = relationship("NDE", back_populates="acceptance")
    
class NDE(Base):
    __tablename__ = "NDE Specification"

    id = Column(Integer, primary_key=True, nullable=False)
    nde_spec = Column(String, nullable=False)
    acceptance = relationship(Acceptance)

class Acabado(Base):
    __tablename__ = "Acabado Superficial"

    id = Column(Integer, primary_key=True, nullable=False)
    acabado = Column(String, nullable=False)

class Admins(Base):
    __tablename__ = "admins"

    email = Column(String, primary_key=True, nullable=False, unique=True)
    username = Column(String, nullable=False)
    admin = Column(Boolean, default=False)
    salt = Column(String, nullable=False)

class Distance(Base):
    __tablename__ = "Distance Calibration"

    id = Column(Integer, primary_key=True, nullable=False)
    distance = Column(String, nullable=False)

class Sensitivity(Base):
    __tablename__ = "Sensitivity Block"

    id = Column(Integer, primary_key=True, nullable=False)
    sensitivity = Column(String, nullable=False)

class Notch(Base):
    __tablename__ = "Notch Depth"

    id = Column(Integer, primary_key=True, nullable=False)
    notch_depth = Column(String, nullable=False)

class Recording(Base):
    __tablename__ = "Recording Level"

    id = Column(Integer, primary_key=True, nullable=False)
    recording_level = Column(String, nullable=False)

class Scanning(Base):
    __tablename__ = "Scanning Direction"

    id = Column(Integer, primary_key=True, nullable=False)
    scanning_direction = Column(String, nullable=False)

class Method(Base):
    __tablename__ = "Inspection Method"

    id = Column(Integer, primary_key=True, nullable=False)
    ins_method = Column(String, nullable=False)

class Agent(Base):
    __tablename__ = "Coupling Agent"

    id = Column(Integer, primary_key=True, nullable=False)
    coupling_agent = Column(String, nullable=False)

class Stage(Base):
    __tablename__ = "Inspection Stage"

    id = Column(Integer, primary_key=True, nullable=False)
    ins_stage = Column(String, nullable=False)

class Clients(BaseModel):
    __tablename__ = "clientes"

    plants = relationship(Plants)
    contacts = relationship(Contacts)

    def __repr__(self):
        return f"<Client(id={self.id}, Name={self.name})>"

class Instrument(Base):
    __tablename__ = "ut_instruments"

    sn = Column(BigInteger, primary_key=True, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    calibration_date = Column(Date, nullable=False)
    calibration_due_date = Column(Date, nullable=False)

class Probe(Base):
    __tablename__ = "Probe Data"

    sn = Column(BigInteger, primary_key=True, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    freq = Column(String, nullable=False)
    size = Column(String, nullable=False)
    angle = Column(String, nullable=False)

class Sensitivity_Method(Base):
    __tablename__ = "Sensitivity Method"

    id = Column(Integer, primary_key=True)
    method = Column(String, nullable=False)

class Ref_Size(Base):
    __tablename__ = "Reference Size"

    id = Column(Integer, primary_key=True)
    ref_size = Column(String, nullable=False)

class Ref_Level(Base):
    __tablename__ = "Reference Level"

    id = Column(Integer, primary_key=True)
    ref_level = Column(String, nullable=False)

class Trans_Corr(Base):
    __tablename__ = "Transfer Correction"

    id = Column(Integer, primary_key=True)
    trans_cor = Column(Integer, nullable=False)

class Scan_level(Base):
    __tablename__ = "Scanning Level"

    id = Column(Integer, primary_key=True)
    scan_level = Column(Integer, nullable=False)

class Screen_Range(Base):
    __tablename__ = "Screen Range"

    id = Column(Integer, primary_key=True)
    screen_range = Column(Float, nullable=False)

class Scan_Type(Base):
    __tablename__ = "Scan Type"

    id = Column(Integer, primary_key=True)
    scan_type = Column(String, nullable=False)

# class Calibration(Base):
#     __tablename__ = "calibration_setup"

#     sn = Column(BigInteger, primary_key=True, nullable=False)
#     brand = Column(String, nullable=False)
#     model = Column(String, nullable=False)
#     frequency = Column(String, nullable=False)
#     size = Column(String, nullable=False)
#     angle = Column(String, nullable=False)
#     sensitivity = Column(String, nullable=False)
#     reference_size = Column(String, nullable=False)
#     reference_level = Column(String, nullable=False)
#     transfer_correction = Column(String, nullable=False)
#     scanning_level = Column(String, nullable=False)
#     screen_range = Column(String, nullable=False)
#     scan_type = Column(String, nullable=False)

class Inspector(Base):
    __tablename__ = "inspectores"

    name = Column(String, primary_key=True, nullable=False)
    VT = Column(String) 
    PT = Column(String) 
    UT = Column(String) 
    ET = Column(String) 
    MT = Column(String)
    VT_due = Column(Date)
    PT_due = Column(Date)
    UT_due = Column(Date)
    ET_due = Column(Date)
    MT_due = Column(Date)

# class Client(Base):
#     __tablename__ = "clientes"

#     id = Column(Integer, primary_key=True, nullable=False)
#     #id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
#     name = Column(String, nullable=False)
#     #plantas: Mapped[list["Plant"]] = relationship()
#     #contactos: Mapped[list["Contact"]] = relationship()

#     # plant_id = Column(
#     #     Integer,
#     #     ForeignKey("plantas.id", ondelete="CASCADE"), 
#     #     nullable=False
#     # )

#     # contact_id = Column(
#     #     Integer,
#     #     ForeignKey("contactos.id", ondelete="CASCADE"), 
#     #     nullable=False
#     # )

#     plantas = relationship("Plant")
#     contactos = relationship("Contact")

# class Plant(Base):

#     __tablename__ = "plantas"

#     id = Column(Integer, primary_key=True, nullable=False)
#     #id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
#     plant = Column(String, nullable=False)
#     #client: Mapped[int] = mapped_column(ForeignKey("clientes.id"))

#     client_id = Column(
#         Integer,
#         ForeignKey("clientes.id", ondelete="CASCADE"),
#     )

# class Contact(Base):
#     __tablename__ = "contactos"

#     id = Column(Integer, primary_key=True, nullable=False)
#     #id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
#     contact = Column(String, nullable=False)
#     #client: Mapped[int] = mapped_column(ForeignKey("clientes.id"))

#     client_id = Column(
#         Integer,
#         ForeignKey("clientes.id", ondelete="CASCADE"),
#     )

#class Report(Base):

Base.metadata.create_all(engine)