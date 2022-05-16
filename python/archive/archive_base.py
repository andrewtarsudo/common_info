import datetime
import re
from enum import Enum
from typing import Optional, Union
from pathlib import Path
from hashlib import md5
import logging
import json
from json import JSONDecodeError
import os
import pprint


class Const:
    dict_classification = dict()
    dict_doc_product = dict()
    dict_product = dict()
    dict_physical = dict()
    set_tags = set()


class SortMode(Enum):
    ASC = "по возрастанию"
    DESC = "по убыванию"


class Language(Enum):
    RUS = "русский"
    ENG = "английский"


class DocStandard(Enum):
    """
    Specify the state standards.
    """
    GOST_2_102_2013 = "ГОСТ 2.102-2013"
    GOST_2_106_96 = "ГОСТ 2.106-96"
    GOST_2_109_73 = "ГОСТ 2.109-73"
    GOST_2_114_2016 = "ГОСТ 2.114-2016"
    GOST_2_119_2013 = "ГОСТ 2.119-2013"
    GOST_2_120_2013 = "ГОСТ 2.120-2013"
    GOST_2_601_2019 = "ГОСТ 2.601-2019"
    GOST_2_610_2006 = "ГОСТ 2.610-2006"
    GOST_2_701_2008 = "ГОСТ 2.701-2008"

    GOST_3_1105_2011 = "ГОСТ 3.1105-2011"
    GOST_3_1118_82 = "ГОСТ 3.1118-82"
    GOST_3_1122_84 = "ГОСТ 3.1122-84"
    GOST_3_1404_86 = "ГОСТ 3.1404-86"

    GOST_19_202_78 = "ГОСТ 19.202-78"
    GOST_19_301_79 = "ГОСТ 19.301-79"
    GOST_19_401_78 = "ГОСТ 19.401-78"
    GOST_19_402_78 = "ГОСТ 19.402-78"
    GOST_19_403_79 = "ГОСТ 19.403-79"
    GOST_19_404_79 = "ГОСТ 19.404-79"
    GOST_19_502_78 = "ГОСТ 19.502-78"
    GOST_19_503_79 = "ГОСТ 19.503-79"
    GOST_19_504_79 = "ГОСТ 19.504-79"
    GOST_19_505_79 = "ГОСТ 19.505-79"
    GOST_19_507_79 = "ГОСТ 19.507-79"

    GOST_34_201_89 = "ГОСТ 34.201-89"

    GOST_R_2_106_2019 = "ГОСТ Р 2.106-2019"
    GOST_R_2_610_2019 = "ГОСТ Р 2.610-2019"
    GOST_R_2_711_2019 = "ГОСТ Р 2.711-2019"

    GOST_RV_15_211_2002 = "ГОСТ РВ 15.211-2002"

    STO_202_2019 = "СТО 202-2019"


class DocCategory(Enum):
    """
    Specify the document categories.
    """
    BASIC_DESIGN = "Технический проект"
    DESIGN_DOC = "Конструкторская документация"
    DEVELOPMENT_DOC = "Программная документация"
    OPERATION_DOC = "Эксплуатационная документация"
    PRODUCTION_DOC = "Технологическая документация"
    FOREIGN = "Зарубежье"


