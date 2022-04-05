from pprint import pprint
import sys
import re

def parse_db_info():
    dict_indexes = {0: "Parameter", 1: "Type", 2: "NULL", 3: "Key", 4: "Default", 5: "Extra"}
    print("Lines to parse:")
    # lines = sys.stdin.read().splitlines()
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
        # parameter, par_type, null, key, extra
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
        # print(f"{dict_indexes[idx]}")
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
            # line_mod = line_updated.replace(r"\s{}|", "\t")
            final_lines.append(line_mod)

    for final_line in final_lines:
        print(final_line)
        # print(final_line[1:-1])


def parse_db_rows_item(item):
    final_lines: list[str] = []
    for line in item:
        if line.startswith("+"):
            continue
        else:
            line_updated = line[1:-1]
            pattern = re.compile(r'\s*\|\s*')
            line_mod = re.sub(pattern=pattern, repl="\t", string=line_updated)
            # line_mod = line_updated.replace(r"\s{}|", "\t")
            final_lines.append(line_mod.lstrip())

    final_lines[0].rstrip()

    pattern_final = re.compile(r"Field\tType\tNull\tKey\tDefault\tExtra")
    pattern_null = re.compile(r"NULL\t")
    pattern_auto_increment = re.compile(r"auto_increment ")

    for final_line in final_lines:
        line_null = re.sub(pattern=pattern_null, repl="", string=final_line)
        line_res = re.sub(pattern=pattern_auto_increment, repl="Auto_increment.", string=line_null)

        if line_res and not re.match(pattern_final, line_res):
            print(line_res)
    print(len(final_lines))


class DPDP_RBT:
    ip_server = "192.168.125.148"
    web_port = 8081
    login = "root"
    password = "elephant"
    command = "mysql -uroot -p"
    db_password = "elephant"

    dict_rbt_dpdp: dict[str, dict] = {}

    list_questions: list[tuple[str, str]] = []

    @classmethod
    def print_out(cls):
        print(f"ip server = {cls.ip_server}")
        print(f"web interface port = {cls.web_port}")
        print(f"command = {cls.command}")
        print(f"login = {cls.login}")
        print(f"password = {cls.password}")
        print(f"db_password = {cls.db_password}")
        print(f"dict:")
        pprint(cls.dict_rbt_dpdp)

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


class RBT_Web(DPDP_RBT):
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


class DPDP_Core(DPDP_RBT):
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

    list_state = ["SUSPENDED", "INACTIVE", "PRE_ACTIVE", "ACTIVE", "GRACE", "PENDING"]

    list_provider_type = ["CONTENT_PROVIDER", "SERVICE_PROVIDER", "BOTH"]

    list_questions = [
        ("remove", "RepoMetadata.remove"), ("url", "SenderMessage.url"), ("node_name", "TaskQueue.node_name"),
        ("remote_task_id", "TaskQueue.remote_task_id"), ("owner", "TaskQueue.owner"), ("purchase_id",
                                                                                       "price_category.purchase_id")]


def divide_item(item: str):
    list_items: list[str] = item.split('\n')
    if not list_items[1].startswith(('|', '+')):
        name = list_items[1].strip()
        return name, list_items[2:]
    else:
        name = "default"
        return name, list_items[1:]


def main():
    # parse_db_info()
