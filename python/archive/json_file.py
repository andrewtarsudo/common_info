import hashlib
import json
from json import JSONDecodeError
from typing import Union, Optional
# from archive import Ward, Shelf, DocFolder, FileRecord, Const
from pathlib import Path
import logging
from pprint import pprint


logging.basicConfig()


class JSONFile:
    dict_item = {
        "ward": ("ward_name", "shelf_id", "identifier"),
        "shelf": ("ward_id", "shelf_number", "folder_id", "identifier"),
        "folder": ("ward_id", "shelf_id", "name", "file_id", "identifier"),
        "file": ("ward_id", "shelf_id", "folder_id", "name", "doc_type", "serial_number", "product", "identifier")
    }

    def __init__(self, path: Union[str, Path]):
        self.path = path
        self._is_validated = self.check_path()

    def __str__(self):
        return f"JSON file: {Path(self.path).resolve()}, validated: {self._is_validated}"

    def __repr__(self):
        return f"JSONFile({self.path})"

    def __eq__(self, other):
        if isinstance(other, JSONFile):
            return self.path == other.path
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, JSONFile):
            return self.path != other.path
        else:
            return NotImplemented

    def __hash__(self):
        return hash((id(self), self.path))

    def __len__(self):
        return len(self.parse_file)

    def check_path(self) -> bool:
        flag = False
        try:
            with open(self.path, "r") as file:
                json.load(file)
        except FileNotFoundError as e:
            logging.error(f"FileNotFoundError, {e.errno}, {e.strerror}.")
        except PermissionError as e:
            logging.error(f"PermissionError, {e.errno}, {e.strerror}.")
        except NameError as e:
            logging.error(f"NameError, {e.name}, {str(e)}.")
        except OSError as e:
            logging.error(f"OSError, {e.errno}, {e.strerror}.")
        except JSONDecodeError as e:
            logging.error(f"JSONDecodeError,{e.lineno}, {e.msg}.")
        else:
            flag = True
        finally:
            return flag

    @property
    def __content(self) -> Optional[dict]:
        if self._is_validated:
            with open(self.path, "r") as file:
                content = json.load(file)
            return content
        else:
            logging.critical(f"File is incorrect.")
            exit()

    def __getitem__(self, item):
        if item in ("ward", "shelf", "folder", "file"):
            return self.__content[item]
        else:
            logging.info(f"KeyError, {item} is not an appropriate item.")
            return None

    def __parse_item(self, item):
        result = []
        for value in self.__getitem__(item):
            result_item = [value[param] for param in JSONFile.dict_item[item]]
            result.append(result_item)
        return result

    @property
    def parse_file(self):
        dict_parsed_file = dict()
        for item in ("ward", "shelf", "folder", "file"):
            dict_parsed_file[item] = self.__parse_item(item)
        return dict_parsed_file

    # def get_items(self):
    #     for ward_name, shelf_id, identifier in self.parsed_file["ward"]:
    #         Ward(ward_name, shelf_id, identifier)
    #     for ward_id, shelf_number, folder_id, identifier in self.parsed_file["shelf"]:
    #         Shelf(ward_id, shelf_number, folder_id, identifier)
    #     for ward_id, shelf_id, name, file_id, identifier in self.parsed_file["folder"]:
    #         DocFolder(ward_id, shelf_id, name, file_id, identifier)
    #     for ward_id, shelf_id, folder_id, name, doc_type, serial_number, product, identifier in self.parsed_file["file"]:
    #         FileRecord(ward_id, shelf_id, folder_id, name, doc_type, serial_number, product, identifier)

    def write_to_file(self):
        dict_to_json = dict()
        dict_to_json["ward"] = []
        dict_to_json["shelf"] = []
        dict_to_json["folder"] = []
        dict_to_json["file"] = []

        for ward_name, shelf_id, identifier in self.parse_file["ward"]:
            item = {"identifier": identifier, "ward_name": ward_name, "shelf_id": shelf_id}
            dict_to_json["ward"].append(item)
        for ward_id, shelf_number, folder_id, identifier in self.parse_file["shelf"]:
            item = {"identifier": identifier, "ward_id": ward_id, "shelf_number": shelf_number, "folder_id": folder_id}
            dict_to_json["shelf"].append(item)
        for ward_id, shelf_id, name, file_id, identifier in self.parse_file["folder"]:
            item = {"identifier": identifier, "ward_id": ward_id, "shelf_id": shelf_id, "file_id": file_id}
            dict_to_json["folder"].append(item)
        for ward_id, shelf_id, folder_id, name, doc_type, serial_number, product, identifier in self.parse_file["file"]:
            item = {"identifier": identifier, "ward_id": ward_id, "shelf_id": shelf_id, "folder_id": folder_id,
                    "name": name, "doc_type": doc_type, "serial_number": serial_number, "product": product}
            dict_to_json["file"].append(item)

        return dict_to_json


