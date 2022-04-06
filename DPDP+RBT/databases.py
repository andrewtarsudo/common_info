from pprint import pprint
import re
from typing import Optional


def parse_db_info():
    # dict_indexes = {0: "Parameter", 1: "Type", 2: "NULL", 3: "Key", 4: "Default", 5: "Extra"}
    print("Lines to parse:")
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []
    res: list[list[str]] = [list_1, list_2, list_3, list_4, list_5, list_6]
    sentinel = ""
    num_lines = -1

    for line in iter(input, sentinel):
        parse_line = line.split(sep="|")
        num_lines = len(parse_line)
        parsed_line = []

        for val in parse_line:
            if val:
                parsed_line.append(val)

        for index, item in enumerate(parsed_line):
            if index in (-1, 8):
                continue
            else:
                if not item.strip():
                    res[index].append("------")
                else:
                    res[index].append(f"{item.strip()}")

    for idx, res_list in enumerate(res):
        for value in res_list:
            if value == "------":
                print()
            else:
                print(value)
    print("++++++++++end++++++++++")
    print(f"lines: {num_lines}")


def line_join(lines: list[str]):
    pattern = r'\\t'
    items = [re.escape(pattern).join((str(line),)) for line in lines]
    return ''.join(items)


def parse_db_rows():
    sentinel = ""
    final_lines: list[str] = []

    for line in iter(input, sentinel):
        if line.startswith("+"):
            continue
        else:
            line_updated = line[1:-1]
            print(line_updated)
            pattern = re.compile(r'\s*\|\s*')
            line_mod = re.sub(pattern=pattern, repl="\t", string=line_updated)
            final_lines.append(line_mod)

    for final_line in final_lines:
        print(final_line)


def parse_db_rows_item(item):
    final_lines: list[str] = []
    for line in item:
        if line.startswith("+"):
            continue
        else:
            line_updated = line[1:-1]
            pattern = re.compile(r'\s*\|\s*')
            line_mod = re.sub(pattern=pattern, repl="\t", string=line_updated)
            final_lines.append(line_mod.lstrip())

    final_lines[0].rstrip()

    pattern_final = re.compile(r"Field\tType\tNull\tKey\tDefault\tExtra")
    pattern_null = re.compile(r"NULL\t")
    pattern_auto_increment = re.compile(r"auto_increment ")

    for final_line in final_lines:
        line_null = re.sub(pattern=pattern_null, repl="", string=final_line)
        line_res = re.sub(pattern=pattern_auto_increment, repl="Auto_increment.", string=line_null)

        if line_res and not re.match(pattern_final, line_res) and not line_res.startswith("+"):
            print(line_res)


class DpdpRbt:
    ip_server = "192.168.125.148"
    web_port = 8081
    login = "root"
    password = "elephant"
    command = "mysql -uroot -p"
    db_password = "elephant"

    dict_db_parameters = {
        'content_id': 'Content identifier.',
        'external_id': 'External service identifier.',
        'hlr_id': 'HLR node identifier.',
        'is_default': 'Flag to set as a default value.\nDefault: false.',
        'is_hidden': 'Flag not to display the content.',
        'msisdn': 'Subscriber MSISDN.',
        'partner_id': 'Partner identifier.',
        'price': 'Subscription price.',
        'product_id': 'Service product identifier.',
        'provider_id': 'Content provider identifier.',
        'purchase_fee': 'Purchase price.',
        'purchase_id': 'Purchase policy identifier.',
        'refund_information': 'Information about the refund conditions.',
        'renewal_fee': 'Renewal price.',
        'renewal_id': 'Renewal policy identifier.',
        'service_variant_id': 'Service option identifier.',
        'subscriber_id': 'Subscriber identifier.',
        'subscription_id': 'Subscription identifier.',
        'service_id': 'Service identifier.',
        'channel_id': 'Identifier of the media channel.',
        'channel': 'Media channel name.'
    }

    dict_default_text = {
        "heading_name": "Table {table_name}",
        "summary": "The parameters of the table {table_name} are provided below."
    }

    dict_rbt_dpdp: dict[str, dict] = {"dict_db_parameters": dict_db_parameters, "dict_default_text": dict_default_text}

    list_questions: list[tuple[str, str]] = []

    list_types = [
        "bigint(M)", "bit(M)", "blob", "datetime(M)", "int(M)", "json", "text", "timestamp", "varchar(M)",
        "smallint(M)", "longtext", "tinyint(M)"]

    @classmethod
    def get_dict_value(cls):
        value = input('Print the parameter name:\n')
        if value in cls.dict_db_parameters.keys():
            print(cls.dict_db_parameters[value])
        else:
            print(f"The parameter {value} is not in the dict.")
            print("Available names:")
            pprint(cls.dict_db_parameters.keys())

    @classmethod
    def print_out(cls):
        print(f"ip server = {cls.ip_server}")
        print(f"web interface port = {cls.web_port}")
        print(f"command = {cls.command}")
        print(f"login = {cls.login}")
        print(f"password = {cls.password}")
        print(f"db_password = {cls.db_password}")
        print("dict:")
        pprint(cls.dict_rbt_dpdp,)
        cls.print_questions()
        print(f"types = {cls.list_types}")

    @classmethod
    def print_questions(cls):
        for index, question in enumerate(cls.list_questions):
            pprint(f"Q{index + 1} - {question};")

    @classmethod
    def print_dict(cls, dict_name: str):
        if dict_name in cls.dict_rbt_dpdp.keys():
            print(f"{dict_name}:")
            pprint(cls.dict_rbt_dpdp[dict_name])
        else:
            print(f"ValueError. {dict_name} does not exist yet.")

    @classmethod
    def check_types(cls, new_types: list[str]) -> list[str]:
        return [new_type for new_type in modify_types(new_types) if new_type not in cls.list_types]

    @classmethod
    def add_types(cls, new_types: list[str]):
        add_types = cls.check_types(new_types)
        cls.list_types.append(*add_types)
        return cls.list_types

    @classmethod
    def print_new_types(cls, kind_type: str, types: list[str]):
        kind_types = kind_type.strip().lower()
        if kind_types == "new":
            pprint(types)
        elif kind_types == "modified":
            pprint(modify_types(types))
        elif kind_types == "check":
            pprint(cls.check_types(types))
        elif kind_types == "add":
            pprint(cls.add_types(types))
        else:
            print('There is no such types. "NEW", "MODIFIED", "CHECK", "ADD".')