class DocShort(Enum):
    """
    Specify the document type abbreviations.
    """
    AUTHENTIC_TEXT_HOLDERS_LIST_SHORT = "05"
    SOURCE_CODE_SHORT = "12"
    PROGRAM_DESCRIPTION_SHORT = "13"
    LIST_OPERATION_PAPERS_20_SHORT = "20"
    PRODUCT_STATUS_RECORD_30_SHORT = "30"
    USE_DESCRIPTION_SHORT = "31"
    SYSTEM_PROGRAMMER_GUIDE_SHORT = "32"
    PROGRAMMER_GUIDE_SHORT = "33"
    OPERATOR_GUIDE_SHORT = "34"
    TESTING_PROGRAMME_AND_PROCEDURE_51_SHORT = "51"
    EXPLANATORY_NOTE_81_SHORT = "81"

    OTHERS_SHORT = "90-99"

    DATABASE_CATALOG_SHORT = "В7"
    MESSAGES_OUTPUT_SHORT = "В8"
    LIST_REFERENCE_PAPERS_SHORT = "ВД"
    OPERATION_DOCUMENTATION_TYPES_SHORT = "ВдЭД"
    LIST_BOUGHT_IN_PERMISSION_PAPERS_SHORT = "ВИ"
    GENERAL_ARRANGEMENT_DRAWING_SHORT = "ВО"
    LIST_BOUGHT_IN_PAPERS_SHORT = "ВП"
    LIST_ASSEMBLY_PAPERS_SHORT = "ВП/ВСИ"
    LIST_SPECIFICATIONS_SHORT = "ВС"
    LIST_OPERATION_PAPERS_PROGRAMMING_SHORT = "ВЭ"

    OUTLINE_DRAWING_SHORT = "ГЧ"

    SECURITY_SYSTEM_ADMINISTRATOR_GUIDE_SHORT = "Д3"
    INFORMATION_SECURITY_OFFICER_GUIDE_SHORT = "Д4"
    SECURITY_TOOL_SYSTEM_GUIDE_D5_SHORT = "Д5"
    SECURITY_TOOL_SYSTEM_GUIDE_D6_SHORT = "Д6"
    SECURITY_TOOL_OPERATOR_GUIDE_SHORT = "Д7"
    CONFIGURATION_TEST_CASE_SHORT = "Д8"
    JOINT_RESOLUTION_SHORT = "Д9"
    ANTIVIRUS_PROTECTION_MANAGEMENT_INSTRUCTION_SHORT = "Д11"

    PRODUCT_COMPONENT_STRUCTURE_SHORT = "Е1"

    SPTA_SET_LIST_SHORT = "ЗИ"

    INSTRUCTIONS_SHORT = "И"
    SPTA_USE_INSTRUCTION_SHORT = "И1"
    USER_GUIDE_SHORT = "И3"
    DATABASE_MANAGEMENT_INSTRUCTION_SHORT = "И4"
    SECURITY_ADMINISTRATOR_GUIDE_SHORT = "И5"
    MOUNTING_COMMISSIONING_INSTRUCTION_SHORT = "ИМ"
    INSPECTION_AND_MAINTENANCE_GUIDE_SHORT = "ИС"
    OPERATION_INSTRUCTION_SHORT = "ИЭ"

    PROCESS_FLOW_CHART_SHORT = "КТП"

    MOUNTING_DRAWING_SHORT = "МЧ"
    PROCESS_CHART_SHORT = "МК"

    PRODUCT_DESCRIPTION_SHORT = "ОИ"
    DATABASE_DESCRIPTION_SHORT = "ОБД"

    PROCESS_AND_TECHNOLOGY_DESCRIPTION_SHORT = "ПГ"
    GENERAL_SYSTEM_DESCRIPTION_SHORT = "ПД"
    EXPLANATORY_NOTE_PZ_SHORT = "ПЗ"
    TESTING_PROGRAMME_AND_PROCEDURE_PM_SHORT = "ПМ"
    PRODUCT_CERTIFICATE_SHORT = "ПС"

    ADMINISTRATOR_GUIDE_SHORT = "РА"
    INSTALLATION_GUIDE_SHORT = "РИ"
    CONFIGURATION_GUIDE_SHORT = "РН"
    CALCULATION_SHORT = "РР"
    SERVICE_CHARGE_SETTLEMENT_SHORT = "РТО"
    OPERATION_GUIDE_SHORT = "РЭ"

    ASSEMBLY_DRAWING_SHORT = "СБ"
    SECURITY_SYSTEM_GUIDE_SHORT = "СЗИ"

    PROCESSING_INSTRUCTION_SHORT = "ТИ"
    TECHNICAL_DESCRIPTION_SHORT = "ТО"
    BASIC_DESIGN_LIST_SHORT = "ТП"
    TECHNICAL_SPECIFICATION_SHORT = "ТУ"

    PACKING_DRAWING_SHORT = "УЧ"

    PRODUCT_STATUS_RECORD_FO_SHORT = "ФО"

    ELECTRO_SCHEMATIC_DIAGRAM_SHORT = "Э3"
    ELECTRO_CIRCUIT_DIAGRAM_SHORT = "Э4"
    ELECTRO_CONNECTIONS_DIAGRAM_SHORT = "Э5"
    LIST_OPERATION_PAPERS_ED_SHORT = "ЭД"
    LABEL_SHORT = "ЭТ"