#     list_parse = [
#         """
#         TaskQueue
# +-----------------+--------------+------+-----+---------+----------------+
# | Field           | Type         | Null | Key | Default | Extra          |
# +-----------------+--------------+------+-----+---------+----------------+
# | id              | bigint(20)   | NO   | PRI | NULL    | auto_increment |
# | action          | int(11)      | NO   |     | NULL    |                |
# | node_name       | varchar(128) | NO   |     | NULL    |                |
# | content_id      | bigint(20)   | NO   | MUL | NULL    |                |
# | remote_task_id  | int(11)      | YES  |     | NULL    |                |
# | owner           | varchar(256) | NO   |     | NULL    |                |
# | content_version | bigint(20)   | NO   |     | NULL    |                |
# +-----------------+--------------+------+-----+---------+----------------+
#         """,
#         """
#         content
# +-------------------+----------------------+------+-----+---------------------------------------------------+----------------+
# | Field             | Type                 | Null | Key | Default                                           | Extra          |
# +-------------------+----------------------+------+-----+---------------------------------------------------+----------------+
# | id                | bigint(20) unsigned  | NO   | PRI | NULL                                              | auto_increment |
# | external_id       | bigint(20) unsigned  | YES  | UNI | NULL                                              |                |
# | order_code        | bigint(20) unsigned  | NO   | UNI | nextval(`dpdp_core_fix`.`seq_content_order_code`) |                |
# | name              | varchar(255)         | NO   |     | NULL                                              |                |
# | is_hidden         | bit(1)               | NO   |     | b'0'                                              |                |
# | duration_days     | smallint(5) unsigned | YES  |     | NULL                                              |                |
# | metadata          | longtext             | YES  |     | NULL                                              |                |
# | product_id        | bigint(20) unsigned  | NO   | MUL | NULL                                              |                |
# | provider_id       | bigint(20) unsigned  | YES  | MUL | NULL                                              |                |
# | price_category_id | bigint(20) unsigned  | YES  | MUL | NULL                                              |                |
# | created_date      | datetime(3)          | YES  |     | NULL                                              |                |
# | status            | varchar(15)          | NO   |     | ACTIVE                                            |                |
# | type              | varchar(24)          | NO   |     | TONE                                              |                |
# | is_file_present   | bit(1)               | YES  |     | b'0'                                              |                |
# | expiration_date   | datetime(3)          | YES  |     | NULL                                              |                |
# +-------------------+----------------------+------+-----+---------------------------------------------------+----------------+
#         """,
#         """
#         content_ownership
# +---------------+---------------------+------+-----+---------+----------------+
# | Field         | Type                | Null | Key | Default | Extra          |
# +---------------+---------------------+------+-----+---------+----------------+
# | id            | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
# | content_id    | bigint(20) unsigned | NO   | MUL | NULL    |                |
# | subscriber_id | bigint(20) unsigned | NO   | MUL | NULL    |                |
# | created_date  | datetime(3)         | NO   |     | NULL    |                |
# +---------------+---------------------+------+-----+---------+----------------+
#         """,
#         """
#         content_purchase
# +--------------------+---------------------+------+-----+---------+----------------+
# | Field              | Type                | Null | Key | Default | Extra          |
# +--------------------+---------------------+------+-----+---------+----------------+
# | id                 | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
# | subscriber_id      | bigint(20) unsigned | NO   |     | NULL    |                |
# | content_id         | bigint(20) unsigned | NO   |     | NULL    |                |
# | date               | datetime(3)         | YES  |     | NULL    |                |
# | price              | bigint(20)          | NO   |     | NULL    |                |
# | channel            | varchar(32)         | NO   |     | NULL    |                |
# | is_copied          | bit(1)              | NO   |     | b'0'    |                |
# | refund_information | varchar(128)        | YES  |     | NULL    |                |
# +--------------------+---------------------+------+-----+---------+----------------+
#         """,
#         """
#         gift
# +---------------------+---------------------+------+-----+----------------------+----------------+
# | Field               | Type                | Null | Key | Default              | Extra          |
# +---------------------+---------------------+------+-----+----------------------+----------------+
# | id                  | bigint(20) unsigned | NO   | PRI | NULL                 | auto_increment |
# | content_purchase_id | bigint(20) unsigned | YES  | MUL | NULL                 |                |
# | content_id          | bigint(20) unsigned | NO   | MUL | NULL                 |                |
# | from_subscriber_id  | bigint(20) unsigned | NO   | MUL | NULL                 |                |
# | to_subscriber_id    | bigint(20) unsigned | NO   | MUL | NULL                 |                |
# | status              | varchar(24)         | NO   |     | PENDING              |                |
# | is_requested        | bit(1)              | YES  |     | b'0'                 |                |
# | created_date        | datetime(3)         | NO   |     | current_timestamp(3) |                |
# +---------------------+---------------------+------+-----+----------------------+----------------+
#         """,
#         """
#         notification_event
# +---------------+---------------------+------+-----+---------+----------------+
# | Field         | Type                | Null | Key | Default | Extra          |
# +---------------+---------------------+------+-----+---------+----------------+
# | id            | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
# | name          | varchar(255)        | NO   |     | NULL    |                |
# | is_predefined | bit(1)              | NO   |     | b'0'    |                |
# +---------------+---------------------+------+-----+---------+----------------+
#         """,
#         """
#         notification_template
# +------------+---------------------+------+-----+---------+----------------+
# | Field      | Type                | Null | Key | Default | Extra          |
# +------------+---------------------+------+-----+---------+----------------+
# | id         | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
# | event_id   | bigint(20) unsigned | NO   | MUL | NULL    |                |
# | service_id | bigint(20) unsigned | YES  | MUL | NULL    |                |
# | language   | varchar(10)         | NO   |     | NULL    |                |
# | text       | text                | YES  |     | NULL    |                |
# +------------+---------------------+------+-----+---------+----------------+
#         """,
#         """
#         notification_webhook
# +---------------+---------------------+------+-----+--------------+----------------+
# | Field         | Type                | Null | Key | Default      | Extra          |
# +---------------+---------------------+------+-----+--------------+----------------+
# | id            | bigint(20) unsigned | NO   | PRI | NULL         | auto_increment |
# | endpoint_url  | varchar(255)        | NO   | MUL | NULL         |                |
# | endpoint_name | varchar(255)        | YES  |     | NULL         |                |
# | product_id    | bigint(20) unsigned | NO   | MUL | NULL         |                |
# | type          | varchar(32)         | NO   |     | SUBSCRIPTION |                |
# +---------------+---------------------+------+-----+--------------+----------------+
#         """,
#         """
#         price_category
# +----------------+---------------------+------+-----+---------+----------------+
# | Field          | Type                | Null | Key | Default | Extra          |
# +----------------+---------------------+------+-----+---------+----------------+
# | id             | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
# | purchase_id    | bigint(20) unsigned | NO   |     | NULL    |                |
# | renewal_id     | bigint(20) unsigned | NO   |     | NULL    |                |
# | name           | varchar(255)        | NO   |     | NULL    |                |
# | purchase_fee   | bigint(20)          | NO   |     | NULL    |                |
# | renewal_fee    | bigint(20)          | NO   |     | NULL    |                |
# | creator_id     | bigint(20) unsigned | NO   | MUL | NULL    |                |
# | creation_date  | datetime(3)         | YES  |     | NULL    |                |
# | channel_params | longtext            | YES  |     | NULL    |                |
# +----------------+---------------------+------+-----+---------+----------------+
# """,
#         """
# product
# +-------------+---------------------+------+-----+---------+----------------+
# | Field       | Type                | Null | Key | Default | Extra          |
# +-------------+---------------------+------+-----+---------+----------------+
# | id          | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
# | external_id | varchar(255)        | YES  | UNI | NULL    |                |
# | name        | varchar(255)        | NO   | UNI | NULL    |                |
# | partner_id  | bigint(20) unsigned | YES  | MUL | NULL    |                |
# +-------------+---------------------+------+-----+---------+----------------+
# """,
#         """
# reminder
# +-----------------+---------------------+------+-----+----------------------+----------------+
# | Field           | Type                | Null | Key | Default              | Extra          |
# +-----------------+---------------------+------+-----+----------------------+----------------+
# | id              | bigint(20) unsigned | NO   | PRI | NULL                 | auto_increment |
# | subscription_id | bigint(20) unsigned | NO   | MUL | NULL                 |                |
# | sent_date       | datetime(3)         | NO   |     | current_timestamp(3) |                |
# | receipt_date    | datetime(3)         | YES  |     | NULL                 |                |
# +-----------------+---------------------+------+-----+----------------------+----------------+
# """,
#         """
# reminder_policy
# +-----------------------+----------------------+------+-----+---------+----------------+
# | Field                 | Type                 | Null | Key | Default | Extra          |
# +-----------------------+----------------------+------+-----+---------+----------------+
# | id                    | bigint(20) unsigned  | NO   | PRI | NULL    | auto_increment |
# | days_to_reminder      | smallint(5) unsigned | NO   |     | NULL    |                |
# | notification_event_id | bigint(20) unsigned  | NO   | MUL | NULL    |                |
# +-----------------------+----------------------+------+-----+---------+----------------+
# """,
#         """
# renewal_policy
# +-------------+----------------------+------+-----+---------+----------------+
# | Field       | Type                 | Null | Key | Default | Extra          |
# +-------------+----------------------+------+-----+---------+----------------+
# | id          | bigint(20) unsigned  | NO   | PRI | NULL    | auto_increment |
# | version     | smallint(5) unsigned | NO   |     | 1       |                |
# | policy_info | longtext             | NO   |     | NULL    |                |
# +-------------+----------------------+------+-----+---------+----------------+
# """,
#         """
# renewal_task
# +-----------------+---------------------+------+-----+----------------------+----------------+
# | Field           | Type                | Null | Key | Default              | Extra          |
# +-----------------+---------------------+------+-----+----------------------+----------------+
# | id              | bigint(20) unsigned | NO   | PRI | NULL                 | auto_increment |
# | type            | varchar(24)         | NO   |     | NULL                 |                |
# | subscription_id | bigint(20) unsigned | YES  | MUL | NULL                 |                |
# | created_date    | datetime(3)         | NO   |     | current_timestamp(3) |                |
# | subscriber_id   | bigint(20) unsigned | NO   | MUL | NULL                 |                |
# | debt_only       | bit(1)              | YES  |     | b'0'                 |                |
# +-----------------+---------------------+------+-----+----------------------+----------------+
# """,
#         """
# seq_content_order_code
# +-----------------------+---------------------+------+-----+---------+-------+
# | Field                 | Type                | Null | Key | Default | Extra |
# +-----------------------+---------------------+------+-----+---------+-------+
# | next_not_cached_value | bigint(21)          | NO   |     | NULL    |       |
# | minimum_value         | bigint(21)          | NO   |     | NULL    |       |
# | maximum_value         | bigint(21)          | NO   |     | NULL    |       |
# | start_value           | bigint(21)          | NO   |     | NULL    |       |
# | increment             | bigint(21)          | NO   |     | NULL    |       |
# | cache_size            | bigint(21) unsigned | NO   |     | NULL    |       |
# | cycle_option          | tinyint(1) unsigned | NO   |     | NULL    |       |
# | cycle_count           | bigint(21)          | NO   |     | NULL    |       |
# +-----------------------+---------------------+------+-----+---------+-------+
# """,
#         """
# service
# +-----------------+---------------------+------+-----+---------+----------------+
# | Field           | Type                | Null | Key | Default | Extra          |
# +-----------------+---------------------+------+-----+---------+----------------+
# | id              | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
# | product_id      | bigint(20) unsigned | NO   | MUL | NULL    |                |
# | name            | varchar(255)        | NO   | UNI | NULL    |                |
# | is_hlr_required | bit(1)              | NO   |     | b'0'    |                |
# | hlr_id          | bigint(20) unsigned | YES  |     | NULL    |                |
# | is_default      | bit(1)              | NO   |     | b'0'    |                |
# | created_date    | datetime(3)         | YES  |     | NULL    |                |
# | creator_id      | bigint(20) unsigned | NO   | MUL | NULL    |                |
# +-----------------+---------------------+------+-----+---------+----------------+
# """,
#         """
# service_variant
# +------------------------------+----------------------+------+-----+---------+----------------+
# | Field                        | Type                 | Null | Key | Default | Extra          |
# +------------------------------+----------------------+------+-----+---------+----------------+
# | id                           | bigint(20) unsigned  | NO   | PRI | NULL    | auto_increment |
# | name                         | varchar(255)         | NO   |     | NULL    |                |
# | is_hidden                    | bit(1)               | NO   |     | b'0'    |                |
# | is_default                   | bit(1)               | NO   |     | b'0'    |                |
# | subscription_type            | varchar(10)          | NO   |     | FULL    |                |
# | profit_multiplier            | bigint(20)           | NO   |     | 1       |                |
# | discount_multiplier          | bigint(20)           | NO   |     | 1       |                |
# | duration_days                | smallint(5) unsigned | NO   |     | NULL    |                |
# | service_id                   | bigint(20) unsigned  | NO   | MUL | NULL    |                |
# | downgrade_service_variant_id | bigint(20) unsigned  | YES  | MUL | NULL    |                |
# | price_category_id            | bigint(20) unsigned  | NO   | MUL | NULL    |                |
# | renewal_policy_id            | bigint(20) unsigned  | YES  | MUL | NULL    |                |
# | pre_active_renewal_policy_id | bigint(20) unsigned  | YES  | MUL | NULL    |                |
# | reminder_policy_id           | bigint(20) unsigned  | YES  | MUL | NULL    |                |
# | created_date                 | datetime(3)          | YES  |     | NULL    |                |
# | creator_id                   | bigint(20) unsigned  | NO   | MUL | NULL    |                |
# | channel                      | varchar(10)          | YES  |     | WEB     |                |
# | purchase_id                  | bigint(20) unsigned  | YES  |     | NULL    |                |
# | renewal_id                   | bigint(20) unsigned  | YES  |     | NULL    |                |
# +------------------------------+----------------------+------+-----+---------+----------------+
# """,
#         """
# subscriber
# +--------------+---------------------+------+-----+----------------------+----------------+
# | Field        | Type                | Null | Key | Default              | Extra          |
# +--------------+---------------------+------+-----+----------------------+----------------+
# | id           | bigint(20) unsigned | NO   | PRI | NULL                 | auto_increment |
# | msisdn       | varchar(16)         | NO   | UNI | NULL                 |                |
# | language     | varchar(32)         | NO   |     | en                   |                |
# | created_date | datetime(3)         | NO   |     | current_timestamp(3) |                |
# +--------------+---------------------+------+-----+----------------------+----------------+
# """,
#         """
# subscription
# +-------------------------+---------------------+------+-----+---------+----------------+
# | Field                   | Type                | Null | Key | Default | Extra          |
# +-------------------------+---------------------+------+-----+---------+----------------+
# | id                      | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
# | created_date            | datetime(3)         | YES  |     | NULL    |                |
# | end_date                | datetime(3)         | YES  |     | NULL    |                |
# | last_charging_date      | datetime(3)         | YES  |     | NULL    |                |
# | next_charging_date      | datetime(3)         | YES  | MUL | NULL    |                |
# | charging_metadata       | longtext            | YES  |     | NULL    |                |
# | status                  | varchar(15)         | NO   |     | NULL    |                |
# | subscriber_id           | bigint(20) unsigned | NO   | MUL | NULL    |                |
# | service_id              | bigint(20) unsigned | NO   | MUL | NULL    |                |
# | service_variant_id      | bigint(20) unsigned | NO   | MUL | NULL    |                |
# | last_activation_date    | datetime(3)         | NO   |     | NULL    |                |
# | renewal_cycle_state     | longtext            | YES  |     | NULL    |                |
# | next_debt_charging_date | datetime(3)         | YES  | MUL | NULL    |                |
# | channel                 | varchar(10)         | NO   |     | NULL    |                |
# +-------------------------+---------------------+------+-----+---------+----------------+
# """,
#         """
# subscription_purchase
# +--------------------+---------------------+------+-----+---------+----------------+
# | Field              | Type                | Null | Key | Default | Extra          |
# +--------------------+---------------------+------+-----+---------+----------------+
# | id                 | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
# | subscription_id    | bigint(20) unsigned | YES  |     | NULL    |                |
# | subscriber_id      | bigint(20) unsigned | NO   |     | NULL    |                |
# | service_variant_id | bigint(20) unsigned | NO   |     | NULL    |                |
# | date               | datetime(3)         | YES  |     | NULL    |                |
# | price              | bigint(20)          | NO   |     | NULL    |                |
# | refund_information | varchar(128)        | YES  |     | NULL    |                |
# +--------------------+---------------------+------+-----+---------+----------------+
# """,
#         """
# user
# +----------------+---------------------+------+-----+---------+----------------+
# | Field          | Type                | Null | Key | Default | Extra          |
# +----------------+---------------------+------+-----+---------+----------------+
# | id             | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
# | username       | varchar(255)        | NO   | UNI | NULL    |                |
# | email          | varchar(255)        | YES  |     | NULL    |                |
# | password       | varchar(255)        | NO   |     | NULL    |                |
# | is_blocked     | bit(1)              | NO   |     | b'0'    |                |
# | role           | varchar(255)        | YES  |     | NULL    |                |
# | provider_type  | varchar(15)         | NO   |     | BOTH    |                |
# | parent_user_id | bigint(20) unsigned | YES  | MUL | NULL    |                |
# +----------------+---------------------+------+-----+---------+----------------+
#         """
#     ]
#     for item in list_parse:
#         name, list_items = divide_item(item)
#         print('----------')
#         print(f"{name}")
#         parse_db_rows_item(list_items)
#         print('----------')
#     print(DPDP_RBT.print_out())
#     list_types = ["bigint(20) unsigned", "varchar", "varchar", "varchar", "bit(1)", "varchar", "varchar", "bigint(20) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "datetime(3)", "bigint(20)", "varchar", "bigint(20) unsigned", "datetime(3)", "datetime(3)", "datetime(3)", "datetime(3)", "longtext", "varchar", "bigint(20) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "datetime(3)", "longtext", "datetime(3)", "varchar", "bigint(20) unsigned", "varchar", "varchar", "datetime(3)", "bigint(20) unsigned", "bigint(20) unsigned", "varchar", "bit(1)", "bigint(20) unsigned", "bit(1)", "datetime(3)", "bigint(20) unsigned", "varchar", "bigint(20) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "varchar", "bit(1)", "bigint(20) unsigned", "bit(1)", "datetime(3)", "bigint(20) unsigned", "bigint(21)", "bigint(21)", "bigint(21)", "bigint(21)", "bigint(21)", "bigint(21) unsigned", "tinyint(1) unsigned", "bigint(21)", "bigint(20) unsigned", "varchar", "bigint(20) unsigned", "datetime(3)", "bigint(20) unsigned", "bit(1)", "bigint(20) unsigned", "smallint(5) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "smallint(5) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "datetime(3)", "datetime(3)", "bigint(20) unsigned", "varchar", "varchar", "bigint(20) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "varchar", "bigint(20)", "bigint(20)", "bigint(20) unsigned", "datetime(3)", "longtext", "bigint(20) unsigned", "varchar", "varchar", "bigint(20) unsigned", "varchar", "bigint(20) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "varchar", "text", "bigint(20) unsigned", "varchar", "bit(1)", "bigint(20) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "varchar", "bit(1)", "datetime(3)", "bigint(20) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "datetime(3)", "bigint(20)", "varchar", "bit(1)", "varchar", "bigint(20) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "datetime(3)", "bigint(20) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "varchar", "bit(1)", "smallint(5) unsigned", "longtext", "bigint(20) unsigned", "bigint(20) unsigned", "bigint(20) unsigned", "datetime(3)", "varchar", "varchar", "bit(1)", "datetime(3)", "bigint(20)", "int(11)", "varchar", "bigint(20)", "int(11)", "varchar", "bigint(20)", "bigint(20)", "varchar", "text", "varchar", "varchar", "text", "int(11)", "bit(1)", "datetime", "bit(1)", "datetime", "varchar", "varchar", "varchar", "varchar", "datetime", "bigint(20)", "varchar", "varchar", "datetime", "varchar", "varchar", "bit(1)", "bit(1)", "text", "bigint(20)", "varchar", "text", "bigint(20)", "bigint(20)", "varchar", "varchar"]
#     print(set(list_types))
    pprint(RBT_Web.dict_rbt_dpdp)


if __name__ == "__main__":
    main()
