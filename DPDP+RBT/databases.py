from pprint import pprint
import re
from typing import Optional

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
    "list_provider_type",
    "list_questions",
    "list_rbt_web_questions",
    "list_state",
    "list_types",
    "login",
    "password",
    "web_port"
    """
    ip_server = "192.168.125.148"
    web_port = 8081
    login = "root"
    password = "elephant"
    command = "mysql -uroot -p"
    db_password = "elephant"

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
        'order_code': 'Code to purchase the content.'
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

    list_provider_type = ["CONTENT_PROVIDER", "SERVICE_PROVIDER", "BOTH"]

    list_channels = ["IVR", "SMS", "WEB", "USSD", "API", "OKP", "SERVICE", "RETAIL", "SYSTEM"]

    list_webhook_types = ["RBT_SUBSCRIPTION", "RBT_CONTENT", "SUBSCRIPTION"]

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
        ("next_debt_charging_date", "subscription.next_debt_charging_date")
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


def main():
    # print(__doc__)
    # print(DpdpRbt.__doc__)

    DpdpRbt.get_dict_value()
    DpdpRbt.print_default_text()
    # DpdpRbt.print_questions()
    # DpdpRbt.print_out()
    # list_values = [
    #     "bigint(M)", "bigint(M)", "varchar(M)", "varchar(M)", "bigint(M)", "varchar(M)", "varchar(M)", "datetime",
    #     "varchar(M)", "varchar(M)", "bit(M)", "bit(M)", "text", "bigint(M)", "varchar(M)", "text", "bigint(M)",
    #     "varchar(M)", "text", "varchar(M)", "varchar(M)", "text", "int(M)", "bit(M)", "datetime", "bit(M)", "datetime",
    #     "varchar(M)", "varchar(M)", "varchar(M)", "varchar(M)", "datetime", "bigint(M)", "int(M)", "varchar(M)",
    #     "bigint(M)", "int(M)", "varchar(M)", "bigint(M)", "bigint(M) U", "bigint(M) U", "bigint(M) U", "varchar(M)",
    #     "bit(M)", "smallint(M) U", "longtext", "bigint(M) U", "bigint(M) U", "bigint(M) U", "datetime(M)", "varchar(M)",
    #     "varchar(M)", "bit(M)", "datetime(M)", "bigint(M) U", "bigint(M) U", "bigint(M) U", "datetime(M)",
    #     "bigint(M) U", "bigint(M) U", "bigint(M) U", "datetime(M)", "bigint(M)", "varchar(M)", "bit(M)", "varchar(M)",
    #     "bigint(M) U", "bigint(M) U", "bigint(M) U", "bigint(M) U", "bigint(M) U", "varchar(M)", "bit(M)",
    #     "datetime(M)", "bigint(M) U", "varchar(M)", "bit(M)", "bigint(M) U", "bigint(M) U", "bigint(M) U", "varchar(M)",
    #     "text", "bigint(M) U", "varchar(M)", "varchar(M)", "bigint(M) U", "varchar(M)", "bigint(M) U", "bigint(M) U",
    #     "bigint(M) U", "varchar(M)", "bigint(M)", "bigint(M)", "bigint(M) U", "datetime(M)", "longtext", "bigint(M) U",
    #     "varchar(M)", "varchar(M)", "bigint(M) U", "bigint(M) U", "bigint(M) U", "datetime(M)", "datetime(M)",
    #     "bigint(M) U", "smallint(M) U", "bigint(M) U", "bigint(M) U", "smallint(M) U", "bigint(M) U", "bigint(M) U",
    #     "varchar(M)", "bigint(M) U", "datetime(M)", "bigint(M) U", "bit(M)", "bigint(M)", "bigint(M)", "bigint(M)",
    #     "bigint(M)", "bigint(M)", "bigint(M) U", "tinyint(M) U", "bigint(M)", "bigint(M) U", "bigint(M) U",
    #     "varchar(M)", "bit(M)", "bigint(M) U", "bit(M)", "datetime(M)", "bigint(M) U", "bigint(M) U", "bigint(M) U",
    #     "varchar(M)", "bit(M)", "bigint(M) U", "bit(M)", "datetime(M)", "bigint(M) U", "varchar(M)", "bigint(M) U",
    #     "bigint(M) U", "bigint(M) U", "varchar(M)", "varchar(M)", "datetime(M)", "bigint(M) U", "datetime(M)",
    #     "datetime(M)", "datetime(M)", "datetime(M)", "longtext", "varchar(M)", "bigint(M) U", "bigint(M) U",
    #     "bigint(M) U", "datetime(M)", "longtext", "datetime(M)", "varchar(M)", "bigint(M) U", "bigint(M) U",
    #     "bigint(M) U", "bigint(M) U", "datetime(M)", "bigint(M)", "varchar(M)", "bigint(M) U", "varchar(M)",
    #     "varchar(M)", "varchar(M)", "bit(M)", "varchar(M)", "varchar(M)", "bigint(M) U", "int(M)", "timestamp",
    #     "int(M)", "varchar(M)", "int(M)", "bigint(M)", "int(M)", "int(M)", "longtext", "int(M)", "int(M)", "int(M)",
    #     "varchar(M)", "int(M)", "int(M)", "int(M)", "int(M)", "int(M)", "varchar(M)", "bigint(M)", "int(M)", "int(M)",
    #     "varchar(M)", "varchar(M)", "bigint(M)", "bigint(M)", "int(M)", "varchar(M)", "int(M)", "int(M)", "int(M)",
    #     "int(M)", "int(M)", "int(M)", "int(M)", "int(M)", "int(M)", "int(M)", "int(M)", "int(M)", "int(M)",
    #     "varchar(M)", "timestamp", "timestamp", "varchar(M)", "int(M)", "int(M)", "int(M)", "int(M)", "varchar(M)",
    #     "bit(M)", "timestamp", "timestamp", "int(M)", "bit(M)", "int(M)", "int(M)", "timestamp", "timestamp", "bit(M)",
    #     "int(M)", "int(M)", "bigint(M)", "int(M)", "bit(M)", "int(M)", "int(M)", "varchar(M)", "int(M)", "int(M)"
    # ]
    # unique_values = get_unique_values(list_values)
    # unique_values.sort()
    # pprint(unique_values)
    print('"')


if __name__ == "__main__":
    main()