class DocType(Enum):
    """
    Specify the document types.
    """
    AUTHENTIC_TEXT_HOLDERS_LIST = "Ведомость держателей подлинников"
    SPTA_SET_LIST = "Ведомость ЗИП"
    LIST_BOUGHT_IN_PAPERS = "Ведомость покупных изделий"
    LIST_BOUGHT_IN_PERMISSION_PAPERS = "Ведомость разрешения применения покупных изделий"
    LIST_SPECIFICATIONS = "Ведомость спецификаций"
    LIST_REFERENCE_PAPERS = "Ведомость ссылочных документов"
    LIST_ASSEMBLY_PAPERS = "Ведомость сборки изделия"
    BASIC_DESIGN_LIST = "Ведомость технического проекта"
    LIST_OPERATION_PAPERS = "Ведомость эксплуатационных документов"

    OPERATION_DOCUMENTATION_TYPES = "Виды для ЭД"

    OUTLINE_DRAWING = "Габаритный чертеж"

    INSTRUCTIONS = "Инструкции"
    SPTA_USE_INSTRUCTION = "Инструкция по использованию ЗИП-О"
    MOUNTING_LAUNCH_CONFIGURATION_TRIAL_INSTRUCTION = "Инструкция по монтажу, пуску, регулированию и обкатке изделия"
    MOUNTING_COMMISSIONING_INSTRUCTION = "Инструкция по монтажу и вводу в эксплуатацию"
    ANTIVIRUS_PROTECTION_MANAGEMENT_INSTRUCTION = "Инструкция по организации антивирусной защиты информации"
    DATABASE_MANAGEMENT_INSTRUCTION = "Инструкция по формированию и ведению базы данных"
    OPERATION_INSTRUCTION = "Инструкция по эксплуатации"

    PROCESS_FLOW_CHART = "Карта технологического процесса"
    DATABASE_CATALOG = "Каталог базы данных"
    CONFIGURATION_TEST_CASE = "Контрольный пример по настройке"

    PROCESS_CHART = "Маршрутная карта"
    MOUNTING_DRAWING = "Монтажный чертеж"

    GENERAL_SYSTEM_DESCRIPTION = "Общее описание системы"
    DATABASE_DESCRIPTION = "Описание базы данных"
    PRODUCT_DESCRIPTION = "Описание изделия"
    PROGRAM_DESCRIPTION = "Описание программы"
    USE_DESCRIPTION = "Описание применения"
    PROCESS_AND_TECHNOLOGY_DESCRIPTION = "Описание технологического процесса"

    PRODUCT_CERTIFICATE = "Паспорт"
    EXPLANATORY_NOTE = "Пояснительная записка"
    TESTING_PROGRAMME_AND_PROCEDURE = "Программа и методика испытаний"
    OTHERS = "Прочие документы"

    CALCULATION = "Расчеты"
    SERVICE_CHARGE_SETTLEMENT = "Расчет затрат на техническое обслуживание"

    INSPECTION_AND_MAINTENANCE_GUIDE = "Регламент технического обслуживания"

    ADMINISTRATOR_GUIDE = "Руководство администратора"
    SECURITY_ADMINISTRATOR_GUIDE = "Руководство администратора безопасности"
    SECURITY_SYSTEM_ADMINISTRATOR_GUIDE = "Руководство администратора СЗИ"
    OPERATOR_GUIDE = "Руководство оператора"
    SECURITY_TOOL_OPERATOR_GUIDE = "Руководство оператора КСЗ"
    USER_GUIDE = "Руководство пользователя"
    SECURITY_TOOL_SYSTEM_GUIDE = "Руководство по КСЗ"
    CONFIGURATION_GUIDE = "Руководство по настройке"
    SECURITY_SYSTEM_GUIDE = "Руководство по СЗИ"
    INSTALLATION_GUIDE = "Руководство по установке"
    OPERATION_GUIDE = "Руководство по эксплуатации"
    INFORMATION_SECURITY_OFFICER_GUIDE = "Руководство пользователя СЗИ"
    PROGRAMMER_GUIDE = "Руководство программиста"
    SYSTEM_PROGRAMMER_GUIDE = "Руководство системного программиста"

    ASSEMBLY_DRAWING = "Сборочный чертеж"
    JOINT_RESOLUTION = "Совместное решение"
    MESSAGES_OUTPUT = "Состав выходных данных (сообщений)"
    SPECIFICATION = "Спецификация"

    PRODUCT_COMPONENT_STRUCTURE = "Схема деления структурная"

    ELECTRO_CONNECTIONS_DIAGRAM = "Схема электрическая подключения"
    ELECTRO_SCHEMATIC_DIAGRAM = "Схема электрическая принципиальная"
    ELECTRO_CIRCUIT_DIAGRAM = "Схема электрическая соединений"

    SOURCE_CODE = "Текст программы"
    TECHNICAL_DESCRIPTION = "Техническое описание"
    TECHNICAL_SPECIFICATION = "Технические условия"
    PROCESSING_INSTRUCTION = "Технологическая инструкция"

    PACKING_DRAWING = "Упаковочный чертеж"
    PRODUCT_STATUS_RECORD = "Формуляр"
    DETAIL_DRAWING = "Чертеж детали"
    GENERAL_ARRANGEMENT_DRAWING = "Чертеж общего вида"
    LABEL = "Этикетка"


class Manufacturer(Enum):
    """
    Specify the product manufacturer company.
    """
    PROTEI_RD = "НТЦ ПРОТЕЙ"
    PROTEI_ST = "ПРОТЕЙ СТ"
    DEFAULT = ""


