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

    dict_types: dict[str, dict[str, tuple[str]]] = {"dpdp_web": dict_dpdp_web, "dpdp_core": dict_dpdp_core}

    dict_connections = dict()

# class TableConst:
#     def __init__(self, name, table_type):
#         self.name = name
#         self.table_type = table_type
#
#     @property
#     def product(self) -> dict[str, tuple[str]]:
#         return Const.dict_types[self.table_type]
#
#     @property
#     def tables(self):
#         return self.product.keys()
#
#     @property
#     def params(self):
#         return self.product.values()


class Connection:
    index = 0

    __slots__ = ("identifier", "table_from", "table_to", "table_type", "param_from", "param_to")

    def __init__(self, table_from: str, table_to: str, table_type: str, param_from: str, param_to: str):
        self.table_from = table_from
        self.table_to = table_to
        self.table_type = table_type
        self.param_from = param_from
        self.param_to = param_to
        self.identifier = Connection.index

        Const.dict_connections[self.identifier] = self
        Connection.index += 1

    def __key(self):
        return self.table_from, self.table_to, self.table_type, self.param_from, self.param_to, self.identifier

    def __hash__(self):
        return hash((self.table_from, self.table_to, self.table_type, self.param_from, self.param_to, self.identifier))

    @property
    def tables(self):
        return Const.dict_types[self.table_type]

    def table_attrs(self, name):
        return self.tables[name]

    @property
    def verify_from(self):
        return self.param_from in self.table_attrs(self.table_from)

    @property
    def verify_to(self):
        return self.param_to in self.table_attrs(self.table_to)

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

    def __init__(self, name, conns: list = None):
        if conns is None:
            cons = []

        self.name = name
        self.conns = conns

    @property
    def connections(self) -> list[Connection]:
        return list(Const.dict_connections.values())

    @property
    def connections_id(self):
        return list(Const.dict_connections.keys())

    @property
    def full_conn(self):
        return list(Const.dict_connections.items())

    def conn_table_from(self, table_from):
        return [connection.identifier for connection in self.connections if connection.table_from == table_from]

    def conn_table_to(self, table_to):
        return [connection.identifier for connection in self.connections if connection.table_to == table_to]

    def conn_from_attr(self, identifier):
        for index, connection in self.connections:
            if index == identifier:
                return connection.param_from

    def conn_to_attr(self, identifier):
        for index, connection in self.connections:
            if index == identifier:
                return connection.param_to


def parse(string: str):
    return string.split(", ")


def main():
    list_tables = [
        "RepoLink", "RepoMetadata", "SenderMessage", "TaskQueue", "content", "content_ownership", "content_purchase",
        "gift", "notification_event", "notification_template", "notification_webhook", "price_category", "product",
        "reminder", "reminder_policy", "renewal_policy", "renewal_task", "seq_content_order_code", "service",
        "service_variant", "subscriber", "subscription", "subscription_purchase", "user"
    ]

    list_attrs = [
        ("id", "content_id", "owner_system", "owner_object"),
        ("id", "name", "path", "load_date", "owner_system", "owner_object", "synchronization", "remove",
         "node_status_info", "version", "lang", "params"),
        ("id", "direction_name", "url", "source_address", "destination_address", "body", "attempt_count", "processed",
         "send_time", "is_immediate", "validity_time", "subject_message", "http_headers", "schedule", "params",
         "creation_time"),
        ("id", "action", "node_name", "content_id", "remote_task_id", "owner", "content_version"),
        ("id", "external_id", "order_code", "name", "is_hidden", "duration_days", "metadata", "product_id",
         "provider_id", "price_category_id", "created_date", "status", "type", "is_file_present", "expiration_date"),
        ("id", "content_id", "subscriber_id", "created_date"),
        ("id", "subscriber_id", "content_id", "date", "price", "channel", "is_copied", "refund_information"),
        ("id", "content_purchase_id", "content_id", "from_subscriber_id", "to_subscriber_id", "status", "is_requested",
         "created_date"),
        ("id", "name", "is_predefined"),
        ("id", "event_id", "service_id", "language", "text"),
        ("id", "endpoint_url", "endpoint_name", "product_id", "type"),
        ("id", "purchase_id", "renewal_id", "name", "purchase_fee", "renewal_fee", "creator_id", "creation_date",
         "channel_params"),
        ("id", "external_id", "name", "partner_id"),
        ("id", "subscription_id", "sent_date", "receipt_date"),
        ("id", "days_to_reminder", "notification_event_id"),
        ("id", "version", "policy_info"),
        ("id", "type", "subscription_id", "created_date", "subscriber_id", "debt_only"),
        ("next_not_cached_value", "minimum_value", "maximum_value", "start_value", "increment", "cache_size",
         "cycle_option", "cycle_count"),
        ("id", "product_id", "name", "is_hlr_required", "hlr_id", "is_default", "created_date", "creator_id"),
        ("id", "product_id", "name", "is_hlr_required", "hlr_id", "is_default", "created_date", "creator_id", "channel",
         "purchase_id", "renewal_id"),
        ("id", "msisdn", "language", "created_date"),
        ("id", "created_date", "end_date", "last_charging_date", "next_charging_date", "charging_metadata", "status",
         "subscriber_id", "service_id", "service_variant_id", "last_activation_date", "renewal_cycle_state",
         "next_debt_charging_date", "channel"),
        ("id", "subscription_id", "subscriber_id", "service_variant_id", "date", "price", "refund_information"),
        ("id", "username", "email", "password", "is_blocked", "role", "provider_type", "parent_user_id")
    ]

    table_dict = dict(zip(list_tables, list_attrs))
    print(table_dict)
    """
    gift(content_purchase_id) == content_purchase(id)
    gift(content_id) == content(id)
    gift(from_subscriber_id) == subscriber(id)
    gift(to_subscriber_id) == subscriber(id)
    renewal_task(subscriber_id) == subscriber(id)
    renewal_task(subscription_id) == subscription(id)
    subscription_purchase(subscriber_id) == subscriber(id)
    subscription_purchase(service_variant_id) == service_variant(id)
    subscription_purchase(subscription_id) == subscription(id)
    reminder(subscription_id) == subscription(id)
    RepoLink(content_id) == RepoMetadata(id)
    RepoLink(content_id) == content(id)
    TaskQueue(content_id) == content(id)
    content_purchase(content_id) == content(id)
    content_purchase(subscriber_id) == subscriber(id)
    content_ownership(content_id) == content(id)
    content_ownership(subscriber_id) == subscriber(id)
    subscription(subscriber_id) == subscriber(id)
    subscription(service_variant_id) == service_variant(id)
    subscription(service_id) == service(id)

    notification_template(event_id) == notification_event(id)
    notification_template(service_id) == service(id)
    notification_webhook(product_id) == product(id)
    """


if __name__ == "__main__":
    main()
