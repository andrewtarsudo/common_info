"""
notification_template
notification_template.event_id -> notification_event.id
notification_template.service_id -> service.id
----------
notification_webhook
notification_webhook.product_id -> product.id
----------
price_category
price_category.creator_id -> user.id
content.price_category_id -> price_category.id
service_variant.price_category_id -> price_category.id
----------
product
product.partner_id -> user.id
notification_webhook.product_id -> product.id
content.product_id -> product.id
service.product_id -> product.id
----------
reminder
reminder.subscription_id -> subscription.id
----------
reminder_policy
reminder_policy.notification_event_id -> notification_event.id
service_variant.reminder_policy_id -> reminder_policy.id
----------
renewal_policy
service_variant.renewal_policy_id -> renewal_policy.id
service_variant.pre_active_renewal_policy_id -> renewal_policy.id
----------
renewal_task
renewal_task.subscriber_id -> subscriber.id
renewal_task.subscription_id -> subscription.id
----------
seq_content_order_code
----------
service
service.creator_id -> user.id
service.product_id -> product.id
subscription.service_id -> service.id
notification_template.service_id -> service.id
service_variant.service_id -> service.id
----------
service_variant
service_variant.renewal_policy_id -> renewal_policy.id
service_variant.pre_active_renewal_policy_id -> renewal_policy.id
service_variant.reminder_policy_id -> reminder_policy.id
service_variant.price_category_id -> price_category.id
service_variant.downgrade_service_variant_id -> service_variant.id
service_variant.creator_id -> user.id
service_variant.service_id -> service.id
subscription_purchase.service_variant_id -> service_variant.id
subscription.service_variant_id -> service_variant.id
service_variant.downgrade_service_variant_id -> service_variant.id
----------
subscriber
gift.from_subscriber_id -> subscriber.id
gift.to_subscriber_id -> subscriber.id
renewal_task.subscriber_id -> subscriber.id
subscription_purchase.subscriber_id -> subscriber.id
content_purchase.subscriber_id -> subscriber.id
content_ownership.subscriber_id -> subscriber.id
subscription.subscriber_id -> subscriber.id
----------
subscription
subscription.subscriber_id -> subscriber.id
subscription.service_variant_id -> service_variant.id
subscription.service_id -> service.id
renewal_task.subscription_id -> subscription.id
subscription_purchase.subscription_id -> subscription.id
reminder.subscription_id -> subscription.id
----------
subscription_purchase
subscription_purchase.subscriber_id -> subscriber.id
subscription_purchase.service_variant_id -> service_variant.id
subscription_purchase.subscription_id -> subscription.id
----------
user
user.parent_user_id -> user.id
price_category.creator_id -> user.id
user.parent_user_id -> user.id
product.partner_id -> user.id
content.provider_id -> user.id
service_variant.creator_id -> user.id
service.creator_id -> user.id




----------
audit
----------
caller_group
caller_group.subscriber_id -> subscriber.id
caller_group_member.group_id -> caller_group.id
rule_caller_group.caller_group_id -> caller_group.id
----------
caller_group_member
caller_group_member.member_id -> member.id
caller_group_member.group_id -> caller_group.id
----------
corporate_member
corporate_member.subscriber_id -> subscriber.id
----------
hidden_content
----------
member
member.subscriber_id -> subscriber.id
caller_group_member.member_id -> member.id
----------
playlist_content
----------
rule
rule.subscriber_id -> subscriber.id
rule_caller_group.rule_id -> rule.id
rule_schedule.rule_id -> rule.id
rule_content.rule_id -> rule.id
----------
rule_caller_group
rule_caller_group.caller_group_id -> caller_group.id
rule_caller_group.rule_id -> rule.id
----------
rule_content
rule_content.rule_id -> rule.id
rule_content.subscriber_content_id -> subscriber_content.id
----------
rule_schedule
rule_schedule.schedule_id -> schedule.id
rule_schedule.rule_id -> rule.id
----------
schedule
schedule.subscriber_id -> subscriber.id
rule_schedule.schedule_id -> schedule.id
----------
setting
----------
subscriber
member.subscriber_id -> subscriber.id
corporate_member.subscriber_id -> subscriber.id
caller_group.subscriber_id -> subscriber.id
schedule.subscriber_id -> subscriber.id
rule.subscriber_id -> subscriber.id
subscriber_content.subscriber_id -> subscriber.id
subscriber_content_list.subscriber_id -> subscriber.id
----------
subscriber_content
subscriber_content.subscriber_id -> subscriber.id
rule_content.subscriber_content_id -> subscriber_content.id
subscriber_content_list_item.subscriber_content_id -> subscriber_content.id
----------
subscriber_content_list
subscriber_content_list.subscriber_id -> subscriber.id
subscriber_content_list_item.subscriber_content_list_id -> subscriber_content_list.id
----------
subscriber_content_list_item
subscriber_content_list_item.subscriber_content_list_id -> subscriber_content_list.id
subscriber_content_list_item.subscriber_content_id -> subscriber_content.id




----------
album
album.creator_id -> user.id
album.moderator_id -> user.id
album.updater_id -> user.id
album.artist_id -> artist.id
album_category.album_id -> album.id
raw_album.album_id -> album.id
raw_tone.album_id -> album.id
tone.album_id -> album.id
----------
album_category
album_category.album_id -> album.id
album_category.category_id -> category.id
----------
app_settings
----------
artist
artist.creator_id -> user.id
artist.moderator_id -> user.id
artist.updater_id -> user.id
raw_album.artist_id -> artist.id
raw_artist.artist_id -> artist.id
raw_tone.artist_id -> artist.id
tone.artist_id -> artist.id
album.artist_id -> artist.id
----------
audit
audit.user_id -> user.id
audit.object_owner_id -> user.id
----------
category
category.creator_id -> user.id
category.updater_id -> user.id
raw_album_category.category_id -> category.id
album_category.category_id -> category.id
tone_category.category_id -> category.id
----------
content_list
content_list.creator_id -> user.id
content_list_content.content_list_id -> content_list.id
----------
content_list_content
content_list_content.content_list_id -> content_list.id
content_list_content.content_id -> provided_content.content_id
----------
license
license.provider_id -> user.id
license.updater_id -> user.id
raw_tone.license_id -> license.id
tone.license_id -> license.id
raw_license.license_id -> license.id
----------
partner
user.partner_id -> partner.id
----------
playlist
playlist.creator_id -> user.id
playlist.moderator_id -> user.id
playlist_content.playlist_id -> playlist.id
----------
playlist_content
playlist_content.content_id -> provided_content.content_id
playlist_content.playlist_id -> playlist.id
----------
provided_content
content_list_content.content_id -> provided_content.content_id
playlist_content.content_id -> provided_content.content_id
raw_playlist_content.content_id -> provided_content.content_id
----------
raw_album
raw_album.creator_id -> user.id
raw_album.moderator_id -> user.id
raw_album.album_id -> album.id
raw_album.artist_id -> artist.id
raw_album_category.raw_album_id -> raw_album.id
----------
raw_album_category
raw_album_category.raw_album_id -> raw_album.id
raw_album_category.category_id -> category.id
----------
raw_artist
raw_artist.creator_id -> user.id
raw_artist.moderator_id -> user.id
raw_artist.artist_id -> artist.id
----------
raw_custom_tone
raw_custom_tone.moderator_id -> user.id
----------
raw_license
raw_license.creator_id -> user.id
raw_license.moderator_id -> user.id
raw_license.license_id -> license.id
----------
raw_partner
raw_partner.moderator_id -> user.id
----------
raw_partner_service
raw_partner_service.creator_id -> user.id
raw_partner_service.moderator_id -> user.id
----------
raw_playlist
raw_playlist_content.raw_playlist_id -> raw_playlist.id
----------
raw_playlist_content
raw_playlist_content.raw_playlist_id -> raw_playlist.id
raw_playlist_content.content_id -> provided_content.content_id
----------
raw_service_variant
raw_service_variant.creator_id -> user.id
raw_service_variant.moderator_id -> user.id
----------
raw_tone
raw_tone.creator_id -> user.id
raw_tone.moderator_id -> user.id
raw_tone.album_id -> album.id
raw_tone.artist_id -> artist.id
raw_tone.tone_id -> tone.id
raw_tone.license_id -> license.id
----------
raw_tone_category
----------
role
user_role.role_id -> role.id
----------
tone
tone.creator_id -> user.id
tone.moderator_id -> user.id
tone.album_id -> album.id
tone.artist_id -> artist.id
tone.license_id -> license.id
tone_category.tone_id -> tone.id
raw_tone.tone_id -> tone.id
----------
tone_category
tone_category.tone_id -> tone.id
tone_category.category_id -> category.id
----------
user
user.partner_id -> partner.id
user_role.user_id -> user.id
content_list.creator_id -> user.id
raw_album.creator_id -> user.id
raw_album.moderator_id -> user.id
raw_artist.creator_id -> user.id
raw_artist.moderator_id -> user.id
raw_tone.creator_id -> user.id
raw_tone.moderator_id -> user.id
tone.creator_id -> user.id
tone.moderator_id -> user.id
raw_license.creator_id -> user.id
raw_license.moderator_id -> user.id
license.provider_id -> user.id
license.updater_id -> user.id
playlist.creator_id -> user.id
playlist.moderator_id -> user.id
raw_custom_tone.moderator_id -> user.id
raw_partner_service.creator_id -> user.id
raw_partner_service.moderator_id -> user.id
raw_service_variant.creator_id -> user.id
raw_service_variant.moderator_id -> user.id
raw_partner.moderator_id -> user.id
artist.creator_id -> user.id
artist.moderator_id -> user.id
artist.updater_id -> user.id
album.creator_id -> user.id
album.moderator_id -> user.id
album.updater_id -> user.id
user_moderator.user_id -> user.id
user_moderator.moderator_id -> user.id
audit.user_id -> user.id
audit.object_owner_id -> user.id
category.creator_id -> user.id
category.updater_id -> user.id
----------
user_moderator
user_moderator.user_id -> user.id
user_moderator.moderator_id -> user.id
----------
user_role
user_role.role_id -> role.id
user_role.user_id -> user.id

"""


