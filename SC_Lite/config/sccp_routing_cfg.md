---
title : "sccp_routing.cfg"
description : "Файл настройки маршрутизации SCCP"
weight : 3
---
В файле настраиваются параметры маршрутизации SCCP.

Ключ для reload - **sccp_routing.cfg**.

Список разделов:
* **[Blackhole](#blackhole)**
* **[DefaultRouting](#defaultrouting)**
* **[Routing](#routing)**

## Описание параметров
|Name|Description|Type|Default|O/M|P/R|Version|
|:---|:----------|:---|:------|:--|:--|:------|
|**<a name="blackhole">[Blackhole]</a>**||
|GT_AddrDigit|Перечень масок адресов CdPN, чьи сообщения прекращают обрабатываться на уровне SCCP. Формат:<br>{ GT_AddrDigit = "#mask" };|list, regex||O|R||
|**<a name="defaultrouting">[DefaultRouting]</a>**||
|DPC|Перечень кодов DPC.|list, int<br>0-16383||M|R||
|NI|Значение NI для пункта назначения.|int||O|R||
|TT|Значение подмены Translation Type для CdPN.|int|-1|O|R||
|TT_AL|Флаг запрета подмены Translation Type для CdPN.|bool|0|O|R||
|CgPN_RI_set|Флаг подмены Routing Indicator для CgPN во всех исходящих сообщениях.|bool||O|R||
|CdPN_RI_set|Флаг подмены Routing Indicator для CdPN во всех исходящих сообщениях.|bool||O|R||
|RDPC|Код резервного пункта Reserved DPC.<br>**Примечание.** Используется только для SS7.|int<br>0-16383||O|R||
|RNI|Значение NI для резервного пункта назначения.|int||O|R||
|Resend|Флаг повторной отправки сообщения при получении UDTS.|bool|1|O|R||
|**<a name="routing">[Routing]</a>**||
|GT_AddrDigit|Номер GT.|string||M|R||
|DPC|Перечень кодов DPC.|list, int<br>0-16383||M|R||
|NI|Значение NI для пункта назначения.|int||O|R||
|TT|Значение подмены Translation Type для CdPN.|int|-1|O|R||
|TT_AL|Флаг запрета подмены Translation Type для CdPN.|bool|0|O|R||
|CgPN_RI_set|Флаг подмены Routing Indicator для CgPN во всех исходящих сообщениях.|bool||O|R||
|CdPN_RI_set|Флаг подмены Routing Indicator для CdPN во всех исходящих сообщениях.|bool||O|R||
|RDPC|Код резервного пункта Reserved DPC.<br>**Примечание.** Используется только для SS7.|int<br>0-16383||O|R||
|RNI|Значение NI для резервного пункта назначения.|int||O|R||
|Resend|Флаг повторной отправки сообщения при получении UDTS.|bool|1|O|R||

**Примечание.** В первую очередь проверяется совпадение с масками секции [[Blackhole]](#blackhole). Если совпадений нет, то далее проверяются параметры секций [[Routing]](#routing) и [[DefaultRouting]](#defaultrouting).

Первый маршрут имеет наибольший приоритет. При совпадении адреса с масками нескольких маршрутов выбирается тот, что указан раньше в секции [[Routing]](#routing).
