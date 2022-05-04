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
