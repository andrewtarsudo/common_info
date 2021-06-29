---
title : "smpp.cfg"
description : "Файл настройки подключений внешних приложений"
weight : 3
---

В файле настраиваются параметры SMPP для взаимодействия с внешними службами и подключения как внешней службы.

Ключ для reload - **reload smpp.cfg**.

Используется во всех версиях.
## Описание параметров
|Name|Description|Type|Default|O/M|P/R|Version|
|:---|:----------|:---|:------|:--|:--|:------|
|**[General]**||
|CheckImeiSmppId|Идентификатор SMPP–направления для адресации запросов CheckIMEI.|int|0|O|R||
|welcome_port|Порт для взаимодействия с внешними приложениями.|int<br>1-65535||M|P||
|UseSmppBlocking|Флаг блокирования SMPP–соединения при недоступности всех SIGTRAN–ассоциаций.|bool|0|O|R||
|**[directions]**||
|id|Уникальный идентификатор направления.|int||M|R||
|mode|Идентификатор режима обмена.<br>1 – SMPP_TRANSACTION_MODE, режим транзакций;<br>2 – SMPP_STORE_FORWARD_MODE, режим хранения на SMSC.|int||M|R||
|SMS_UseBRT|Флаг использования BRT для данного направления.|bool|0|O|R||
|SMS_UseDiameter|Флаг использования протокола Diameter для данного направления.|bool||O|R||
|SMS_MT_UseDiameter|Флаг использования протокола Diameter для MT‒SMS данного направления.|bool||O|R||
|SMS_MAP_MT_UseDiameter|Флаг использования Diameter–тарификации для сообщений Home Routing данного направления.|bool|0|O|R||
|reserved|Флаг использования соединения при отсутствии свободных обычных соединений.|bool|0|O|R||
|max_in_operations|Максимальное количество неподтвержденных MT‒SMS.|int|–1, без ограничений|O|R||
|in_bandwidth|Максимальное количество MT‒SMS в секунду.|int|–1, без ограничений|O|R||
|max_out_operations|Максимальное количество неподтвержденных MO‒SMS.|int|–1, без ограничений|O|R||
|out_bandwidth|Максимальное количество MO‒SMS в секунду.|int|–1, без ограничений|O|R||
|response_timeout|Время ожидания ответа.|int ms|140000|O|R||
|enquire_link_interval|Интервал проверки активности соединения.|int ms|0, проверка отключена|O|R||
|server_login|Логин для входящих соединений.<br>**Примечание.** Если значение пусто или не задано, то направление не используется для входящих соединений.|string||O|R||
|server_pwd|Пароль для входящих соединений.|string||C|R||
|server_bind_type_mask|Перечень масок вида соединения. Виды соединения:<br>tx - transmitter, передатчик;<br>rx - receiver, приемник;<br>trx - transceiver, приемопередатчик.|list, string||C|R||
|server_white_hosts|Белый список входящих соединений.<br>**Примечание.** Если список пуст или не задан, то направление не используется для входящих соединений.|regex||C|R||
|**auto_connections**|параметры автосоединений, O/R||
|id|Идентификатор автосоединения.|int||M|R||
|ip|IP–адрес удаленной системы.|ip||M|R||
|port|Порт удаленной системы.|int||M|R||
|bind_type|Вид соединения.<br>tx - transmitter, передатчик;<br>rx - receiver, приемник;<br>trx - transceiver, приемопередатчик.|string||M|R||
|login|Логин удаленной стороны.|string||M|R||
|pwd|Пароль удаленной стороны.|string||M|R||
|DeliverType|Разрешенные типы запросов.<br>deliver/data.|string|deliver|O|R||
|Numbers|Сервисный номер направления.|string||O|R||
|ReceiveAlert|Флаг приема сообщений alert.|bool||O|R||
|Send8Bit|Флаг конвертирования сообщения из 7bit в 8bit для данного SMPP–направления.|bool|0|O|R||
|Send7BitIfUdhAnd8Bit|Флаг конвертирования сообщения с UDH из 8bit в 7bit.|bool|0|O|R||
|USSD_ServiceKey|Перечень префиксов USSD–запросов, которые будут переданы на обработку в данное направление.|list, regex<br>через запятую||O|R||
|USSD_ReserveServiceKey|Перечень масок префиксов USSD–запросов, которые будут переданы на обработку в данное резервное направление.|list, regex<br>через запятую||O|R||
|USSD_ErrorMessage|Переопределение параметра ErrorMessage в разделе USSD файла *gsm.cfg* для данного направления.|string||O|R||
|USSD_WaitApplication<br>Timeout|Переопределение параметра ApplicationTimeout в разделе [USSD] файла *gsm.cfg* для данного направления.|int s||O|R||
|USSD_WaitUserTimeout|Переопределение параметра UserTimeout в разделе [USSD] файла *gsm.cfg* для данного направления.|int s||O|R||
|USSD_StatisticsEnabled|Флаг переопределения параметра StatisticsEnabled в разделе [USSD] файла *gsm.cfg* для данного направления.|bool||O|R||
|USSD_CDR_Enabled|Флаг переопределения параметра CDR_Enabled в разделе [USSD] файла *gsm.cfg* для данного направления.|bool||O|R||
|USSD_Translate7bit|Флаг активации трансляции 7bit сообщений в ASCII и обратно.|bool|1|O|R||
|**[SMS_Routing]**<br>**[SMS_ReserveRouting]**<br>**[MT_SMS_Routing]**<br>**[MT_SMS_ReserveRouting]**|основное направление соединений MO‒SMS.<br>резервное направление соединений MO‒SMS.<br>основное направление соединений MT‒SMS.<br>резервное направление соединений MT‒SMS.|
|Prio|Приоритет маршрута.<br>**Примечание.** Чем больше значение, тем выше приоритет.|int|0|O|R||
|DestInternational|Допустимые номера получателя в формате international.|regex||O|R||
|DestUnknown|Допустимые номера получателя в формате unknown.|regex||O|R||
|DestOther|Флаг обработки в данном направлении номера, не являющегося international или unknown.|bool|0|O|R||
|Source|Допустимые номера отправителя.<br>**Примечание.** Номера должны быть в формате international.|regex||O|R||
|GT|Допустимые номера SMSC.|regex||O|R||
|UseExtendedSelector|Флаг использования расширенного селектора.|bool|0|O|R||
