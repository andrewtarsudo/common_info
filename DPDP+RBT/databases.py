import errno
import pathlib
from pprint import pprint
import re
from typing import Optional, Union
import json

__doc__ = """
    divide_item: divide the db item into strings;
    modify_types: change type(int) to type(M);
    get_info_tables: get the list of commands for the db
        describe: "describe {table_name};"
        select: "SELECT * FROM {table_name};"
    line_join: add tabulation;
    parse_db_rows_item: parse one table from the database;
    full_parse_db: parse the whole output of the database;
    """


class DpdpRbt:
    __doc__ = """
    add_types: add new types to the list;
    check_types: get the list of new types;
    get_dict_value: get the value from the dict_db_parameters;
    print_default_text: print default sentences;
    print_dict: print all dictionaries;
    print_new_types: print any types:
        "NEW", "MODIFIED", "CHECK", "ADD"
    print_out: print the following
        ip server, command, login, password, db_password, dict_rbt_dpdp, list_questions, list_types
    print_questions: print the list_questions;

    "command",
    "db_password",
    "dict_caller_group_type",
    "dict_channel_id",
    "dict_content_type",
    "dict_db_parameters",
    "dict_default_text",
    "dict_object_type",
    "dict_operation",
    "dict_order",
    "dict_rbt_dpdp",
    "dict_rule_mode",
    "dict_rule_type",
    "dict_subscriber_type",
    "get_dict_value",
    "ip_server",
    "list_channels",
    "list_dpdp_core_questions",
    "list_partner_type",
    "list_questions",
    "list_rbt_web_questions",
    "list_state",
    "list_types",
    "login",
    "password",
    "web_port"
    """
    dict_common_params: dict = {
        "ip_server": "192.168.125.148",
        "web_port": 8081,
        "login": "root",
        "password": "elephant",
        "command": "mysql -uroot -p",
        "db_password": "elephant"
    }

    dict_default_text = {
        "heading_name": "Table {table_name}",
        "summary": "The parameters of the table {table_name} are provided below.",
        "table_name": "Field description"
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
        "0": "SUBSCRIBER",
        "1": "CORPORATE"
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

    dict_notification_event = {
        "1": "GET_PASSWORD",
        "2": "SUCCESSFUL_SUBSCRIPTION",
        "3": "UNSUCCESSFUL_SUBSCRIPTION",
        "4": "SUCCESSFUL_CONTENT_PURCHASE",
        "5": "UNSUCCESSFUL_CONTENT_PURCHASE",
        "6": "SUCCESSFUL_UNSUBSCRIPTION",
        "7": "UNSUCCESSFUL_UNSUBSCRIPTION",
        "8": "GIFT_SENT",
        "9": "GIFT_RECEIVED",
        "10": "SENT_GIFT_ACCEPTED",
        "11": "RECEIVED_GIFT_ACCEPTED",
        "12": "SENT_GIFT_REJECTED",
        "13": "RECEIVED_GIFT_REJECTED",
        "14": "GIFT_REQUEST_SENT",
        "15": "GIFT_REQUEST_RECEIVED",
        "16": "SENT_GIFT_REQUEST_ACCEPTED",
        "17": "RECEIVED_GIFT_REQUEST_ACCEPTED",
        "18": "SENT_GIFT_REQUEST_REJECTED",
        "19": "RECEIVED_GIFT_REQUEST_REJECTED",
        "20": "SUCCESSFUL_SUBSCRIPTION_RENEWAL",
        "21": "UNSUCCESSFUL_SUBSCRIPTION_RENEWAL",
        "22": "SUCCESSFUL_CONTENT_COPY",
        "23": "UNSUCCESSFUL_CONTENT_COPY",
        "24": "SUCCESSFUL_DIY_CONTENT_MODERATION",
        "25": "UNSUCCESSFUL_DIY_CONTENT_MODERATION",
        "26": "SUCCESSFUL_TRIAL_SUBSCRIPTION",
        "27": "UNSUCCESSFUL_TRIAL_SUBSCRIPTION",
        "28": "SUCCESSFUL_TRIAL_UNSUBSCRIPTION",
        "29": "UNSUCCESSFUL_TRIAL_UNSUBSCRIPTION",
        "30": "TRIAL_OPT_IN_SUBSCRIPTION_EXPIRING",
        "31": "TRIAL_OPT_OUT_SUBSCRIPTION_EXPIRING"
    }

    dict_db_parameters = {
        'content_id': 'Content identifier.',
        'external_id': 'External service identifier.',
        'hlr_id': 'HLR node identifier.',
        'is_default': 'Flag to set as a default value.\nDefault: false.',
        'is_hidden': 'Flag not to display the content.\nDefault: false.',
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
        'channel': 'Media channel name.',
        'is_hlr_required': 'Flag to make the parameter hlr_id mandatory.\nDefault: false.',
        'increment': 'Step size.',
        'is_copied': 'Flag to indicate if the content has been copied from the other subscriber.',
        'order_code': 'Code to purchase the content.',
        'moderator_id': 'Moderator identifier.',
        'moderation_time': 'Moderation completion date and time.',
        'creation_time': '{} creation date and time.\nDefault: current_timestamp()',
        'creator_id': '{} creator identifier.',
        'name': '{} name.',
        'update_time': '{} update date and time.',
        'updater_id': 'Identifier of the user to modify the {}.'
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
        "rule_type": dict_rule_type,
        "dict_db_parameters": dict_db_parameters,
        "dict_default_text": dict_default_text,
        "dict_notification_event": dict_notification_event
    }

    list_types = [
        "bigint(M)", "bit(M)", "blob", "datetime(M)", "int(M)", "json", "text", "timestamp", "varchar(M)",
        "smallint(M)", "longtext", "tinyint(M)"]

    list_state = ["SUSPENDED", "INACTIVE", "PRE_ACTIVE", "ACTIVE", "GRACE", "PENDING"]

    list_partner_type = ["CONTENT_PROVIDER", "SERVICE_PROVIDER", "BOTH"]

    list_channels = ["IVR", "SMS", "WEB", "USSD", "API", "OKP", "SERVICE", "RETAIL", "SYSTEM"]

    list_webhook_types = ["RBT_SUBSCRIPTION", "RBT_CONTENT", "SUBSCRIPTION"]

    list_business_divisions = ["VAS_OPERATION", "DIGITAL_OPERATION", "B2B_OPERATION", "OTHERS"]

    list_dpdp_core_questions = (
        ("remove", "RepoMetadata.remove"),
        ("url", "SenderMessage.url"),
        ("node_name", "TaskQueue.node_name"),
        ("remote_task_id", "TaskQueue.remote_task_id"),
        ("owner", "TaskQueue.owner"),
        ("purchase_id", "price_category.purchase_id"),
        ("is_file_present", "content.is_file_present"),
        ("type", "notification_webhook.type"),
        ("cycle_option", "seq_content_order_code.cycle_option"),
        ("cycle_count", "seq_content_order_code.cycle_count"),
        ("days_to_reminder", "reminder_policy.days_to_reminder"),
        ("type", "renewal_task.type"),
        ("debt_only", "renewal_task.debt_only"),
        ("charging_metadata", "subscription.charging_metadata"),
        ("renewal_cycle_state", "subscription.renewal_cycle_state"),
        ("next_debt_charging_date", "subscription.next_debt_charging_date"),
        ("artist_id", "raw_custom_tone.artist_id")
    )

    list_rbt_web_questions = (
        ("rbt type", "subscriber.type"),
        ("unknown_rule", "rule.order"),
        ("id", "subscriber_content.id")
    )

    list_questions: list[tuple[str, str]] = [
        ("DPDP.Core", list_dpdp_core_questions),
        ("RBT Web", list_rbt_web_questions)
    ]

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
        pprint(cls.dict_common_params)
        print("dict:")
        pprint(cls.dict_rbt_dpdp)
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
            print('There is no such type. "NEW", "MODIFIED", "CHECK", "ADD".')

    @classmethod
    def print_default_text(cls):
        pprint(cls.dict_default_text)


def divide_item(item: str, name_from_list: str) -> tuple[str, list[str]]:
    list_items: list[str] = item.split('\n')

    if not list_items[1].strip().startswith(('|', '+')):
        name = list_items[1].strip()
        num_start = 2
    else:
        name = name_from_list
        num_start = 1

    return name, list_items[num_start:]


def modify_types(list_types: list[str]) -> list[str]:
    list_modified_types: list[str] = []
    pattern = re.compile(r"(.*)\(\d+\)(.*)")

    for new_type in list_types:
        match = re.match(pattern, new_type)
        if match:
            list_modified_types.append(f"{match.group(0)}(M){match.group(1)}")
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


def line_join(lines: list[str]):
    pattern = r'\\t'
    items = [re.escape(pattern).join((str(line),)) for line in lines]
    return ''.join(items)


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


def full_parse_db(list_parse: list[str], list_names: list[str]):
    for index, item in enumerate(list_parse):
        name, list_items = divide_item(item, list_names[index])
        print('----------')
        print(f"{name}")
        parse_db_rows_item(list_items)
        print('----------')


def get_unique_values(list_values: list):
    return list(set(list_values))


def convert_list_to_json(attr_name: str, list_items: list[str]):
    text = json.dumps(list_items, indent=2)
    name = f"\"{attr_name}\""
    return f"{name}: {text}"


def convert_dict_to_json(attr_name: str, dict_items: dict):
    text = json.dumps(dict_items, indent=2)
    text.replace("'", '"')
    name = f"\"{attr_name}\""
    return f"{name}: {text}"


def convert_to_json(name: str, obj):
    string = " = ".join((f"{name}", f"{obj}"))
    return json.dumps(string, indent=2, sort_keys=True, ensure_ascii=False)[1:-1]


def convert_all_to_json():
    return [convert_to_json(param, DpdpRbt.__getattribute__(DpdpRbt, param)) for param in dir(DpdpRbt)
            if param.startswith(("dict", "list"))]


def check_path(path: Union[str, pathlib.Path]):
    path_file = pathlib.Path(path).resolve()
    existence: bool = True if path_file.exists() else False
    file: bool = True if path_file.is_file() else False
    extension: bool = True if path_file.suffix == '.json' else False

    return existence, file, extension


def write_json_file(text: list[str], path: Union[str, pathlib.Path]):
    with open(path, "w+") as f:
        for line in text:
            f.write(f"{line}\n")


class RbtAPI:
    get_common_text = [
        "Content thumbnail image with the sizes of 50 px. Type: binary. Format: image, jpeg, or base64."
    ]

    get_full_list = (
        "Album", "Album_ref", "App", "Artist", "Artist_ref", "Category", "Content", "Content_group",
        "Content_group_changes", "Content_group_data", "Content_group_identity", "Content_identity", "Content_ref",
        "Default_rule", "Default_rule_data", "Gallery", "Member", "Member_ref", "Playlist", "Price", "Rbt_addon",
        "Rbt_package", "Rbt_package_ref", "Ref", "Rule", "Rule_data", "Rule_full", "Schedule", "Schedule_data",
        "Schedule_range", "Search_result", "Search_result_item", "Session_app", "Subscriber",
        "Subscriber_caller_group_data", "Subscriber_custom_content", "Subscriber_data", "Subscriber_ref", "Tone"
    )

    addon: tuple[str] = (
        '{', '  "id": 0,', '  "name": "addonName",', '  "price": 0,', '  "orderCode": 0,', '  "purchasedCount": 0,',
        '  "discountCount": 0,', '  "discountTime": 0,', '  "discountMultiplier": 0,', '  "discountCoefficient": 0,',
        '  "from": 0,', '  "till": 0,', '  "repeat": true,', '  "forNewSubscribers": true,', '  "period": 0,',
        '  "active": true', '}',
    )

    album: tuple[str] = (
        '{', '  "id": 0,', '  "name": "albumName",', '  "artist": {', '    "id": 0,', '    "name": "artistName"',
        '  },', '  "releaseYear": 0,', '  "categories": [', '    {', '      "id": 0,', '      "name": "categoryName"',
        '    }', '  ]', '}',
    )

    artist: tuple[str] = (
        '{', '  "id": 0,', '  "name": "artistName",', '  "thumbnail": "data:image/jpeg;base64"', '}',
    )

    artist_ref: tuple[str] = (
        '{', '  "id": 0,', '  "name": "artistName"', '}'
    )

    category: tuple[str] = (
        '{', '  "id": 0,', '  "name": "categoryName"', '}'
    )

    playlist: tuple[str] = (
        '{', '  "id": 0,', '  "name": "playlistName",', '  "categories": [', '    {', '      "id": 0,',
        '      "name": "categoryName"', '    }', '  ],', '  "thumbnail": "image",', '  "alreadyPurchased": true,',
        '  "canBeGifted": true,', '  "orderCode": 0,', '  "price": 0', '}'
    )

    rbt_package: tuple[str] = (
        '{', '  "id": 0,', '  "name": "rbtPackageName",', '  "price": 0,', '  "daysPeriod": 0,', '  "antiRbt": true,',
        '  "channel": "IVR",', '  "isTrial": true', '}'
    )

    rbt_package_ref: tuple[str] = (
        '{', '  \"id\": 0,', '  \"name\": \"rbtPackageName\"', '}'
    )

    tone: tuple[str] = (
        '{', '  "id": 0,', '  "title": "toneName",', '  "artist": {', '    "id": 0,', '    "name": "artistName"',
        '  },', '  "album": {', '    "id": 0,', '    "name": "albumName",', '    "releaseYear": 0', '  },',
        '  "categories": [', '    {', '      "id": 0,', '      "name": "categoryName"', '    }', '  ],',
        '  "thumbnail": "image",', '  "alreadyPurchased": true,', '  "canBeGifted": true,', '  "orderCode": 0,',
        '  "price": 0', '}'
    )

    schedule_data: tuple[str] = (
        '{', '  "name": "scheduleName",', '  "from": 0,', '  "till": 0,', '  "ranges": [', '    {',
        '      "from": "10:00",', '      "till": "10:00",', '      "weekDays": [', '        ["MO", "SU"]', '      ],',
        '      "monthDays": [', '        [1, 2, 3]', '      ],', '      "yearDays": [', '        ["10.01", "20.02"]',
        '      ]', '    }', '  ]', '}'
    )

    subscriber_custom_content: tuple[str] = (
        '{', '  "id": 0,', '  "title": "contentName",', '  "isWaitModeration": true', '}'
    )

    subscriber_ref: tuple[str] = (
        '{', '  "subscriber": {', '    "id": 0,', '    "name": "subscriberName",', '    "isHidden": true', '  }', '}'
    )

    subscriber_data: tuple[str] = (
        '{', '  \"isRbtOverlay\": true,', '  \"isAntiRbtOverlay\": true,', '  \"isPrivate\": true', '}'
    )

    schedule: tuple[str] = (
        '{', '  "id": 0,', '  "name": "scheduleName",', '  "from": 0,', '  "till": 0,', '  "ranges": [', '    {',
        '      "from": "10:00",', '      "till": "10:00",', '      "weekDays": [', '        ["MO", "SU"]', '      ],',
        '      "monthDays": [', '        [1, 2, 3]', '      ],', '      "yearDays": [', '        ["10.01", "20.02"]',
        '      ]', '    }', '  ]', '}'
    )

    member: tuple[str] = (
        '{', '  "msisdn": 0,', '  "name": "memberName",', '  "isPublic": true', '}'
    )

    member_ref: tuple[str] = (
        '{', '  "msisdn": 0,', '  "name": "memberName"', '}'
    )

    group: tuple[str] = (
        '{', '  "name": "groupName",', '  "members": [ 0 ]', '}'
    )

    group_ref: tuple[str] = (
        '{', '  "id": 0,', '  "name": "groupName"', '}'
    )

    default_rule_data: tuple[str] = (
        '{', '  "mode": "RANDOM",', '  "contentsIds": [ 0 ]', '}'
    )

    default_rule: tuple[str] = (
        '{', '  "mode": "RANDOM",', '  "contents": [', '    {', '      "id": 0,', '      "name": "toneName",',
        '      "type": "TONE",', '      "thumbnail": "data:image/jpeg;base64",', '      "orderCode": 0', '    }', '  ]',
        '}'
    )

    rule_data: tuple[str] = (
        '{', '  \"name\": \"string\",', '  \"kind\": \"SCHEDULE\",', '  \"type\": \"GENERAL\",', '  \"order\": 0,',
        '  \"mode\": \"RANDOM\",', '  \"members\": [ 0 ],', '  \"groupsIds\": [ 0 ],', '  \"schedulesIds\": [ 0 ],',
        '  \"contentIds\": [ 0 ]', '}',

    )

    subscriber_caller_group: tuple[str] = (
        '{', '  \"name\": \"groupName\",', '  \"members\": [ 0 ]', '}'
    )

    subscriber_caller_group_ref: tuple[str] = (
        '{', '  \"id\": 0,', '  \"name\": \"groupName\"', '}'
    )

    schedule_range: tuple[str] = (
        '{', '  \"from\": \"10:00\",', '  \"till\": \"10:00\",', '  \"weekDays\": [', '    [\"MO\", \"SU\"]', '  ],',
        '  \"monthDays\": [', '    [1, 2, 3]', '  ],', '  \"yearDays\": [', '    [\"10.01\", \"20.02\"]', '  ]', '}'

    )

    search_result: tuple[str] = (
        '{', '  \"artists\": [', '    {', '      \"id\": 0,', '      \"name\": \"artistName\",',
        '      \"ownerName\": \"ownerName\",', '      \"orderCode\": 0,',
        '      \"thumbnail\": \"data:image/jpeg;base64\"', '    }', '  ],', '  \"playlists\": [', '    {',
        '      \"id\": 0,', '      \"name\": \"playlistName\",', '      \"ownerName\": \"ownerName\",',
        '      \"orderCode\": 0,', '      \"thumbnail\": \"data:image/jpeg;base64\"', '    }', '  ],',
        '  \"albums\": [', '    {', '      \"id\": 0,', '      \"name\": \"albumName\",',
        '      \"ownerName\": \"ownerName\",', '      \"orderCode\": 0,',
        '      \"thumbnail\": \"data:image/jpeg;base64\"', '    }', '  ],', '  \"tones\": [', '    {',
        '      \"id\": 0,', '      \"name\": \"toneName\",', '      \"ownerName\": \"ownerName\",',
        '      \"orderCode\": 0,', '      \"thumbnail\": \"data:image/jpeg;base64\"', '    }', '  ],',
        '  \"categories\": [', '    {', '      \"id\": 0,', '      \"name\": \"categoryName\",',
        '      \"ownerName\": \"ownerName\",', '      \"orderCode\": 0,',
        '      \"thumbnail\": \"data:image/jpeg;base64\"', '    }', '  ],', '  \"subscriber\": {', '    \"id\": 0,',
        '    \"name\": \"subscriberName\",', '    \"isHidden\": true', '  }', '}',

    )

    search_result_item: tuple[str] = (
        '{', '  \"id\": 0,', '  \"name\": \"itemName\",', '  \"ownerName\": \"ownerName\",', '  \"orderCode\": 0,',
        '  \"thumbnail\": \"data:image/jpeg;base64\"', '}'
    )

    rule_full: tuple[str] = (
        '{', '  "id": 0,', '  "order": 0,', '  "type": "GENERAL",', '  "mode": "RANDOM",', '  "name": "ruleName",',
        '  "members": [', '    {', '      "msisdn": 0,', '      "name": "memberName"', '    }', '  ],', '  "groups": [',
        '    {', '      "id": 0,', '      "name": "groupName"', '    }', '  ],', '  "schedules": [', '    {',
        '      "id": 0,', '      "name": "scheduleName"', '    }', '  ],', '  "contents": [', '    {', '      "id": 0,',
        '      "name": "contentName",', '      "type": "TONE",', '      "thumbnail": "data:image/jpeg;base64",',
        '      "orderCode": 0', '    }', '  ]', '}'
    )

    schedule_ref: tuple[str] = (
        '{', '  "id": 0,', '  "name": "scheduleName"', '}'
    )

    content: tuple[str] = (
        '{', '  "id": 0,', '  "orderCode": 0', '}'
    )

    content_ref: tuple[str] = (
        '{', '  "id": 0,', '  "name": "contentName",', '  "type": "TONE",', '  "thumbnail": "data:image/jpeg;base64",',
        '  "orderCode": 0', '}'
    )

    rule: tuple[str] = (
        '{', '  "id": 0,', '  "order": 0,', '  "kind": "SCHEDULE",', '  "type": "GENERAL",', '  "mode": "RANDOM",',
        '  "name": "ruleName",', '  "groupsIds": [ 0 ],', '  "schedulesIds": [ 0 ],', '  "contents": [', '    {',
        '      "id": 0,', '      "orderCode": 0', '    }', '  ]', '}'
    )

    rule_ref: tuple[str] = (
        '{', '  "name": "ruleDataName",', '  "kind": "SCHEDULE",', '  "type": "GENERAL",', '  "order": 0,',
        '  "mode": "RANDOM",', '  "members": [ 0 ],', '  "groupsIds": [ 0 ],', '  "schedulesIds": [ 0 ],',
        '  "contentIds": [ 0 ]', '}'
    )

    gallery: tuple[str] = (
        '{', '  "artists": [', '    {', '      "id": 0,', '      "name": "string",', '      "ownerName": "string",',
        '      "orderCode": 0,', '      "thumbnail": "data:image/jpeg;base64"', '    }', '  ],', '  "playlists": [',
        '    {', '      "id": 0,', '      "name": "string",', '      "ownerName": "string",', '      "orderCode": 0,',
        '      "thumbnail": "data:image/jpeg;base64"', '    }', '  ],', '  "albums": [', '    {', '      "id": 0,',
        '      "name": "string",', '      "ownerName": "string",', '      "orderCode": 0,',
        '      "thumbnail": "data:image/jpeg;base64"', '    }', '  ],', '  "tones": [', '    {', '      "id": 0,',
        '      "name": "string",', '      "ownerName": "string",', '      "orderCode": 0,',
        '      "thumbnail": "data:image/jpeg;base64"', '    }', '  ],', '  "categories": [', '    {',
        '      "id": 0,', '      "name": "string",', '      "ownerName": "string",', '      "orderCode": 0,',
        '      "thumbnail": "data:image/jpeg;base64"', '    }', '  ],', '  "subscriber": {', '    "id": 0,',
        '    "name": "string",', '    "isHidden": true', '  }', '}'
    )

    @classmethod
    def convert_all_to_word(cls):
        return "\n".join(cls.convert_attr_to_word(attr) for attr in cls.get_all_attrs())

    @classmethod
    def convert_attr_to_word(cls, attr: str) -> Optional[str]:
        if attr in cls.get_all_attrs():
            value: tuple[str] = getattr(RbtAPI, attr)
            new_value: str = "\n".join(convert_to_word(line) for line in value)
            return f"{attr}\n{new_value}"
        else:
            return f"{attr}\nINCORRECT_ATTRIBUTE\n"

    @classmethod
    def get_all_attrs(cls) -> list[str]:
        return [attr for attr in dir(RbtAPI) if not attr.startswith(("_", "get", "convert"))]


def write_to_file(file_name: str, text):
    """
    Writes the information to the file.\n
    :param file_name: full file name
    :param text:
    :return:
    """
    if check_path_file(file_name):
        with open(file_name, "w+", encoding="ascii") as file:
            file.write(text)


def check_path_file(path: Union[str, pathlib.Path]) -> bool:
    """
    Checks the path to the file.\n
    :param path: path to the file, str or Path
    :return: the path validity of the bool type.
    """
    flag = False
    try:
        with open(pathlib.Path(path).resolve(strict=True), "w+") as file:
            file.close()
    except FileNotFoundError as e:
        print(f"FileNotFoundError {e.strerror}. The file is created.")
        with open(pathlib.Path(path).resolve(), "x") as file:
            file.close()
        flag = True
    except AttributeError:
        print(f"AttributeError. Incorrect parameter input.")
    except ValueError:
        print(f"ValueError. Incorrect path input.")
    except IsADirectoryError as e:
        print(f"IsADirectoryError {e.strerror}. Path leads to not a file.")
    except PermissionError as e:
        print(f"PermissionError {e.strerror}. Not enough access rights.")
    except OSError as e:
        print(f"OSError {errno}, {e.strerror}.")
    else:
        flag = True
    finally:
        return flag


def check_file_extension(path: Union[str, pathlib.Path], file_ext: str):
    if check_path_file(path):
        suffix = "".join((".", file_ext)) if not file_ext.startswith(".") else file_ext
        if pathlib.Path(path).resolve().suffix == suffix:
            return True
        else:
            print(f"File has an incorrect extension, {pathlib.Path(path).resolve().suffix}, instead of {suffix}.")
            return False
    else:
        return check_path_file(path)


def convert_to_word(line: str):
    return line.replace(r'"', r'\"')


def get_json(text: str):
    return json.loads(json.dumps(text, indent=2))


def main():
    # print(__doc__)
    # print(DpdpRbt.__doc__)
    # attrs = [attr for attr in dir(DpdpRbt) if attr.startswith(("dict", "list"))]
    # pprint(attrs)
    # pprint(convert_all_to_json())
    # DpdpRbt.get_dict_value()
    # DpdpRbt.print_default_text()
    # text = convert_all_to_json()
    # print(text)

    # print(convert_list_to_json("list_state", DpdpRbt.list_state))
    # print(convert_dict_to_json("dict_rbt_dpdp", DpdpRbt.dict_rbt_dpdp))
    # res = []
    # for attr in attrs:
    #     if isinstance(DpdpRbt.__getattribute__(DpdpRbt, attr), list):
    #         res.append(convert_list_to_json(attr, DpdpRbt.__getattribute__(DpdpRbt, attr)))
    #     elif isinstance(DpdpRbt.__getattribute__(DpdpRbt, attr), dict):
    #         res.append(convert_dict_to_json(attr, DpdpRbt.__getattribute__(DpdpRbt, attr)))
    #     else:
    #         continue
    #
    # path = "./db_params.json"
    # write_json_file(res, path)

    # res = get_json(convert_to_word(RbtAPI.artist))
    # print(res)
    #
    # res_json = json.dumps(RbtAPI.artist, indent=2)
    #
    # with open("test.json", "w+") as f:
    #     f.write(res_json)
    # attrs = [attr for attr in dir(RbtAPI) if not attr.startswith("_")]
    # pprint(attrs)
    # print(len(attrs))
    write_to_file("API entities.txt", RbtAPI.convert_all_to_word())
    # print(OSError.errno)


if __name__ == "__main__":
    main()
