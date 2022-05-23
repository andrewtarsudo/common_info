import datetime
from decimal import Decimal
from enum import Enum


class CompanyName(Enum):
    PROTEI_RD = "НТЦ ПРОТЕЙ"
    PROTEI_ST = "ПРОТЕЙ СТ"
    BOTH = "НТЦ ПРОТЕЙ + ПРОТЕЙ СТ"


class DevOpsDepartment(Enum):
    NGN = "NGN"
    MOBILE = "MOBILE"
    CPE = "CPE"
    CALL_CENTER = "CALL CENTER"
    SOSM = "SOSM"
    MOUNT = "MOUNT"


class DimensionLinearUnit(Enum):
    M = "METERS"
    CM = "CENTIMETERS"
    MM = "MILLIMETERS"


class DimensionWeightUnit(Enum):
    KG = "KILOGRAMS"
    G = "GRAMS"
    MG = "MILLIGRAMS"


class Language(Enum):
    RUS = "RUSSIAN"
    ENG = "ENGLISH"


class DocCategory(Enum):
    BASIC_DESIGN = "BASIC DESIGN"
    OPERATION_DOC = "OPERATION DOCUMENTATION"
    DESIGN_DOC = "DESIGN DOCUMENTATION"
    DEVELOPMENT_DOC = "DEVELOPMENT DOCUMENTATION"
    PRODUCTION_DOC = "PRODUCTION DOCUMENTATION"


class HardwareInterface:
    def __init__(
            self,
            interface_name: str = None,
            amount: int = None):
        pass


class Certificate:
    def __init__(
            self,
            has_cert: bool = False,
            cert_no: str = None,
            expiry_date: datetime.date = None):
        pass


class Dimension:
    def __init__(
            self,
            length: Decimal = None,
            width: Decimal = None,
            height: Decimal = None,
            linear_unit: DimensionLinearUnit = None,
            mass: Decimal = None,
            weight_unit: DimensionWeightUnit = None):
        pass


class Requirement:
    def __init__(
            self,
            requirement: str = None,
            is_nullable: bool = False):
        pass


class ProductDoc:
    def __init__(
            self,
            doc_category: DocCategory = None,
            doc_type: str = None,
            short_doc_type: str = None,
            language: Language = None,
            year: datetime.date = None):
        pass





class General:
    def __init__(
            self,
            full_name: str,
            short_name: str,
            devops_department: DevOpsDepartment,
            modification_no: str = None,
            company_name: CompanyName = CompanyName.BOTH,
            certificate: Certificate = None,
            spec_no: str = None,
            summary: str = None,
            has_hardware: bool = False,
            has_software: bool = False,
            branch: str = None,
            tags: list = None):
        pass


class Hardware:
    def __init__(
            self,
            dimensions: Dimension = None,
            hw_components: list[str] = None,
            hw_interfaces: list[HardwareInterface] = None,
            hw_operation: list[str] = None,
            hw_requirements: list[Requirement] = None,
            hw_opmodes: list[str] = None):
        pass


class Software:
    def __init__(
            self,
            protocols: list[str] = None,
            features: list[str] = None,
            sw_components: list[str] = None,
            sw_operation: list[str] = None,
            sw_requirements: list[Requirement] = None,
            sw_opmodes: list[str] = None,
            has_gui: bool = False,
            has_api: bool = False,
            has_cli: bool = False):
        pass


class Documentation:
    def __init__(
            self,
            doc: list[ProductDoc] = None):
        pass


class Product:
    index = 0
    
    def __init__(self, general: General, hardware: Hardware, software: Software, documentation: Documentation):
        self.general = general
        self.hardware = hardware
        self.software = software
        self.documentation = documentation
        self.identifier = Product.index
        
        Product.index += 1


def main():
    pass 
    

if __name__ == "__main__":
    main()