class DocClassification:
    index = 0

    def __init__(self,
                 doc_type: DocType,
                 doc_short: DocShort = None,
                 doc_category: DocCategory = None,
                 doc_standard: list[DocStandard] = None):
        self.identifier = DocClassification.index

        if doc_type is None:
            self.doc_type = None
        else:
            self.doc_type = doc_type.value

        if doc_short is None:
            self.doc_short = None
        else:
            self.doc_short = doc_short.value

        if doc_category is None:
            self.doc_category = None
        else:
            self.doc_category = doc_category.value

        if doc_standard is None:
            self.doc_standard = []
        else:
            self.doc_standard = [standard.value for standard in doc_standard]

        Const.dict_classification[self.identifier] = self
        DocClassification.index += 1

    def __str__(self):
        return f"{self.doc_type} ({self.doc_short}) --- {self.doc_category}, {self.doc_standard}"

    def __repr__(self):
        return f"DocClassification({self.doc_type}, {self.doc_short}, {self.doc_category}, {self.doc_standard})"

    def __hash__(self):
        return hash((self.doc_type, self.doc_short, self.doc_category, self.doc_standard))

    def __key(self):
        return self.doc_type, self.doc_short, self.doc_category, self.doc_standard

    def __eq__(self, other):
        if isinstance(other, DocClassification):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, DocClassification):
            return self.__key() != other.__key()
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, DocClassification):
            return self.doc_type < other.doc_type
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, DocClassification):
            return self.doc_type > other.doc_type
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, DocClassification):
            return self.doc_type <= other.doc_type
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, DocClassification):
            return self.doc_type >= other.doc_type
        else:
            return NotImplemented

    def provide(self):
        return self.doc_type, self.doc_category