class RbtWeb(DpdpRbt):
    def __init__(self):
        super().__init__()

    dict_channel_id = {
        "0": "IVR",
        "1": "SMS",
        "2": "WEB",
        "3": "USSD",
        "4": "API",
        "5": "OKP",
        "6": "SERVICE",
        "7": "RETAIL",
        "8": "SYSTEM"
    }

    dict_operation = {
        "0": "AUTHORIZATION",
        "1": "CREATION",
        "2": "MODIFICATION",
        "3": "DELETING",
        "4": "PROVIDING",
        "5": "MODERATION",
        "6": "ACTIVATING",
        "7": "DEACTIVATING",
        "8": "REQUEST",
        "9": "CANCEL_REQUEST"
    }

    dict_object_type = {
        "1": "USER",
        "2": "ROLE",
        "3": "ALBUM",
        "5": "ARTIST",
        "7": "TONE",
        "10": "PLAYLIST",
        "13": "LICENSE",
        "14": "CATEGORY",
        "15": "PRICE_CATEGORY",
        "16": "SUBSCRIBER",
        "19": "VAS",
        "20": "SMS_TEMPLATE",
        "21": "SETTINGS",
        "22": "CONTENT_LIST",
        "23": "RULE",
        "24": "SUBSCRIBER_RBT_PRIVACY",
        "25": "SUBSCRIBER_RBT_OVERLAY",
        "26": "DIY_TONE",
        "27": "CALLER_GROUP",
        "28": "PARTNER",
        "29": "SERVICE"
    }

    dict_caller_group_type = {
        "0": "GENERAL",
        "1": "FAVORITE",
        "2": "BLACKLIST",
        "3": "None"
    }

    dict_order = {
        "default rule": (0, 10_000),
        "schedule rule": (10_001, 20_000),
        "group rule": (20_001, 30_000),
        "caller rule": (30_001, 40_000),
        "unknown_rule": (40_001, 50_000)
    }

    dict_subscriber_type = {
        "0": "subscriber",
        "1": "corporate"
    }

    dict_content_type = {
        "0": "TONE",
        "1": "PLAYLIST"
    }

    dict_rule_mode = {
        "0": "RANDOM",
        "1": "ORDERED"
    }

    dict_rule_type = {
        "0": "GENERAL",
        "1": "AntiRBT"
    }

    dict_rbt_dpdp = {
        "channel_id": dict_channel_id,
        "operation": dict_operation,
        "object_type": dict_object_type,
        "caller_group_type": dict_caller_group_type,
        "order": dict_order,
        "subscriber_type": dict_subscriber_type,
        "content_type": dict_content_type,
        "rule_mode": dict_rule_mode,
        "rule_type": dict_rule_type
    }

    list_questions = [("rbt type", "subscriber.type"), ("unknown_rule", "rule.order"), ("id", "subscriber_content.id")]


