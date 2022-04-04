from pprint import pprint
import sys


def parse_db_info():
    dict_indexes = {0: "Parameter", 1: "Type", 2: "NULL", 3: "Key", 4: "Default", 5: "Extra"}
    print("Lines to parse:\n")
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
        print(f"=====\n{dict_indexes[idx]}\n=====")
        for value in res_list:
            if value == "------":
                print()
            else:
                print(value)
    print("++++++++++end++++++++++")
    print(f"lines: {num_lines}")

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

    list_questions = [("remove", "RepoMetadata.remove"), ("url", "SenderMessage.url")]


def main():
    parse_db_info()


if __name__ == "__main__":
    main()
