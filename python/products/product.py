import datetime
from decimal import Decimal
from enum import Enum


class CompanyName(Enum):
    """Define the manufacturer company."""
    PROTEI_RD = "НТЦ ПРОТЕЙ"
    PROTEI_ST = "ПРОТЕЙ СТ"
    BOTH = "НТЦ ПРОТЕЙ + ПРОТЕЙ СТ"
    UNKNOWN = None


class DevOpsDepartment(Enum):
    IN = "Интеллектуальные сети"
    NGN_MO = "Коммутационное оборудование"
    MOBILE = "Мобильные сети"
    CPE = "Платформа CPE"
    CALL_CENTER = "Колл-центр"
    SOSM = "СОРМ"
    SYSTEM_112 = "Система-112"
    SYSTEM_02 = "Система-02"
    WEB_RTC = "Видеоконференцсвязь"
    SAFE_CITY = "Безопасный город"
    VIDEO_PORTAL = "Видеопортал"
    SERVICE_CENTER = "Сервисный центр"
    ALERT_SYSTEM = "Система оповещения"


class DimensionLinearUnit(Enum):
    M = "METERS"
    CM = "CENTIMETERS"
    MM = "MILLIMETERS"
    UNKNOWN = None


class DimensionWeightUnit(Enum):
    KG = "KILOGRAMS"
    G = "GRAMS"
    MG = "MILLIGRAMS"
    UNKNOWN = None


class Language(Enum):
    RUS = "RUSSIAN"
    ENG = "ENGLISH"
    UNKNOWN = None


class DocCategory(Enum):
    BASIC_DESIGN = "BASIC DESIGN"
    OPERATION_DOC = "OPERATION DOCUMENTATION"
    DESIGN_DOC = "DESIGN DOCUMENTATION"
    DEVELOPMENT_DOC = "DEVELOPMENT DOCUMENTATION"
    PRODUCTION_DOC = "PRODUCTION DOCUMENTATION"
    UNKNOWN = None


class HardwareInterface:
    def __init__(
            self,
            interface_name: str = None,
            amount: int = None):
        self.interface_name = interface_name
        self.amount = amount

    def __str__(self):
        return f"Interface: {self.interface_name}, amount: {self.amount}"

    def __repr__(self):
        return f"HardwareInterface({self.interface_name}, {self.amount})"


class Certificate:
    def __init__(
            self,
            has_cert: bool = False,
            cert_no: str = None,
            expiry_date: datetime.date = None):
        self.has_cert = has_cert
        self.cert_no = cert_no
        self.expiry_date = expiry_date


class Dimension:
    def __init__(
            self,
            length: Decimal = None,
            width: Decimal = None,
            height: Decimal = None,
            linear_unit: DimensionLinearUnit = DimensionLinearUnit.UNKNOWN,
            mass: Decimal = None,
            weight_unit: DimensionWeightUnit = DimensionWeightUnit.UNKNOWN):
        pass




class Requirement:
    def __init__(
            self,
            requirement: str = None,
            is_nullable: bool = False):
        self.requirement = requirement
        self.is_nullable = is_nullable


class ProductDoc:
    def __init__(
            self,
            doc_category: DocCategory = DocCategory.UNKNOWN,
            doc_type: str = None,
            short_doc_type: str = None,
            language: Language = Language.UNKNOWN,
            year: datetime.date = None):
        self.doc_category = doc_category
        self.doc_type = doc_type
        self.short_doc_type = short_doc_type
        self.language = language
        self.year = year


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
            tags: list[str] = None):
        if tags is None:
            tags = []
        if certificate is None:
            certificate = Certificate()

        self.full_name = full_name
        self.short_name = short_name
        self.devops_department = devops_department
        self.modification_no = modification_no
        self.company_name = company_name
        self.certificate = certificate
        self.spec_no = spec_no
        self.summary = summary
        self.has_hardware = has_hardware
        self.has_software = has_software
        self.branch = branch
        self.tags = tags

    def __hash__(self):
        return hash((self.full_name, self.short_name, self.modification_no, self.spec_no))

    def __key(self):
        return self.full_name, self.short_name, self.modification_no, self.spec_no

    def __eq__(self, other):
        if isinstance(other, General):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, General):
            return self.__key() != other.__key()
        else:
            return NotImplemented

    def __bool__(self):
        attrs = ("modification_no", "company_name", "certificate", "spec_no", "summary", "has_hardware", "has_software",
                 "branch", "tags")
        bool_company = self.company_name == CompanyName.BOTH
        bool_attrs = all([getattr(self, attr) is None for attr in attrs])
        bool_tags = len(self.tags)

        return bool_company and bool_attrs and bool_tags