class DpdpCore(DpdpRbt):
    def __init__(self):
        super().__init__()

    dict_operation = {
        "0": "AUTHORIZATION",
        "1": "CREATION",
        "2": "MODIFICATION",
        "3": "DELETING",
        "4": "PROVIDING",
        "5": "MODERATION",
        "6": "ACTIVATING",
        "7": "DEACTIVATING",
        "8": "REQUEST",
        "9": "CANCEL_REQUEST"
    }

    dict_rbt_dpdp = {
        "operation": dict_operation,
    }

    list_state = ["SUSPENDED", "INACTIVE", "PRE_ACTIVE", "ACTIVE", "GRACE", "PENDING"]

    list_provider_type = ["CONTENT_PROVIDER", "SERVICE_PROVIDER", "BOTH"]

    list_questions = (
        ("remove", "RepoMetadata.remove"), ("url", "SenderMessage.url"), ("node_name", "TaskQueue.node_name"),
        ("remote_task_id", "TaskQueue.remote_task_id"), ("owner", "TaskQueue.owner"),
        ("purchase_id", "price_category.purchase_id"), ("is_file_present", "content.is_file_present"),
        ("type", "notification_webhook.type")
    )
    list_channels = ["IVR", "SMS", "WEB", "USSD", "API", "OKP", "SERVICE", "RETAIL", "SYSTEM"]


def divide_item(item: str, name_from_list: str) -> tuple[str, list[str]]:
    list_items: list[str] = item.split('\n')

    if not list_items[1].strip().startswith(('|', '+')):
        name = list_items[1].strip()
        num_start = 2
    else:
        name = name_from_list
        num_start = 1

    return name, list_items[num_start:]


def modify_types(list_types: list[str]):
    list_modified_types: list[str] = []
    pattern = re.compile(r"(.*)\(\d+\)")

    for new_type in list_types:
        match = re.match(pattern, new_type)
        if match:
            list_modified_types.append(f"{match.group(0)}(M)")
        else:
            list_modified_types.append(new_type)

    return list_modified_types


def get_info_tables(tables: list[str], command_db: str) -> Optional[str]:
    if command_db == "describe":
        print_strings: list[str] = [f"describe {table};" for table in tables]
    elif command_db == "select":
        print_strings: list[str] = [f"SELECT * FROM {table};" for table in tables]
    else:
        return None

    return " ".join(print_strings)


def full_parse_db(list_parse: list[str]):
    list_names = [
        "album", "album_category", "app_settings", "artist", "audit", "category", "content_list",
        "content_list_content", "license", "partner", "playlist", "playlist_content", "provided_content", "raw_album",
        "raw_album_category", "raw_artist", "raw_custom_tone", "raw_license", "raw_partner", "raw_partner_service",
        "raw_playlist", "raw_playlist_content", "raw_service_variant", "raw_tone", "raw_tone_category", "role", "tone",
        "tone_category", "user", "user_moderator", "user_role"]

    for index, item in enumerate(list_parse):
        name, list_items = divide_item(item, list_names[index])
        print('----------')
        print(f"{name}")
        parse_db_rows_item(list_items)
        print('----------')