class Const:
    dict_dpdp_web: dict[str, tuple[str]] = {
        'album': (
            'id', 'creation_time', 'creator_id', 'name', 'thumbnail', 'releaseYear', 'moderation_time', 'moderator_id',
            'update_time', 'updater_id', 'artist_id'),
        'album_category': ('album_id', 'category_id'),
        'app_settings': ('id', 'custom_price_category_id'),
        'artist': (
            'id', 'creation_time', 'creator_id', 'name', 'thumbnail', 'moderation_time', 'moderator_id', 'update_time',
            'updater_id'),
        'audit': (
            'id', 'date_time', 'user_id', 'user_ip', 'channel_id', 'msisdn', 'operation', 'object_type', 'props',
            'object_owner_id', 'product_id'),
        'category': ('id', 'creation_time', 'creator_id', 'name', 'update_time', 'updater_id'),
        'content_list': ('id', 'name', 'content_orders', 'creator_id', 'creation_time'),
        'content_list_content': ('content_list_id', 'content_id'),
        'license': ('id', 'creation_time', 'expire_date', 'name', 'provider_id', 'update_time', 'updater_id'),
        'partner': (
            'id', 'type', 'business_division', 'company_name', 'company_owner_name', 'address', 'point_of_contact',
            'contact_number', 'point_of_contact', 'contact_number', 'email', 'agreements_no'),
        'playlist': ('id', 'name', 'creation_time', 'creator_id', 'thumbnail', 'moderation_time', 'moderator_id'),
        'playlist_content': ('playlist_id', 'content_id'),
        'provided_content': (
            'content_id', 'creation_time', 'creator_id', 'price_category_id', 'order_code', 'is_hidden', 'tone_id',
            'playlist_id', 'is_expired'),
        'raw_album': (
            'id', 'creator_id', 'name', 'operation_time', 'thumbnail', 'releaseYear', 'is_moderate', 'moderator_id',
            'album_id', 'artist_id'),
        'raw_album_category': ('raw_album_id', 'category_id'),
        'raw_artist': (
            'id', 'creator_id', 'name', 'operation_time', 'thumbnail', 'is_moderate', 'artist_id', 'moderator_id'),
        'raw_custom_tone': ('id', 'name', 'operation_time', 'is_moderate', 'msisdn', 'moderator_id'),
        'raw_license': ('id', 'creator_id', 'name', 'expire_date', 'operation_time', 'moderator_id', 'license_id'),
        'raw_partner': (
            'id', 'type', 'business_division', 'company_name', 'company_owner_name', 'address',
            'point_of_contact', 'contact_number', 'point_of_contact', 'contact_number', 'email',
            'agreements_no', 'creation_time', 'moderator_id'),
        'raw_partner_service': (
            'id', 'name', 'hlr_id', 'is_hlr_required', 'is_default', 'creation_time', 'creator_id', 'moderator_id'),
        'raw_playlist': (
            'id', 'creator_id', 'moderator_id', 'name', 'operation_time', 'order_code',
            'price_category_id', 'thumbnail', 'is_moderate', 'playlist_id'),
        'raw_playlist_content': ('raw_playlist_id', 'content_id'),
        'raw_service_variant': (
            'id', 'name', 'service_id', 'price_id', 'variant', 'type_id', 'is_hidden', 'is_default',
            'downgrade_service_variant_id', 'renewal_policy_id', 'profit_multiplier', 'discount_multiplier',
            'creation_time', 'creator_id', 'moderator_id'),
        'raw_tone': (
            'id', 'creator_id', 'moderator_id', 'operation_time', 'order_code', 'price_category_id', 'title',
            'album_id', 'artist_id', 'tone_id', 'license_id', 'is_moderate'),
        'raw_tone_category': ('raw_tone_id', 'category_id'),
        'role': ('id', 'name', 'privileges', 'session_limit'),
        'tone': (
            'id', 'creation_time', 'creator_id', 'title', 'moderation_time', 'moderator_id', 'album_id', 'artist_id',
            'license_id'),
        'tone_category': ('tone_id', 'category_id'),
        'user': ('id', 'name', 'last_login', 'is_blocked', 'partner_id', 'product_id', 'ip_masks'),
        'user_moderator': ('user_id', 'moderator_id'), 'user_role': ('user_id', 'role_id')
    }
    dict_dpdp_core: dict[str, tuple[str]] = {
        'RepoLink': ('id', 'content_id', 'owner_system', 'owner_object'),
        'RepoMetadata': (
            'id', 'name', 'path', 'load_date', 'owner_system', 'owner_object', 'synchronization', 'remove',
            'node_status_info', 'version', 'lang', 'params'),
        'SenderMessage': (
            'id', 'direction_name', 'url', 'source_address', 'destination_address', 'body', 'attempt_count',
            'processed', 'send_time', 'is_immediate', 'validity_time', 'subject_message', 'http_headers', 'schedule',
            'params', 'creation_time'),
        'TaskQueue': ('id', 'action', 'node_name', 'content_id', 'remote_task_id', 'owner', 'content_version'),
        'content': (
            'id', 'external_id', 'order_code', 'name', 'is_hidden', 'duration_days', 'metadata', 'product_id',
            'provider_id', 'price_category_id', 'created_date', 'status', 'type', 'is_file_present',
            'expiration_date'),
        'content_ownership': ('id', 'content_id', 'subscriber_id', 'created_date'),
        'content_purchase': (
            'id', 'subscriber_id', 'content_id', 'date', 'price', 'channel', 'is_copied', 'refund_information'),
        'gift': (
            'id', 'content_purchase_id', 'content_id', 'from_subscriber_id', 'to_subscriber_id', 'status',
            'is_requested',
            'created_date'),
        'notification_event': ('id', 'name', 'is_predefined'),
        'notification_template': ('id', 'event_id', 'service_id', 'language', 'text'),
        'notification_webhook': ('id', 'endpoint_url', 'endpoint_name', 'product_id', 'type'),
        'price_category': (
            'id', 'purchase_id', 'renewal_id', 'name', 'purchase_fee', 'renewal_fee', 'creator_id', 'creation_date',
            'channel_params'),
        'product': ('id', 'external_id', 'name', 'partner_id'),
        'reminder': ('id', 'subscription_id', 'sent_date', 'receipt_date'),
        'reminder_policy': ('id', 'days_to_reminder', 'notification_event_id'),
        'renewal_policy': ('id', 'version', 'policy_info'),
        'renewal_task': ('id', 'type', 'subscription_id', 'created_date', 'subscriber_id', 'debt_only'),
        'seq_content_order_code': (
            'next_not_cached_value', 'minimum_value', 'maximum_value', 'start_value', 'increment', 'cache_size',
            'cycle_option', 'cycle_count'),
        'service': (
            'id', 'product_id', 'name', 'is_hlr_required', 'hlr_id', 'is_default', 'created_date', 'creator_id'),
        'service_variant': (
            'id', 'product_id', 'name', 'is_hlr_required', 'hlr_id', 'is_default', 'created_date', 'creator_id',
            'channel', 'purchase_id', 'renewal_id'),
        'subscriber': ('id', 'msisdn', 'language', 'created_date'),
        'subscription': (
            'id', 'created_date', 'end_date', 'last_charging_date', 'next_charging_date', 'charging_metadata', 'status',
            'subscriber_id', 'service_id', 'service_variant_id', 'last_activation_date', 'renewal_cycle_state',
            'next_debt_charging_date', 'channel'),
        'subscription_purchase': (
            'id', 'subscription_id', 'subscriber_id', 'service_variant_id', 'date', 'price', 'refund_information'),
        'user': ('id', 'username', 'email', 'password', 'is_blocked', 'role', 'provider_type', 'parent_user_id')
    }

    dict_rbt_web = {
        "audit": (
            "id", "date_time", "user_id", "user_ip", "channel_id", "msisdn", "operation", "object_type", "props",
            "object_owner_id"),
        "caller_group": ("id", "subscriber_id", "name", "type"),
        "caller_group_member": ("group_id", "member_id"),
        "corporate_member": ("id", "subscriber_id", "msisdn"),
        "hidden_content": ("content_id",),
        "member": ("id", "subscriber_id", "msisdn", "name"),
        "playlist_content": ("playlist_id", "tone_id"),
        "rule": ("id", "name", "subscriber_id", "order", "type", "mode", "counter"),
        "rule_caller_group": ("rule_id", "caller_group_id"),
        "rule_content": ("rule_id", "subscriber_content_id"),
        "rule_schedule": ("rule_id", "schedule_id"),
        "schedule": ("id", "subscriber_id", "name", "from_time", "till_time", "ranges"),
        "setting": ("id", "default_tone_id"),
        "subscriber": (
            "id", "msisdn", "password", "is_private", "subscription_time", "renewal_time", "rbt_package_id",
            "is_rbt_overlay", "type", "anti_rbt_package_id", "anti_renewal_time", "anti_subscription_time",
            "is_anti_rbt_overlay"),
        "subscriber_content": ("id", "subscriber_id", "content_id", "content_type", "is_custom"),
        "subscriber_content_list": ("id", "subscriber_id", "name"),
        "subscriber_content_list_item": ("subscriber_content_list_id", "subscriber_content_id")
    }

    dict_types: dict[str, dict[str, tuple[str]]] = {
        "dpdp_web": dict_dpdp_web, "dpdp_core": dict_dpdp_core, "rbt_web": dict_rbt_web
    }

    dict_connections = dict()


