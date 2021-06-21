---
title : "sccp_routing.cfg"
description : "Файл настройки маршрутизации SCCP"
weight : 3
---
В файле настраиваются параметры маршрутизации SCCP.

Ключ для reload - **sccp_routing.cfg**.

Используется во всех версиях.
## Описание параметров
|Name|Description|Type|Default|O/M|P/R|Version|
|:---|:----------|:---|:------|:--|:--|:------|
|**[Routing]**<br>**[DefaultRouting]**||
|DPC|Перечень кодов пунктов назначения DPC.|list, int 0-16383||M|R||
|NI|Идентификатор NI пункта назначения.<br>0 — International network;<br>1 — Spare (for international use only);<br>2 — National network;<br>3 — Reserved for national use.|int||O|R||
|RDPC|Код резервного пункта назначения Reserved DPC. Используется только для SS7.|int 0-16383||O|R||
|RNI|Идентификатор NI резервного пункта назначения.|int||O|R||
|Resend|Флаг повторной отправки сообщения при получении UDTS.|bool|1|O|R||
|GT_AddrDigit|Номер GT. Задается только в **[Routing]**.|string||M|R||