def main():
    params = ("name", "cabinet_name", "shelf_no", "folder_name", "doc_type", "serial", "product", "commentary")
    # with open("test.json", "r") as file:
    #     dict_items = json.load(file)

    # print(dict_items)

    config = JSONFile("test.json")
    with open("test.json", "r") as file:
        content = json.load(file)

    dict_content = dict()

    for item in content["file"]:
        print(item)
        name = item["name"]
        dict_content[name] = []
        dict_content[name].append([item[param] for param in params])

    print(dict_content)


if __name__ == "__main__":
    main()

"""
Вид документа	Краткое название	Тип документа	ГОСТ
Этикетка	ЭТ	Программная документация	ГОСТ Р 2.610-2019		
Чертеж детали		Конструкторская документация	ГОСТ 2.102-2013		
Формуляр	30	Программная документация	ГОСТ 19.501-87		
Формуляр	ФО	Эксплуатационная документация	ГОСТ Р 2.610-2019		
Упаковочный чертеж	УЧ	Конструкторская документация	ГОСТ 2.102-2013		
Технологическая инструкция	ТИ	Технологическая документация	ГОСТ 3.1105-2011		
Техническое описание	ТО	Конструкторская документация			
Технические условия	ТУ	Конструкторская документация	ГОСТ 2.114-2016		
Текст программы	12	Программная документация	ГОСТ 19.401-78		
Схема электрическая соединений	Э4	Конструкторская документация	ГОСТ 2.701-2008		
Схема электрическая принципиальная	Э3	Конструкторская документация	ГОСТ 2.701-2008		
Схема электрическая подключения	Э5	Конструкторская документация	ГОСТ 2.701-2008		
Схема деления структурная	Е1	Конструкторская документация	ГОСТ Р 2.711-2019		
Спецификация		Конструкторская документация	ГОСТ 2.102-2013		
Спецификация	-	Программная документация	ГОСТ 19.202-78		
Состав выходных данных (сообщений) 	В8	Конструкторская документация			
Совместное решение	Д9	Программная документация	СТО 202-2019		
Сборочный чертеж	СБ	Конструкторская документация	ГОСТ 2.102-2013		
Руководство системного программиста	32	Программная документация	ГОСТ 19.503-79		
Руководство программиста	33	Программная документация	ГОСТ 19.504-79		
Руководство пользователя СЗИ	Д4	Программная документация	СТО 202-2019		
Руководство пользователя	И3	Конструкторская документация	СТО 202-2019		
Руководство пользователя	И3	Эксплуатационная документация	ГОСТ 34.201-89		
Руководство по эксплуатации	РЭ	Эксплуатационная документация	ГОСТ 2.610--2006		
Руководство по эксплуатации 	РЭ	Программная документация			
Руководство по системе защиты информации	СЗИ	Программная документация			
Руководство по настройке	РН	Программная документация			
Руководство по КСЗ	Д6	Программная документация	СТО 202-2019		
Руководство по комплексу средств защиты	Д5	Программная документация	СТО 202-2019		
Руководство по инсталяции	РИ	Программная документация			
Руководство оператора КСЗ	Д7	Программная документация	СТО 202-2019		
Руководство оператора	34	Программная документация	ГОСТ 19.505-79		
Руководство администратора СЗИ	Д3	Программная документация			
Руководство администратора безопасности	И5	Программная документация			
Руководство администратора	РА	Программная документация			
Регламент технического обслуживания	ИС	Конструкторская документация			
Расчеты	РР	Технический проект	ГОСТ Р 2.106-2019		
Расчет затрат на техническое обслуживание	РТО	Конструкторская документация			
Прочие документы	90-99	Программная документация	надо расписать 90, 91...99 из СТО		
Программа и методика испытаний	51	Программная документация	ГОСТ 19.301-79		
Программа и методика испытаний	ПМ	Конструкторская документация	ГОСТ Р 2.610-2019, ГОСТ РВ 15.211		
Пояснительная записка	ПЗ	Технический проект	ГОСТ Р 2.106-2019, ГОСТ 2.119, ГОСТ 2.120		
Пояснительная записка	81	Программная документация	ГОСТ 19.404-79		
Паспорт	ПС	Программная документация	по ГОСТ д.б. ФО только!!!		
Описание технологического процесса	ПГ	Конструкторская документация			
Описание программы	13	Программная документация	ГОСТ 19.402-78		
Описание применения	31	Программная документация	ГОСТ 19.502-78		
Описание изделия	ОИ	Программная документация			
Описание базы данных	ОБД	Программная документация			
Общее описание системы	ПД	Конструкторская документация			
Монтажный чертеж	МЧ	Конструкторская документация	ГОСТ 2.102-2013		
Маршрутная карта	МК	Технологическая документация	ГОСТ 3.1118-82		
Контрольный пример по настройке	Д8	Конструкторская документация	СТО 202-2019		
Каталог базы данных	В7	Конструкторская документация			
Карта технологического процесса	КТП	Технологическая документация	ГОСТ 3.1404-86		
Инстуркция по использованию ЗИП-О	И1	Конструкторская документация	СТО 202-2019, ГОСТ 2.601		
Инструкция по эксплуатации	ИЭ	Программная документация			
Инструкция по формированию и ведению базы данных (набора данных)	И4	Конструкторская документация			
Инструкция по организации антивирусной защиты информации	Д11	Программная документация	СТО 202-2019		
Инструкция по монтажу, пуску, регулированию и обкатке изделия	ИМ	Эксплуатационная документация	ГОСТ Р 2.610-2019		
Инструкция по монтажу и вводу в эксплуатацию	ИМ	Программная документация			
Инструкции	И	Конструкторская документация	ГОСТ 2.106-96		
Габаритный чертеж	ГЧ	Конструкторская документация	ГОСТ 2.109-73		
Виды для ЭД	ВдЭД	Конструкторская документация	-		
Ведомость эксплуатационных документов	ЭД	Эксплуатационная документация	ГОСТ Р 2.610-2019		
Ведомость эксплуатационных документов	ВЭ	Программная документация	ГОСТ Р 2.610-2019		
Ведомость эксплуатационных документов	20	Программная документация	ГОСТ 19.507-79		
Ведомость технического проекта	ТП	Технический проект	ГОСТ 2.106, ГОСТ 2.120		
Ведомость ссылочных документов	ВД	Конструкторская документация	ГОСТ Р 2.106-2019		
Ведомость спецификаций	ВС	Конструкторская документация	ГОСТ Р 2.106-2019		
Ведомость сборки изделия	ВП/ВСИ	Технологическая документация	ГОСТ 3.1122-84		
Ведомость разрешения применения покупных изделий	ВИ	Конструкторская документация	ГОСТ Р 2.106-2019		
Ведомость покупных изделий	ВП	Конструкторская документация	ГОСТ Р 2.106-2019		
Ведомость ЗИП	ЗИ	Эксплуатационная документация	ГОСТ Р 2.610-2019		
Ведомость держателей подлинников	05	Программная документация	ГОСТ 19.403-79		
	ВО	Конструкторская документация		

Тип документа
Технический проект
Конструкторская документация
Программная документация
Эксплуатационная документация
Технологическая документация
Зарубежье



34

mAccess.MTU
  
Абонентский шлюз mAccess.MTU

НТЦ Протей
    

РИ

mAccess.MTU
  
Абонентский шлюз mAccess.MTU

НТЦ Протей
    

34

mAccess.MTU
  
Абонентский шлюз mAccess.MTU

НТЦ Протей
    

ТО

mAccess.MTU
  
Абонентский шлюз mAccess.MTU

НТЦ Протей
    

34

mAccess.MTU
  
Абонентский шлюз mAccess.MTU

НТЦ Протей
    

34

mAccess.MTU
  
Абонентский шлюз mAccess.MTU

НТЦ Протей
    

34

mAccess.MAK
  
Абонентский концентратор (mAccess.MAK)

НТЦ Протей
    

РИ

mAccess.MAK
  
Абонентский концентратор (mAccess.MAK)

НТЦ Протей
    

ТО

mAccess.MAK
  
Абонентский концентратор (mAccess.MAK)

НТЦ Протей
    

34

mAccess.MAK
  
Абонентский концентратор (mAccess.MAK)

НТЦ Протей
    

90-99

IVR

ПАМР.467144.001 90

Прямая линия
      

ИМ

IVR

ПАМР.467144.001 ИМ

Прямая линия
      

ПЗ

IVR
  
Прямая линия
      

51

IVR

ПАМР.467144.001 П2

Прямая линия
      

РЭ

IVR
  
Прямая линия
      

ТО

IVR
  
Прямая линия
      

34

GTR-Probe
  
GTR-Probe

НТЦ Протей
    

34

GGSN/P-GW (eng)
  
GPRS Gateway Support Node (GGSN/P-GW)

НТЦ Протей
    

РА

DeviceMonitor

ПАМР.467144.001 И3-06

Прямая линия
      

34

DeviceMonitor

ПАМР.467144.001 И3-05

Прямая линия
      

34

CAMEL GateWay
  
CAMEL Gateaway/Proxy (Camel_GW)

НТЦ Протей
    

34

CAMEL Gateaway (eng)
  
CAMEL Gateaway/Proxy (Camel_GW)

НТЦ Протей
    

34

Протей-imSwitch5 (web-интерфейс администратора)
  
112-Псковская область

Псков Система 112
    

РА

Protei DPI (eng)
  
Платформа DPI (DPI)

НТЦ Протей

Система видеонаблюдения опытного образца АПК "Безопасный город"

40412735.АПКБГООСВН.14417.ПГ

СВН АПК ТС БГ

Омский филиал ПАО "Ростелеком" (VP)
    

И5

Система видеонаблюдения опытного образца АПК "Безопасный город"

40412735.АПКБГОО.14417.И5

СВН АПК ТС БГ

Омский филиал ПАО "Ростелеком" (VP)
    

31

Система видеонаблюдения опытного образца АПК "Безопасный город"

40412735.АПКБГООСВН.14417.31

СВН АПК ТС БГ

Омский филиал ПАО "Ростелеком" (VP)
    

И3

Система видеонаблюдения опытного образца АПК "Безопасный город"

40412735.АПКБГООСВН.14417.И3

СВН АПК ТС БГ

Омский филиал ПАО "Ростелеком" (VP)
    

ИС

Система видеонаблюдения опытного образца АПК "Безопасный город"

40412735.АПКБГООСВН.14417.ИС

СВН АПК ТС БГ

Омский филиал ПАО "Ростелеком" (VP)
    

В8

Система видеонаблюдения опытного образца АПК "Безопасный город"

40412735.АПКБГООСВН.14417.В8

СВН АПК ТС БГ

Омский филиал ПАО "Ростелеком" (VP)
    

ИЭ

Система видеонаблюдения опытного образца АПК "Безопасный город"

40412735.АПКБГООСВН.14417.ИЭ

СВН АПК ТС БГ

Омский филиал ПАО "Ростелеком" (VP)
    

ФО

Система видеонаблюдения опытного образца АПК "Безопасный город"

40412735.АПКБГООСВН.14417.ФО

СВН АПК ТС БГ

Омский филиал ПАО "Ростелеком" (VP)
    

  12345

Показано 1 из 7 страниц, всего 206 записей
Сортировать по
Дата создания
Менеджер
Проект

Организация-разработчик
Тип документа

Вид документа
Утвержденный
Да
Любой
Нет
Текст документа
Ключевые слова

	Вид	Наименование	Обозначение	Проект	Компания
Версия
Версия
Вид документа
Руководство оператора
Тип исполнения
Электронный
Проект
УТК УСПО-112
Обозначение
Инв. №
"""