class Connection:
    index = 0

    __slots__ = ("identifier", "table_from", "table_to", "table_type", "param_from", "param_to")

    def __init__(self, *,
                 table_from: str,
                 table_to: str,
                 param_from: str,
                 param_to: str,
                 table_type: str = "dpdp_web"):
        self.table_from = table_from
        self.table_to = table_to
        self.param_from = param_from
        self.param_to = param_to
        self.table_type = table_type
        self.identifier = Connection.index

        Const.dict_connections[self.identifier] = self
        Connection.index += 1

    def __str__(self):
        return f"{self.table_from}.{self.param_from} == {self.table_to}.{self.param_to}, id = {self.identifier}"

    def __repr__(self):
        return f"Connection(table_from={self.table_from}, table_to={self.table_to}, param_from={self.param_from}, " \
               f"param_to={self.param_to}), id = {self.identifier}"

    def __key(self):
        return self.table_from, self.table_to, self.table_type, self.param_from, self.param_to, self.identifier

    def __hash__(self):
        return hash((self.table_from, self.table_to, self.table_type, self.param_from, self.param_to, self.identifier))

    @property
    def tables(self):
        return Const.dict_types[self.table_type]

    @property
    def verify_from(self):
        return self.param_from in self.tables.keys()

    @property
    def verify_to(self):
        return self.param_to in self.tables.keys()

    def __eq__(self, other):
        if isinstance(other, Connection):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Connection):
            return self.__key() != other.__key()
        else:
            return NotImplemented