def main():
    # item = [
    #     """
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | Field           | Type         | Null | Key | Default             | Extra                         |
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | id              | int(11)      | NO   | PRI | NULL                | auto_increment                |
    #     | creation_time   | timestamp    | NO   |     | current_timestamp() | on update current_timestamp() |
    #     | creator_id      | int(11)      | NO   | MUL | NULL                |                               |
    #     | name            | varchar(255) | NO   | MUL | NULL                |                               |
    #     | thumbnail       | blob         | YES  |     | NULL                |                               |
    #     | releaseYear     | int(11)      | YES  |     | NULL                |                               |
    #     | moderation_time | timestamp    | YES  |     | NULL                |                               |
    #     | moderator_id    | int(11)      | YES  | MUL | NULL                |                               |
    #     | update_time     | timestamp    | YES  |     | NULL                |                               |
    #     | updater_id      | int(11)      | YES  | MUL | NULL                |                               |
    #     | artist_id       | int(11)      | YES  | MUL | NULL                |                               |
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     """,
    #     """
    #     +-------------+---------+------+-----+---------+-------+
    #     | Field       | Type    | Null | Key | Default | Extra |
    #     +-------------+---------+------+-----+---------+-------+
    #     | album_id    | int(11) | NO   | MUL | NULL    |       |
    #     | category_id | int(11) | NO   | MUL | NULL    |       |
    #     +-------------+---------+------+-----+---------+-------+
    #     """,
    #     """
    #     +--------------------------+---------+------+-----+---------+----------------+
    #     | Field                    | Type    | Null | Key | Default | Extra          |
    #     +--------------------------+---------+------+-----+---------+----------------+
    #     | id                       | int(11) | NO   | PRI | NULL    | auto_increment |
    #     | custom_price_category_id | int(11) | YES  |     | NULL    |                |
    #     +--------------------------+---------+------+-----+---------+----------------+
    #     """,
    #     """
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | Field           | Type         | Null | Key | Default             | Extra                         |
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | id              | int(11)      | NO   | PRI | NULL                | auto_increment                |
    #     | creation_time   | timestamp    | NO   |     | current_timestamp() | on update current_timestamp() |
    #     | creator_id      | int(11)      | NO   | MUL | NULL                |                               |
    #     | name            | varchar(255) | NO   | UNI | NULL                |                               |
    #     | thumbnail       | blob         | YES  |     | NULL                |                               |
    #     | moderation_time | timestamp    | YES  |     | NULL                |                               |
    #     | moderator_id    | int(11)      | YES  | MUL | NULL                |                               |
    #     | update_time     | timestamp    | YES  |     | NULL                |                               |
    #     | updater_id      | int(11)      | YES  | MUL | NULL                |                               |
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     """,
    #     """
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | Field           | Type         | Null | Key | Default             | Extra                         |
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | id              | int(11)      | NO   | PRI | NULL                | auto_increment                |
    #     | date_time       | timestamp    | NO   |     | current_timestamp() | on update current_timestamp() |
    #     | user_id         | int(11)      | YES  | MUL | NULL                |                               |
    #     | user_ip         | varchar(255) | YES  |     | NULL                |                               |
    #     | channel_id      | int(11)      | YES  |     | NULL                |                               |
    #     | msisdn          | bigint(20)   | YES  |     | NULL                |                               |
    #     | operation       | int(11)      | NO   |     | NULL                |                               |
    #     | object_type     | int(11)      | NO   | MUL | NULL                |                               |
    #     | props           | longtext     | NO   |     | NULL                |                               |
    #     | object_owner_id | int(11)      | YES  | MUL | NULL                |                               |
    #     | product_id      | bigint(20)   | YES  |     | NULL                |                               |
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     """,
    #     """
    #     +---------------+--------------+------+-----+---------------------+-------------------------------+
    #     | Field         | Type         | Null | Key | Default             | Extra                         |
    #     +---------------+--------------+------+-----+---------------------+-------------------------------+
    #     | id            | int(11)      | NO   | PRI | NULL                | auto_increment                |
    #     | creation_time | timestamp    | NO   |     | current_timestamp() | on update current_timestamp() |
    #     | creator_id    | int(11)      | NO   | MUL | NULL                |                               |
    #     | name          | varchar(255) | NO   | UNI | NULL                |                               |
    #     | update_time   | timestamp    | YES  |     | NULL                |                               |
    #     | updater_id    | int(11)      | YES  | MUL | NULL                |                               |
    #     +---------------+--------------+------+-----+---------------------+-------------------------------+
    #     """,
    #     """
    #     +----------------+--------------+------+-----+---------------------+----------------+
    #     | Field          | Type         | Null | Key | Default             | Extra          |
    #     +----------------+--------------+------+-----+---------------------+----------------+
    #     | id             | int(11)      | NO   | PRI | NULL                | auto_increment |
    #     | name           | varchar(255) | NO   | UNI | NULL                |                |
    #     | content_orders | longtext     | NO   |     | NULL                |                |
    #     | creator_id     | int(11)      | NO   | MUL | NULL                |                |
    #     | creation_time  | timestamp    | NO   |     | current_timestamp() |                |
    #     +----------------+--------------+------+-----+---------------------+----------------+
    #     """,
    #     """
    #     +-----------------+------------+------+-----+---------+-------+
    #     | Field           | Type       | Null | Key | Default | Extra |
    #     +-----------------+------------+------+-----+---------+-------+
    #     | content_list_id | int(11)    | NO   | PRI | NULL    |       |
    #     | content_id      | bigint(20) | NO   | PRI | NULL    |       |
    #     +-----------------+------------+------+-----+---------+-------+
    #     """,
    #     """
    #     +---------------+--------------+------+-----+---------------------+-------------------------------+
    #     | Field         | Type         | Null | Key | Default             | Extra                         |
    #     +---------------+--------------+------+-----+---------------------+-------------------------------+
    #     | id            | int(11)      | NO   | PRI | NULL                | auto_increment                |
    #     | creation_time | timestamp    | NO   |     | current_timestamp() | on update current_timestamp() |
    #     | expire_date   | timestamp    | YES  |     | NULL                |                               |
    #     | name          | varchar(255) | NO   | UNI | NULL                |                               |
    #     | provider_id   | int(11)      | YES  | MUL | NULL                |                               |
    #     | update_time   | timestamp    | YES  |     | NULL                |                               |
    #     | updater_id    | int(11)      | YES  | MUL | NULL                |                               |
    #     +---------------+--------------+------+-----+---------------------+-------------------------------+
    #     """,
    #     """
    #     +--------------------+--------------+------+-----+---------+----------------+
    #     | Field              | Type         | Null | Key | Default | Extra          |
    #     +--------------------+--------------+------+-----+---------+----------------+
    #     | id                 | bigint(20)   | NO   | PRI | NULL    | auto_increment |
    #     | type               | int(11)      | NO   |     | NULL    |                |
    #     | business_division  | int(11)      | NO   |     | NULL    |                |
    #     | company_name       | varchar(255) | NO   | MUL | NULL    |                |
    #     | company_owner_name | varchar(255) | NO   |     | NULL    |                |
    #     | address            | varchar(255) | NO   |     | NULL    |                |
    #     | point_of_contact   | varchar(255) | NO   |     | NULL    |                |
    #     | contact_number     | varchar(255) | NO   |     | NULL    |                |
    #     | point_of_contact2  | varchar(255) | NO   |     | NULL    |                |
    #     | contact_number2    | varchar(255) | NO   |     | NULL    |                |
    #     | email              | varchar(255) | NO   |     | NULL    |                |
    #     | agreements_no      | varchar(255) | NO   |     | NULL    |                |
    #     +--------------------+--------------+------+-----+---------+----------------+
    #     """,
    #     """
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | Field           | Type         | Null | Key | Default             | Extra                         |
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | id              | int(11)      | NO   | PRI | NULL                | auto_increment                |
    #     | name            | varchar(255) | NO   | UNI | NULL                |                               |
    #     | creation_time   | timestamp    | NO   |     | current_timestamp() | on update current_timestamp() |
    #     | creator_id      | int(11)      | NO   | MUL | NULL                |                               |
    #     | thumbnail       | blob         | YES  |     | NULL                |                               |
    #     | moderation_time | timestamp    | YES  |     | NULL                |                               |
    #     | moderator_id    | int(11)      | YES  | MUL | NULL                |                               |
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     """,
    #     """
    #     +-------------+------------+------+-----+---------+-------+
    #     | Field       | Type       | Null | Key | Default | Extra |
    #     +-------------+------------+------+-----+---------+-------+
    #     | playlist_id | int(11)    | NO   | MUL | NULL    |       |
    #     | content_id  | bigint(20) | YES  | MUL | NULL    |       |
    #     +-------------+------------+------+-----+---------+-------+
    #     """,
    #     """
    #     +-------------------+------------+------+-----+---------------------+-------------------------------+
    #     | Field             | Type       | Null | Key | Default             | Extra                         |
    #     +-------------------+------------+------+-----+---------------------+-------------------------------+
    #     | content_id        | bigint(20) | NO   | PRI | NULL                |                               |
    #     | creation_time     | timestamp  | NO   |     | current_timestamp() | on update current_timestamp() |
    #     | creator_id        | int(11)    | YES  | MUL | NULL                |                               |
    #     | price_category_id | int(11)    | NO   |     | NULL                |                               |
    #     | order_code        | bigint(20) | YES  | UNI | NULL                |                               |
    #     | is_hidden         | bit(1)     | NO   |     | NULL                |                               |
    #     | tone_id           | bigint(20) | YES  | MUL | NULL                |                               |
    #     | playlist_id       | int(11)    | YES  | MUL | NULL                |                               |
    #     | is_expired        | bit(1)     | YES  |     | b'0'                |                               |
    #     +-------------------+------------+------+-----+---------------------+-------------------------------+
    #     """,
    #     """
    #     +----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | Field          | Type         | Null | Key | Default             | Extra                         |
    #     +----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | id             | int(11)      | NO   | PRI | NULL                | auto_increment                |
    #     | creator_id     | int(11)      | NO   | MUL | NULL                |                               |
    #     | name           | varchar(255) | YES  | MUL | NULL                |                               |
    #     | operation_time | timestamp    | NO   |     | current_timestamp() | on update current_timestamp() |
    #     | thumbnail      | blob         | YES  |     | NULL                |                               |
    #     | releaseYear    | int(11)      | YES  |     | NULL                |                               |
    #     | is_moderate    | bit(1)       | NO   |     | NULL                |                               |
    #     | moderator_id   | int(11)      | YES  | MUL | NULL                |                               |
    #     | album_id       | int(11)      | YES  | MUL | NULL                |                               |
    #     | artist_id      | int(11)      | YES  | MUL | NULL                |                               |
    #     +----------------+--------------+------+-----+---------------------+-------------------------------+
    #     """,
    #     """
    #     +--------------+---------+------+-----+---------+-------+
    #     | Field        | Type    | Null | Key | Default | Extra |
    #     +--------------+---------+------+-----+---------+-------+
    #     | raw_album_id | int(11) | NO   | MUL | NULL    |       |
    #     | category_id  | int(11) | NO   | MUL | NULL    |       |
    #     +--------------+---------+------+-----+---------+-------+
    #     """,
    #     """
    #     +----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | Field          | Type         | Null | Key | Default             | Extra                         |
    #     +----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | id             | int(11)      | NO   | PRI | NULL                | auto_increment                |
    #     | creator_id     | int(11)      | YES  | MUL | NULL                |                               |
    #     | name           | varchar(255) | YES  |     | NULL                |                               |
    #     | operation_time | timestamp    | NO   |     | current_timestamp() | on update current_timestamp() |
    #     | thumbnail      | blob         | YES  |     | NULL                |                               |
    #     | is_moderate    | bit(1)       | NO   |     | NULL                |                               |
    #     | artist_id      | int(11)      | YES  | MUL | NULL                |                               |
    #     | moderator_id   | int(11)      | YES  | MUL | NULL                |                               |
    #     +----------------+--------------+------+-----+---------------------+-------------------------------+
    #     """,
    #     """
    #     +----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | Field          | Type         | Null | Key | Default             | Extra                         |
    #     +----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | id             | int(11)      | NO   | PRI | NULL                | auto_increment                |
    #     | name           | varchar(255) | YES  |     | NULL                |                               |
    #     | operation_time | timestamp    | NO   |     | current_timestamp() | on update current_timestamp() |
    #     | is_moderate    | bit(1)       | NO   |     | NULL                |                               |
    #     | msisdn         | bigint(20)   | YES  |     | NULL                |                               |
    #     | moderator_id   | int(11)      | YES  | MUL | NULL                |                               |
    #     +----------------+--------------+------+-----+---------------------+-------------------------------+
    #     """,
    #     """
    #     +----------------+--------------+------+-----+---------+----------------+
    #     | Field          | Type         | Null | Key | Default | Extra          |
    #     +----------------+--------------+------+-----+---------+----------------+
    #     | id             | int(11)      | NO   | PRI | NULL    | auto_increment |
    #     | creator_id     | int(11)      | YES  | MUL | NULL    |                |
    #     | name           | varchar(255) | YES  |     | NULL    |                |
    #     | expire_date    | timestamp    | YES  |     | NULL    |                |
    #     | operation_time | timestamp    | YES  |     | NULL    |                |
    #     | moderator_id   | int(11)      | YES  | MUL | NULL    |                |
    #     | license_id     | int(11)      | YES  | MUL | NULL    |                |
    #     +----------------+--------------+------+-----+---------+----------------+
    #     """,
    #     """
    #     +--------------------+--------------+------+-----+---------------------+-------------------------------+
    #     | Field              | Type         | Null | Key | Default             | Extra                         |
    #     +--------------------+--------------+------+-----+---------------------+-------------------------------+
    #     | id                 | bigint(20)   | NO   | PRI | NULL                | auto_increment                |
    #     | type               | int(11)      | NO   |     | NULL                |                               |
    #     | business_division  | int(11)      | NO   |     | NULL                |                               |
    #     | company_name       | varchar(255) | NO   | MUL | NULL                |                               |
    #     | company_owner_name | varchar(255) | NO   |     | NULL                |                               |
    #     | address            | varchar(255) | NO   |     | NULL                |                               |
    #     | point_of_contact   | varchar(255) | NO   |     | NULL                |                               |
    #     | contact_number     | varchar(255) | NO   |     | NULL                |                               |
    #     | point_of_contact2  | varchar(255) | NO   |     | NULL                |                               |
    #     | contact_number2    | varchar(255) | NO   |     | NULL                |                               |
    #     | email              | varchar(255) | NO   |     | NULL                |                               |
    #     | agreements_no      | varchar(255) | NO   |     | NULL                |                               |
    #     | creation_time      | timestamp    | NO   |     | current_timestamp() | on update current_timestamp() |
    #     | moderator_id       | int(11)      | YES  | MUL | NULL                |                               |
    #     +--------------------+--------------+------+-----+---------------------+-------------------------------+
    #     """,
    #     """
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | Field           | Type         | Null | Key | Default             | Extra                         |
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | id              | int(11)      | NO   | PRI | NULL                | auto_increment                |
    #     | name            | varchar(255) | NO   |     | NULL                |                               |
    #     | hlr_id          | int(11)      | YES  |     | NULL                |                               |
    #     | is_hlr_required | bit(1)       | YES  |     | NULL                |                               |
    #     | is_default      | bit(1)       | YES  |     | NULL                |                               |
    #     | creation_time   | timestamp    | NO   |     | current_timestamp() | on update current_timestamp() |
    #     | creator_id      | int(11)      | YES  | MUL | NULL                |                               |
    #     | moderator_id    | int(11)      | YES  | MUL | NULL                |                               |
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     """,
    #     """
    #     +-------------------+--------------+------+-----+---------+----------------+
    #     | Field             | Type         | Null | Key | Default | Extra          |
    #     +-------------------+--------------+------+-----+---------+----------------+
    #     | id                | int(11)      | NO   | PRI | NULL    | auto_increment |
    #     | creator_id        | int(11)      | NO   | MUL | NULL    |                |
    #     | moderator_id      | int(11)      | YES  | MUL | NULL    |                |
    #     | name              | varchar(255) | YES  |     | NULL    |                |
    #     | operation_time    | timestamp    | YES  |     | NULL    |                |
    #     | order_code        | bigint(20)   | YES  |     | NULL    |                |
    #     | price_category_id | int(11)      | YES  |     | NULL    |                |
    #     | thumbnail         | blob         | YES  |     | NULL    |                |
    #     | is_moderate       | bit(1)       | NO   |     | NULL    |                |
    #     | playlist_id       | int(11)      | YES  | MUL | NULL    |                |
    #     +-------------------+--------------+------+-----+---------+----------------+
    #     """,
    #     """
    #     +-----------------+------------+------+-----+---------+-------+
    #     | Field           | Type       | Null | Key | Default | Extra |
    #     +-----------------+------------+------+-----+---------+-------+
    #     | raw_playlist_id | int(11)    | NO   | MUL | NULL    |       |
    #     | content_id      | bigint(20) | YES  | MUL | NULL    |       |
    #     +-----------------+------------+------+-----+---------+-------+
    #     """,
    #     """
    #     +------------------------------+--------------+------+-----+---------------------+-------------------------------+
    #     | Field                        | Type         | Null | Key | Default             | Extra                         |
    #     +------------------------------+--------------+------+-----+---------------------+-------------------------------+
    #     | id                           | int(11)      | NO   | PRI | NULL                | auto_increment                |
    #     | name                         | varchar(255) | NO   |     | NULL                |                               |
    #     | service_id                   | int(11)      | NO   |     | NULL                |                               |
    #     | price_id                     | int(11)      | NO   |     | NULL                |                               |
    #     | variant                      | int(11)      | NO   |     | NULL                |                               |
    #     | type_id                      | int(11)      | NO   |     | NULL                |                               |
    #     | is_hidden                    | bit(1)       | NO   |     | NULL                |                               |
    #     | is_default                   | bit(1)       | NO   |     | NULL                |                               |
    #     | downgrade_service_variant_id | int(11)      | YES  |     | NULL                |                               |
    #     | renewal_policy_id            | int(11)      | NO   |     | NULL                |                               |
    #     | profit_multiplier            | int(11)      | YES  |     | NULL                |                               |
    #     | discount_multiplier          | int(11)      | YES  |     | NULL                |                               |
    #     | creation_time                | timestamp    | NO   |     | current_timestamp() | on update current_timestamp() |
    #     | creator_id                   | int(11)      | YES  | MUL | NULL                |                               |
    #     | moderator_id                 | int(11)      | YES  | MUL | NULL                |                               |
    #     +------------------------------+--------------+------+-----+---------------------+-------------------------------+
    #     """,
    #     """
    #     +-------------------+--------------+------+-----+---------------------+-------------------------------+
    #     | Field             | Type         | Null | Key | Default             | Extra                         |
    #     +-------------------+--------------+------+-----+---------------------+-------------------------------+
    #     | id                | int(11)      | NO   | PRI | NULL                | auto_increment                |
    #     | creator_id        | int(11)      | NO   | MUL | NULL                |                               |
    #     | moderator_id      | int(11)      | YES  | MUL | NULL                |                               |
    #     | operation_time    | timestamp    | NO   |     | current_timestamp() | on update current_timestamp() |
    #     | order_code        | bigint(20)   | YES  |     | NULL                |                               |
    #     | price_category_id | int(11)      | YES  |     | NULL                |                               |
    #     | title             | varchar(255) | YES  |     | NULL                |                               |
    #     | album_id          | int(11)      | YES  | MUL | NULL                |                               |
    #     | artist_id         | int(11)      | YES  | MUL | NULL                |                               |
    #     | tone_id           | bigint(20)   | YES  | MUL | NULL                |                               |
    #     | license_id        | int(11)      | YES  | MUL | NULL                |                               |
    #     | is_moderate       | bit(1)       | NO   |     | NULL                |                               |
    #     +-------------------+--------------+------+-----+---------------------+-------------------------------+
    #     """,
    #     """
    #     +-------------+---------+------+-----+---------+-------+
    #     | Field       | Type    | Null | Key | Default | Extra |
    #     +-------------+---------+------+-----+---------+-------+
    #     | raw_tone_id | int(11) | NO   | MUL | NULL    |       |
    #     | category_id | int(11) | NO   | MUL | NULL    |       |
    #     +-------------+---------+------+-----+---------+-------+
    #     """,
    #     """
    #     +---------------+--------------+------+-----+---------+----------------+
    #     | Field         | Type         | Null | Key | Default | Extra          |
    #     +---------------+--------------+------+-----+---------+----------------+
    #     | id            | int(11)      | NO   | PRI | NULL    | auto_increment |
    #     | name          | varchar(255) | NO   | UNI | NULL    |                |
    #     | privileges    | longtext     | NO   |     | NULL    |                |
    #     | session_limit | int(11)      | YES  |     | NULL    |                |
    #     +---------------+--------------+------+-----+---------+----------------+
    #     """,
    #     """
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | Field           | Type         | Null | Key | Default             | Extra                         |
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     | id              | bigint(20)   | NO   | PRI | NULL                | auto_increment                |
    #     | creation_time   | timestamp    | NO   |     | current_timestamp() | on update current_timestamp() |
    #     | creator_id      | int(11)      | NO   | MUL | NULL                |                               |
    #     | title           | varchar(255) | NO   | MUL | NULL                |                               |
    #     | moderation_time | timestamp    | YES  |     | NULL                |                               |
    #     | moderator_id    | int(11)      | YES  | MUL | NULL                |                               |
    #     | album_id        | int(11)      | YES  | MUL | NULL                |                               |
    #     | artist_id       | int(11)      | YES  | MUL | NULL                |                               |
    #     | license_id      | int(11)      | NO   | MUL | NULL                |                               |
    #     +-----------------+--------------+------+-----+---------------------+-------------------------------+
    #     """,
    #     """
    #     +-------------+------------+------+-----+---------+-------+
    #     | Field       | Type       | Null | Key | Default | Extra |
    #     +-------------+------------+------+-----+---------+-------+
    #     | tone_id     | bigint(20) | NO   | PRI | NULL    |       |
    #     | category_id | int(11)    | NO   | PRI | NULL    |       |
    #     +-------------+------------+------+-----+---------+-------+
    #     """,
    #     """
    #     +------------+---------------+------+-----+---------+----------------+
    #     | Field      | Type          | Null | Key | Default | Extra          |
    #     +------------+---------------+------+-----+---------+----------------+
    #     | id         | int(11)       | NO   | PRI | NULL    | auto_increment |
    #     | name       | varchar(255)  | NO   | UNI | NULL    |                |
    #     | last_login | timestamp     | YES  |     | NULL    |                |
    #     | is_blocked | bit(1)        | NO   |     | b'0'    |                |
    #     | partner_id | bigint(20)    | YES  | MUL | NULL    |                |
    #     | product_id | bigint(20)    | YES  |     | NULL    |                |
    #     | ip_masks   | varchar(1024) | YES  |     | NULL    |                |
    #     +------------+---------------+------+-----+---------+----------------+
    #     """,
    #     """
    #     +--------------+---------+------+-----+---------+-------+
    #     | Field        | Type    | Null | Key | Default | Extra |
    #     +--------------+---------+------+-----+---------+-------+
    #     | user_id      | int(11) | NO   | MUL | NULL    |       |
    #     | moderator_id | int(11) | NO   | MUL | NULL    |       |
    #     +--------------+---------+------+-----+---------+-------+
    #     """,
    #     """
    #     +---------+---------+------+-----+---------+-------+
    #     | Field   | Type    | Null | Key | Default | Extra |
    #     +---------+---------+------+-----+---------+-------+
    #     | user_id | int(11) | NO   | MUL | NULL    |       |
    #     | role_id | int(11) | NO   | MUL | NULL    |       |
    #     +---------+---------+------+-----+---------+-------+
    #     """
    # ]
    # full_parse_db(item)
    # tables = [
    #     "album", "album_category", "app_settings", "artist", "audit", "category", "content_list",
    #     "content_list_content", "license", "partner", "playlist", "playlist_content", "provided_content", "raw_album",
    #     "raw_album_category", "raw_artist", "raw_custom_tone", "raw_license", "raw_partner", "raw_partner_service",
    #     "raw_playlist", "raw_playlist_content", "raw_service_variant", "raw_tone", "raw_tone_category", "role", "tone",
    #     "tone_category", "user", "user_moderator", "user_role"]
    # for table in tables:
    #     print(table)
    # print(get_info_tables(tables, "select"))
    # DpdpCore.print_questions()
    DpdpRbt.get_dict_value()


if __name__ == "__main__":
    main()