def init_doc_classifications():
    DocClassification(DocType.LABEL, DocShort.LABEL_SHORT, DocCategory.DEVELOPMENT_DOC, [DocStandard.GOST_R_2_610_2019])
    DocClassification(DocType.DETAIL_DRAWING, None, DocCategory.DESIGN_DOC, [DocStandard.GOST_2_102_2013])
    DocClassification(DocType.PRODUCT_STATUS_RECORD, DocShort.PRODUCT_STATUS_RECORD_30_SHORT,
                      DocCategory.DEVELOPMENT_DOC, [])
    DocClassification(DocType.PRODUCT_STATUS_RECORD, DocShort.PRODUCT_STATUS_RECORD_FO_SHORT, DocCategory.OPERATION_DOC,
                      [DocStandard.GOST_R_2_610_2019])
    DocClassification(DocType.PACKING_DRAWING, DocShort.PACKING_DRAWING_SHORT, DocCategory.DESIGN_DOC,
                      [DocStandard.GOST_2_102_2013])
    DocClassification(DocType.PROCESSING_INSTRUCTION, DocShort.PROCESSING_INSTRUCTION_SHORT, DocCategory.PRODUCTION_DOC,
                      [DocStandard.GOST_3_1105_2011])
    DocClassification(DocType.TECHNICAL_DESCRIPTION, DocShort.TECHNICAL_DESCRIPTION_SHORT, DocCategory.DESIGN_DOC, [])
    DocClassification(DocType.TECHNICAL_SPECIFICATION, DocShort.TECHNICAL_SPECIFICATION_SHORT, DocCategory.DESIGN_DOC,
                      [DocStandard.GOST_2_114_2016])
    DocClassification(DocType.SOURCE_CODE, DocShort.SOURCE_CODE_SHORT, DocCategory.DEVELOPMENT_DOC,
                      [DocStandard.GOST_19_401_78])
    DocClassification(DocType.ELECTRO_CIRCUIT_DIAGRAM, DocShort.ELECTRO_CIRCUIT_DIAGRAM_SHORT, DocCategory.DESIGN_DOC,
                      [DocStandard.GOST_2_701_2008])
    DocClassification(DocType.ELECTRO_SCHEMATIC_DIAGRAM, DocShort.ELECTRO_SCHEMATIC_DIAGRAM_SHORT,
                      DocCategory.DESIGN_DOC, [DocStandard.GOST_2_701_2008])
    DocClassification(DocType.ELECTRO_CONNECTIONS_DIAGRAM, DocShort.ELECTRO_CONNECTIONS_DIAGRAM_SHORT,
                      DocCategory.DESIGN_DOC, [DocStandard.GOST_2_701_2008])
    DocClassification(DocType.PRODUCT_COMPONENT_STRUCTURE, DocShort.PRODUCT_COMPONENT_STRUCTURE_SHORT,
                      DocCategory.DESIGN_DOC, [DocStandard.GOST_R_2_711_2019])
    DocClassification(DocType.SPECIFICATION, None, DocCategory.DESIGN_DOC, [DocStandard.GOST_2_102_2013])
    DocClassification(DocType.SPECIFICATION, None, DocCategory.DEVELOPMENT_DOC, [DocStandard.GOST_19_202_78])
    DocClassification(DocType.MESSAGES_OUTPUT, DocShort.MESSAGES_OUTPUT_SHORT, DocCategory.DESIGN_DOC, [])
    DocClassification(DocType.JOINT_RESOLUTION, DocShort.JOINT_RESOLUTION_SHORT, DocCategory.DEVELOPMENT_DOC,
                      [DocStandard.STO_202_2019])
    DocClassification(DocType.ASSEMBLY_DRAWING, DocShort.ASSEMBLY_DRAWING_SHORT, DocCategory.DESIGN_DOC,
                      [DocStandard.GOST_2_102_2013])
    DocClassification(DocType.SYSTEM_PROGRAMMER_GUIDE, DocShort.SYSTEM_PROGRAMMER_GUIDE_SHORT,
                      DocCategory.DEVELOPMENT_DOC, [DocStandard.GOST_19_503_79])
    DocClassification(DocType.PROGRAMMER_GUIDE, DocShort.PROGRAMMER_GUIDE_SHORT, DocCategory.DEVELOPMENT_DOC,
                      [DocStandard.GOST_19_504_79])
    DocClassification(DocType.INFORMATION_SECURITY_OFFICER_GUIDE, DocShort.INFORMATION_SECURITY_OFFICER_GUIDE_SHORT,
                      DocCategory.DEVELOPMENT_DOC, [DocStandard.STO_202_2019])
    DocClassification(DocType.USER_GUIDE, DocShort.USER_GUIDE_SHORT, DocCategory.DESIGN_DOC, [DocStandard.STO_202_2019])
    DocClassification(DocType.USER_GUIDE, DocShort.USER_GUIDE_SHORT, DocCategory.OPERATION_DOC,
                      [DocStandard.GOST_34_201_89])
    DocClassification(DocType.OPERATION_GUIDE, DocShort.OPERATION_GUIDE_SHORT, DocCategory.OPERATION_DOC,
                      [DocStandard.GOST_2_610_2006])
    DocClassification(DocType.OPERATION_GUIDE, DocShort.OPERATION_GUIDE_SHORT, DocCategory.DEVELOPMENT_DOC, [])
    DocClassification(DocType.SECURITY_SYSTEM_GUIDE, DocShort.SECURITY_SYSTEM_GUIDE_SHORT, DocCategory.DEVELOPMENT_DOC,
                      [])
    DocClassification(DocType.CONFIGURATION_GUIDE, DocShort.CONFIGURATION_GUIDE_SHORT, DocCategory.DEVELOPMENT_DOC, [])
    DocClassification(DocType.SECURITY_TOOL_SYSTEM_GUIDE, DocShort.SECURITY_TOOL_SYSTEM_GUIDE_D6_SHORT,
                      DocCategory.DEVELOPMENT_DOC, [DocStandard.STO_202_2019])
    DocClassification(DocType.SECURITY_TOOL_SYSTEM_GUIDE, DocShort.SECURITY_TOOL_SYSTEM_GUIDE_D5_SHORT,
                      DocCategory.DEVELOPMENT_DOC, [DocStandard.STO_202_2019])
    DocClassification(DocType.INSTALLATION_GUIDE, DocShort.INSTALLATION_GUIDE_SHORT, DocCategory.DEVELOPMENT_DOC, [])
    DocClassification(DocType.SECURITY_TOOL_OPERATOR_GUIDE, DocShort.SECURITY_TOOL_OPERATOR_GUIDE_SHORT,
                      DocCategory.DEVELOPMENT_DOC, [DocStandard.STO_202_2019])
    DocClassification(DocType.OPERATOR_GUIDE, DocShort.OPERATOR_GUIDE_SHORT, DocCategory.DEVELOPMENT_DOC,
                      [DocStandard.GOST_19_505_79])
    DocClassification(DocType.SECURITY_SYSTEM_ADMINISTRATOR_GUIDE, DocShort.SECURITY_SYSTEM_ADMINISTRATOR_GUIDE_SHORT,
                      DocCategory.DEVELOPMENT_DOC, [])
    DocClassification(DocType.SECURITY_ADMINISTRATOR_GUIDE, DocShort.SECURITY_ADMINISTRATOR_GUIDE_SHORT,
                      DocCategory.DEVELOPMENT_DOC, [])
    DocClassification(DocType.ADMINISTRATOR_GUIDE, DocShort.ADMINISTRATOR_GUIDE_SHORT, DocCategory.DEVELOPMENT_DOC, [])
    DocClassification(DocType.INSPECTION_AND_MAINTENANCE_GUIDE, DocShort.INSPECTION_AND_MAINTENANCE_GUIDE_SHORT,
                      DocCategory.DESIGN_DOC, [])
    DocClassification(DocType.CALCULATION, DocShort.CALCULATION_SHORT, DocCategory.BASIC_DESIGN,
                      [DocStandard.GOST_R_2_106_2019])
    DocClassification(DocType.SERVICE_CHARGE_SETTLEMENT, DocShort.SERVICE_CHARGE_SETTLEMENT_SHORT,
                      DocCategory.DESIGN_DOC, [])
    DocClassification(DocType.OTHERS, DocShort.OTHERS_SHORT, DocCategory.DEVELOPMENT_DOC, [])
    DocClassification(DocType.TESTING_PROGRAMME_AND_PROCEDURE, DocShort.TESTING_PROGRAMME_AND_PROCEDURE_51_SHORT,
                      DocCategory.DEVELOPMENT_DOC, [DocStandard.GOST_19_301_79])
    DocClassification(DocType.TESTING_PROGRAMME_AND_PROCEDURE, DocShort.TESTING_PROGRAMME_AND_PROCEDURE_PM_SHORT,
                      DocCategory.DESIGN_DOC, [DocStandard.GOST_R_2_610_2019])
    DocClassification(DocType.EXPLANATORY_NOTE, DocShort.EXPLANATORY_NOTE_PZ_SHORT, DocCategory.BASIC_DESIGN,
                      [DocStandard.GOST_R_2_106_2019, DocStandard.GOST_2_119_2013, DocStandard.GOST_2_120_2013])
    DocClassification(DocType.EXPLANATORY_NOTE, DocShort.EXPLANATORY_NOTE_81_SHORT, DocCategory.DEVELOPMENT_DOC,
                      [DocStandard.GOST_19_404_79])
    DocClassification(DocType.PRODUCT_CERTIFICATE, DocShort.PRODUCT_CERTIFICATE_SHORT, DocCategory.DEVELOPMENT_DOC, [])
    DocClassification(DocType.PROCESS_AND_TECHNOLOGY_DESCRIPTION, DocShort.PROCESS_AND_TECHNOLOGY_DESCRIPTION_SHORT,
                      DocCategory.DESIGN_DOC, [])
    DocClassification(DocType.PROGRAM_DESCRIPTION, DocShort.PROGRAM_DESCRIPTION_SHORT, DocCategory.DEVELOPMENT_DOC,
                      [DocStandard.GOST_19_402_78])
    DocClassification(DocType.USE_DESCRIPTION, DocShort.USE_DESCRIPTION_SHORT, DocCategory.DEVELOPMENT_DOC,
                      [DocStandard.GOST_19_502_78])
    DocClassification(DocType.PRODUCT_DESCRIPTION, DocShort.PRODUCT_DESCRIPTION_SHORT, DocCategory.DEVELOPMENT_DOC, [])
    DocClassification(DocType.DATABASE_DESCRIPTION, DocShort.DATABASE_DESCRIPTION_SHORT, DocCategory.DEVELOPMENT_DOC,
                      [])
    DocClassification(DocType.GENERAL_SYSTEM_DESCRIPTION, DocShort.GENERAL_SYSTEM_DESCRIPTION_SHORT,
                      DocCategory.DESIGN_DOC, [])
    DocClassification(DocType.MOUNTING_DRAWING, DocShort.MOUNTING_DRAWING_SHORT, DocCategory.DESIGN_DOC,
                      [DocStandard.GOST_2_102_2013])
    DocClassification(DocType.PROCESS_CHART, DocShort.PROCESS_CHART_SHORT, DocCategory.PRODUCTION_DOC,
                      [DocStandard.GOST_3_1118_82])
    DocClassification(DocType.CONFIGURATION_TEST_CASE, DocShort.CONFIGURATION_TEST_CASE_SHORT, DocCategory.DESIGN_DOC,
                      [DocStandard.STO_202_2019])
    DocClassification(DocType.DATABASE_CATALOG, DocShort.DATABASE_CATALOG_SHORT, DocCategory.DESIGN_DOC, [])
    DocClassification(DocType.PROCESS_FLOW_CHART, DocShort.PROCESS_FLOW_CHART_SHORT, DocCategory.PRODUCTION_DOC,
                      [DocStandard.GOST_3_1404_86])
    DocClassification(DocType.SPTA_USE_INSTRUCTION, DocShort.SPTA_USE_INSTRUCTION_SHORT, DocCategory.DESIGN_DOC,
                      [DocStandard.STO_202_2019, DocStandard.GOST_2_601_2019])
    DocClassification(DocType.OPERATION_INSTRUCTION, DocShort.OPERATION_INSTRUCTION_SHORT, DocCategory.DEVELOPMENT_DOC,
                      [])
    DocClassification(DocType.DATABASE_MANAGEMENT_INSTRUCTION, DocShort.DATABASE_MANAGEMENT_INSTRUCTION_SHORT,
                      DocCategory.DESIGN_DOC, [])
    DocClassification(DocType.ANTIVIRUS_PROTECTION_MANAGEMENT_INSTRUCTION,
                      DocShort.ANTIVIRUS_PROTECTION_MANAGEMENT_INSTRUCTION_SHORT, DocCategory.DEVELOPMENT_DOC,
                      [DocStandard.STO_202_2019])
    DocClassification(DocType.MOUNTING_LAUNCH_CONFIGURATION_TRIAL_INSTRUCTION,
                      DocShort.MOUNTING_COMMISSIONING_INSTRUCTION_SHORT, DocCategory.OPERATION_DOC,
                      [DocStandard.GOST_R_2_610_2019])
    DocClassification(DocType.MOUNTING_COMMISSIONING_INSTRUCTION, DocShort.MOUNTING_COMMISSIONING_INSTRUCTION_SHORT,
                      DocCategory.DEVELOPMENT_DOC, [])
    DocClassification(DocType.INSTRUCTIONS, DocShort.INSTRUCTIONS_SHORT, DocCategory.DESIGN_DOC,
                      [DocStandard.GOST_2_106_96])
    DocClassification(DocType.OUTLINE_DRAWING, DocShort.OUTLINE_DRAWING_SHORT, DocCategory.DESIGN_DOC,
                      [DocStandard.GOST_2_109_73])
    DocClassification(DocType.OPERATION_DOCUMENTATION_TYPES, DocShort.OPERATION_DOCUMENTATION_TYPES_SHORT,
                      DocCategory.DESIGN_DOC, [])
    DocClassification(DocType.LIST_OPERATION_PAPERS, DocShort.LIST_OPERATION_PAPERS_ED_SHORT, DocCategory.OPERATION_DOC,
                      [DocStandard.GOST_R_2_610_2019])
    DocClassification(DocType.LIST_OPERATION_PAPERS, DocShort.LIST_OPERATION_PAPERS_PROGRAMMING_SHORT,
                      DocCategory.DEVELOPMENT_DOC, [DocStandard.GOST_R_2_610_2019])
    DocClassification(DocType.LIST_OPERATION_PAPERS, DocShort.LIST_OPERATION_PAPERS_20_SHORT,
                      DocCategory.DEVELOPMENT_DOC, [DocStandard.GOST_19_507_79])
    DocClassification(DocType.BASIC_DESIGN_LIST, DocShort.BASIC_DESIGN_LIST_SHORT, DocCategory.BASIC_DESIGN,
                      [DocStandard.GOST_2_106_96, DocStandard.GOST_2_120_2013])
    DocClassification(DocType.LIST_REFERENCE_PAPERS, DocShort.LIST_REFERENCE_PAPERS_SHORT, DocCategory.DESIGN_DOC,
                      [DocStandard.GOST_R_2_106_2019])
    DocClassification(DocType.LIST_SPECIFICATIONS, DocShort.LIST_SPECIFICATIONS_SHORT, DocCategory.DESIGN_DOC,
                      [DocStandard.GOST_R_2_106_2019])
    DocClassification(DocType.LIST_ASSEMBLY_PAPERS, DocShort.LIST_ASSEMBLY_PAPERS_SHORT, DocCategory.PRODUCTION_DOC,
                      [DocStandard.GOST_3_1122_84])
    DocClassification(DocType.LIST_BOUGHT_IN_PERMISSION_PAPERS, DocShort.LIST_BOUGHT_IN_PERMISSION_PAPERS_SHORT,
                      DocCategory.DESIGN_DOC, [DocStandard.GOST_R_2_106_2019])
    DocClassification(DocType.LIST_BOUGHT_IN_PAPERS, DocShort.LIST_BOUGHT_IN_PAPERS_SHORT, DocCategory.DESIGN_DOC,
                      [DocStandard.GOST_R_2_106_2019])
    DocClassification(DocType.SPTA_SET_LIST, DocShort.SPTA_SET_LIST_SHORT, DocCategory.OPERATION_DOC,
                      [DocStandard.GOST_R_2_610_2019])
    DocClassification(DocType.AUTHENTIC_TEXT_HOLDERS_LIST, DocShort.AUTHENTIC_TEXT_HOLDERS_LIST_SHORT,
                      DocCategory.DEVELOPMENT_DOC, [DocStandard.GOST_19_403_79])
    DocClassification(DocType.GENERAL_ARRANGEMENT_DRAWING, DocShort.GENERAL_ARRANGEMENT_DRAWING_SHORT,
                      DocCategory.DESIGN_DOC, [])