class ConnectionList:
    __slots__ = ("name", "connections")

    def __init__(self, name: str, connections: list[Connection] = None):
        if connections is None:
            connections = []
        self.name = name
        self.connections = connections

    def __len__(self):
        return len(self.connections)

    @property
    def full_connections(self):
        return list(Const.dict_connections.items())

    @property
    def connections_id(self):
        return list(Const.dict_connections.keys())

    def attr_table_from_to(self, table_name: str, table: str, attr: str):
        return [
            getattr(connection, attr) for connection in self.connections if getattr(connection, table) == table_name]

    def conn_from_attr(self, identifier: int):
        for index, connection in self.connections:
            if index == identifier:
                return connection.param_from

    def conn_to_attr(self, identifier: int):
        for index, connection in self.connections:
            if index == identifier:
                return connection.param_to

    @property
    def verify_from(self):
        return [connection for connection in self.connections if not connection.verify_from]

    @property
    def verify_to(self):
        return [connection.identifier for connection in self.connections if not connection.verify_to]

    def get_from(self, table_name: str):
        table_from_from = self.attr_table_from_to(table_name, "table_from", "table_from")
        table_from_to = self.attr_table_from_to(table_name, "table_from", "table_to")
        attr_from_from = self.attr_table_from_to(table_name, "table_from", "param_from")
        attr_from_to = self.attr_table_from_to(table_name, "table_from", "param_to")
        return tuple(zip(table_from_from, attr_from_from, table_from_to, attr_from_to))

    def get_from_strings(self, table_name: str):
        return [f"{table_from_from}.{attr_from_from} -> {table_from_to}.{attr_from_to}"
                for table_from_from, attr_from_from, table_from_to, attr_from_to in self.get_from(table_name)]

    def get_to(self, table_name: str):
        table_to_from = self.attr_table_from_to(table_name, "table_to", "table_from")
        table_to_to = self.attr_table_from_to(table_name, "table_to", "table_to")
        attr_to_from = self.attr_table_from_to(table_name, "table_to", "param_from")
        attr_to_to = self.attr_table_from_to(table_name, "table_to", "param_to")
        return tuple(zip(table_to_from, attr_to_from, table_to_to, attr_to_to))

    def get_to_strings(self, table_name: str):
        return [f"{table_to_from}.{attr_to_from} -> {table_to_to}.{attr_to_to}"
                for table_to_from, attr_to_from, table_to_to, attr_to_to in self.get_to(table_name)]

    def get_from_to(self, table_name: str):
        list_final: list[str] = []
        list_final.append(f"{table_name}")
        for line in self.get_from_strings(table_name):
            list_final.append(line)
        for line in self.get_to_strings(table_name):
            list_final.append(line)
        return "\n".join(list_final)