class Hardware:
    def __init__(
            self,
            dimensions: Dimension = None,
            hw_components: list[str] = None,
            hw_interfaces: list[HardwareInterface] = None,
            hw_operation: list[str] = None,
            hw_requirements: list[Requirement] = None,
            hw_opmodes: list[str] = None):
        if dimensions is None:
            dimensions = Dimension()
        if hw_components is None:
            hw_components = []
        if hw_interfaces is None:
            hw_interfaces = []
        if hw_operation is None:
            hw_operation = []
        if hw_requirements is None:
            hw_requirements = []
        if hw_opmodes is None:
            hw_opmodes = []

        self.dimensions = dimensions
        self.hw_components = hw_components
        self.hw_interfaces = hw_interfaces
        self.hw_operation = hw_operation
        self.hw_requirements = hw_requirements
        self.hw_opmodes = hw_opmodes

    def __bool__(self):
        attrs = ("hw_components", "hw_interfaces", "hw_operation", "hw_requirements", "hw_opmodes")
        bool_dimensions = self.dimensions == Dimension()
        bool_attrs = all([len(getattr(self, attr)) for attr in attrs])
        return bool_dimensions and bool_attrs


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
        if protocols is None:
            protocols = []
        if features is None:
            features = []
        if sw_components is None:
            sw_components = []
        if sw_operation is None:
            sw_operation = []
        if sw_requirements is None:
            sw_requirements = []
        if sw_opmodes is None:
            sw_opmodes = []

        self.protocols = protocols
        self.features = features
        self.sw_components = sw_components
        self.sw_operation = sw_operation
        self.sw_requirements = sw_requirements
        self.sw_opmodes = sw_opmodes
        self.has_gui = has_gui
        self.has_api = has_api
        self.has_cli = has_cli

    def __bool__(self):
        attrs_len = ("protocols", "features", "sw_components", "sw_operation", "sw_requirements", "sw_opmodes")
        attrs_bool = ("has_gui", "has_api", "has_cli")
        bool_len = all([getattr(self, attr) is None for attr in attrs_len])
        bool_bool = not all([getattr(self, attr) for attr in attrs_bool])

        return bool_len and bool_bool


class Documentation:
    def __init__(
            self,
            docs: list[ProductDoc] = None):
        if docs is None:
            docs = []
        self.docs = docs

    def __bool__(self):
        return len(self.docs)

    def __len__(self):
        return len(self.docs)


class Product:
    index = 0

    __slots__ = "general", "hardware", "software", "documentation", "identifier"

    def __init__(
            self,
            general: General,
            hardware: Hardware = Hardware(),
            software: Software = Software(),
            documentation: Documentation = Documentation()):
        self.general = general
        self.hardware = hardware
        self.software = software
        self.documentation = documentation
        self.identifier = Product.index

        Product.index += 1

    def __str__(self):
        return f"General: {self.general};\nHardware: {self.hardware};\nSoftware: {self.software};\n" \
               f"Doc: {self.documentation}"

    def __bool__(self):
        attrs = "general", "hardware", "software", "documentation"
        return any([bool(getattr(self, attr) for attr in attrs)])


def main():
    pass


if __name__ == "__main__":
    main()