class DocProduct:
    attrs = ("doc_type", "doc_short", "doc_category", "doc_standard")
    index = 0

    def __init__(self,
                 name: str,
                 class_id: int,
                 summary: str = None,
                 language: Language = Language.RUS,
                 customer: str = None,
                 shipment: str = None,
                 update_date: datetime.date = datetime.date.today()):
        self.identifier = DocProduct.index

        self.name = name
        self.class_id = class_id
        self.summary = summary
        self.language = language.value
        self.customer = customer
        self.shipment = shipment
        self.update_date = update_date

        Const.dict_doc_product[self.identifier] = self
        DocProduct.index += 1

    def __str__(self):
        return f"{self.name} ({Const.dict_classification[self.class_id]}), дата создания: {self.update_date}"

    def __repr__(self):
        return f"DocProduct({self.name}, {self.class_id}, {self.summary}, {Language(self.language)}, " \
               f"{self.customer}, {self.shipment}, {self.update_date})"

    def __hash__(self):
        return hash((self.name, self.class_id, self.language))

    def __key(self):
        return self.name, self.class_id, self.language

    def __eq__(self, other):
        if isinstance(other, DocProduct):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, DocProduct):
            return self.__key() != other.__key()
        else:
            return NotImplemented

    def __classification(self) -> Optional[DocClassification]:
        if self.class_id is not None:
            return Const.dict_classification[self.class_id]
        else:
            return None

    def get_class_attr(self, attr: str) -> Optional[Union[str, list[str]]]:
        return object.__getattribute__(self.__classification(), attr)

    def get_all_class_attr(self) -> list[Optional[Union[str, list[str]]]]:
        return [self.get_class_attr(attr) for attr in DocProduct.attrs]

    def comply_pattern(self, mask: str, attr: str) -> Optional[bool]:
        if attr == "name":
            return re.search(mask, self.name, re.IGNORECASE) is not None
        else:
            return None

    def provide(self):
        return self.name, self.customer, self.shipment