def get_connections(list_connections: list[tuple[str, str, str, str]]):
    return [Connection(table_from=table_from, table_to=table_to, param_from=param_from, param_to=param_to) for
            table_from, table_to, param_from, param_to in list_connections]


def get_result(list_connections):
    connections = get_connections(list_connections)
    connection_list = ConnectionList("connection_list", connections)

    if connection_list.verify_from and connection_list.verify_to:
        for item in Const.dict_dpdp_web.keys():
            print("----------")
            print(connection_list.get_from_to(item))


def main():
    list_connections_dpdp_core: list[tuple[str, str, str, str]] = [
        ("gift", "content_purchase", "content_purchase_id", "id"),
        ("gift", "content", "content_id", "id"),
        ("gift", "subscriber", "from_subscriber_id", "id"),
        ("gift", "subscriber", "to_subscriber_id", "id"),
        ("renewal_task", "subscriber", "subscriber_id", "id"),
        ("renewal_task", "subscription", "subscription_id", "id"),
        ("subscription_purchase", "subscriber", "subscriber_id", "id"),
        ("subscription_purchase", "service_variant", "service_variant_id", "id"),
        ("subscription_purchase", "subscription", "subscription_id", "id"),
        ("reminder", "subscription", "subscription_id", "id"),
        ("RepoLink", "RepoMetadata", "content_id", "id"),
        ("RepoLink", "content", "content_id", "id"),
        ("TaskQueue", "content", "content_id", "id"),
        ("content_purchase", "content", "content_id", "id"),
        ("content_purchase", "subscriber", "subscriber_id", "id"),
        ("content_ownership", "content", "content_id", "id"),
        ("content_ownership", "subscriber", "subscriber_id", "id"),
        ("subscription", "subscriber", "subscriber_id", "id"),
        ("subscription", "service_variant", "service_variant_id", "id"),
        ("subscription", "service", "service_id", "id"),
        ("service_variant", "renewal_policy", "renewal_policy_id", "id"),
        ("service_variant", "renewal_policy", "pre_active_renewal_policy_id", "id"),
        ("service_variant", "reminder_policy", "reminder_policy_id", "id"),
        ("reminder_policy", "notification_event", "notification_event_id", "id"),
        ("notification_template", "notification_event", "event_id", "id"),
        ("notification_template", "service", "service_id", "id"),
        ("notification_webhook", "product", "product_id", "id"),
        ("content", "price_category", "price_category_id", "id"),
        ("service_variant", "price_category", "price_category_id", "id"),
        ("price_category", "user", "creator_id", "id"),
        ("service_variant", "service_variant", "downgrade_service_variant_id", "id"),
        ("content", "product", "product_id", "id"),
        ("user", "user", "parent_user_id", "id"),
        ("product", "user", "partner_id", "id"),
        ("content", "user", "provider_id", "id"),
        ("service_variant", "user", "creator_id", "id"),
        ("service", "user", "creator_id", "id"),
        ("service", "product", "product_id", "id"),
        ("service_variant", "service", "service_id", "id")
    ]

    list_connections_rbt_web = [
        ("caller_group_member", "member", "member_id", "id"),
        ("caller_group_member", "caller_group", "group_id", "id"),
        ("rule_caller_group", "caller_group", "caller_group_id", "id"),
        ("rule_caller_group", "rule", "rule_id", "id"),
        ("rule_schedule", "schedule", "schedule_id", "id"),
        ("rule_schedule", "rule", "rule_id", "id"),
        ("rule_content", "rule", "rule_id", "id"),
        ("rule_content", "subscriber_content", "subscriber_content_id", "id"),
        ("subscriber_content_list_item", "subscriber_content_list", "subscriber_content_list_id", "id"),
        ("subscriber_content_list_item", "subscriber_content", "subscriber_content_id", "id"),
        ("member", "subscriber", "subscriber_id", "id"),
        ("corporate_member", "subscriber", "subscriber_id", "id"),
        ("caller_group", "subscriber", "subscriber_id", "id"),
        ("schedule", "subscriber", "subscriber_id", "id"),
        ("rule", "subscriber", "subscriber_id", "id"),
        ("subscriber_content", "subscriber", "subscriber_id", "id"),
        ("subscriber_content_list", "subscriber", "subscriber_id", "id")
    ]

    list_connections_dpdp_web = [
        ("raw_album_category", "raw_album", "raw_album_id", "id"),
        ("raw_album_category", "category", "category_id", "id"),
        ("album_category", "album", "album_id", "id"),
        ("album_category", "category", "category_id", "id"),
        ("user_role", "role", "role_id", "id"),
        ("user_role", "user", "user_id", "id"),
        ("content_list", "user", "creator_id", "id"),
        ("content_list_content", "content_list", "content_list_id", "id"),
        ("content_list_content", "provided_content", "content_id", "content_id"),
        ("playlist_content", "provided_content", "content_id", "content_id"),
        ("playlist_content", "playlist", "playlist_id", "id"),
        ("raw_playlist_content", "raw_playlist", "raw_playlist_id", "id"),
        ("raw_playlist_content", "provided_content", "content_id", "content_id"),
        ("tone_category", "tone", "tone_id", "id"),
        ("tone_category", "category", "category_id", "id"),
        ("raw_album", "user", "creator_id", "id"),
        ("raw_album", "user", "moderator_id", "id"),
        ("raw_album", "album", "album_id", "id"),
        ("raw_album", "artist", "artist_id", "id"),
        ("raw_artist", "user", "creator_id", "id"),
        ("raw_artist", "user", "moderator_id", "id"),
        ("raw_artist", "artist", "artist_id", "id"),
        ("raw_tone", "user", "creator_id", "id"),
        ("raw_tone", "user", "moderator_id", "id"),
        ("raw_tone", "album", "album_id", "id"),
        ("raw_tone", "artist", "artist_id", "id"),
        ("raw_tone", "tone", "tone_id", "id"),
        ("raw_tone", "license", "license_id", "id"),
        ("tone", "user", "creator_id", "id"),
        ("tone", "user", "moderator_id", "id"),
        ("tone", "album", "album_id", "id"),
        ("tone", "artist", "artist_id", "id"),
        ("tone", "license", "license_id", "id"),
        ("raw_license", "user", "creator_id", "id"),
        ("raw_license", "user", "moderator_id", "id"),
        ("raw_license", "license", "license_id", "id"),
        ("license", "user", "provider_id", "id"),
        ("license", "user", "updater_id", "id"),
        ("playlist", "user", "creator_id", "id"),
        ("playlist", "user", "moderator_id", "id"),
        ("raw_custom_tone", "user", "moderator_id", "id"),
        ("raw_partner_service", "user", "creator_id", "id"),
        ("raw_partner_service", "user", "moderator_id", "id"),
        ("raw_service_variant", "user", "creator_id", "id"),
        ("raw_service_variant", "user", "moderator_id", "id"),
        ("raw_partner", "user", "moderator_id", "id"),
        ("artist", "user", "creator_id", "id"),
        ("artist", "user", "moderator_id", "id"),
        ("artist", "user", "updater_id", "id"),
        ("album", "user", "creator_id", "id"),
        ("album", "user", "moderator_id", "id"),
        ("album", "user", "updater_id", "id"),
        ("album", "artist", "artist_id", "id"),
        ("user_moderator", "user", "user_id", "id"),
        ("user_moderator", "user", "moderator_id", "id"),
        ("audit", "user", "user_id", "id"),
        ("audit", "user", "object_owner_id", "id"),
        ("user", "partner", "partner_id", "id"),
        ("category", "user", "creator_id", "id"),
        ("category", "user", "updater_id", "id")
    ]

    get_result(list_connections_dpdp_web)


if __name__ == "__main__":
    main()