class Product:
    index = 0
    doc_attrs = ("name", "class_id", "summary", "language", "customer", "shipment", "update_date")
    doc_class_attrs = ("doc_type", "doc_short", "doc_category", "doc_standard")

    def __init__(self,
                 name: str,
                 version: str = None,
                 project: str = None,
                 notation: list[str] = None,
                 serial: str = None,
                 manufacturer: Manufacturer = Manufacturer.DEFAULT,
                 docs: list[int] = None,
                 tags: list[str] = None):
        self.identifier = Product.index
        self.name = name
        self.version = version
        self.project = project
        if notation is None:
            notation = []
        self.notation = notation
        self.serial = serial
        self.manufacturer = manufacturer
        if docs is None:
            docs = []
        self.docs = docs
        if tags is None:
            tags = []
        self.tags = tags

        Const.dict_product[self.identifier] = self
        Product.index += 1

        Const.set_tags.update(self.tags)

    def __str__(self):
        return f"{self.name} ({self.version}) --- {self.project}, {self.notation}"

    def __repr__(self):
        return f"Product({self.name}, {self.version}, {self.project}, {self.notation}, {self.serial}, " \
               f"{self.manufacturer}, {self.docs}, {self.tags})"

    def __hash__(self):
        return hash((self.name, self.version, self.project))

    def __key(self):
        return self.name, self.version, self.project, self.serial

    def __eq__(self, other):
        if isinstance(other, Product):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Product):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __docs(self) -> Optional[list[DocProduct]]:
        return [self.__doc(doc_id) for doc_id in self.docs]

    def __doc(self, doc_id: int) -> Optional[DocProduct]:
        if doc_id in self.docs:
            return Const.dict_doc_product[doc_id]
        else:
            print(f"KeyError, {doc_id} is not a proper identifier.")
            return None

    def get_all_doc_names(self):
        return [doc.name for doc in self.__docs()]

    def get_all_doc_types(self):
        return [doc.get_class_attr("doc_type") for doc in self.__docs()]

    def get_doc_attr(self, doc_id: int, attr: str):
        return object.__getattribute__(self.__doc(doc_id), attr)

    def get_all_doc_attr(self, doc_id: int):
        return [self.get_doc_attr(doc_id, attr) for attr in Product.doc_attrs]

    def get_doc_class_attr(self, doc_id: int, doc_attr: str):
        return self.__doc(doc_id).get_class_attr(doc_attr)


def main():
    pass


if __name__ == "__main__":
    main()
