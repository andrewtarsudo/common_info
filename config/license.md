---
title : "license.cfg"
description : "Файл настройки лицензии"
weight : 3
---

В файле настраиваются параметры лицензии.

Ключ для reload - **reload license.cfg**.

## Описание параметров
|Name|Description|Type|Default|O/M|P/R|Version|
|:---|:----------|:---|:------|:--|:--|:------|
|**[License]**||
|USSD|Флаг использования USSD–сообщений.|bool|0|O|R||
|SMS|Флаг использования SMS–сообщений.|bool|1|O|R||
|MT|Флаг использования MT‒SMS сообщений.|bool|0|O|R||
|LBS|Флаг использования функциональности LBS.|bool|0|O|R||
|VLR|Флаг использования функциональности LBS (запрос VLR).|bool|0|O|R||
|BRT|Флаг использования функциональности BRT.|bool|0|O|R||
|Diameter|Флаг использования Diameter для тарификации.|bool|0|O|R||
|ZTE|Флаг использования функциональности ZTE.|bool|0|O|R||
|Statistics|Флаг ведения статистики.|bool|0|O|R||
|USSD_Statistics|Флаг ведения USSD–статистики.|bool|0|O|R||
|SMS_Forward|Флаг пересылки MO‒SMS.|bool|0|O|R||
|TrafficNominal|Количество транзакций в секунду, обрабатываемое в штатном режиме.|int<br>1–1000|40|O|R||
|TrafficTresholdInterval|Время обработки всех вызовов в режиме TrafficCriticalThreshold.|int s<br>1–3600|600|O|R||
|TrafficThreshold|Количество транзакций в секунду, обрабатываемое после истечения TrafficThresholdInterval.|int TrafficNominal–TrafficCriticalThreshold|1.1\*TrafficNominal|O|R||
|TrafficCriticalThreshold|Количество транзакций в секунду, обрабатываемое свыше TrafficNominal в течении времени TrafficThresholdInterval после превышения.|int TrafficNominal–2\*TrafficNominal|1.2\*TrafficNominal|O|R||
|TrafficCriticalInterval|Время обработки TrafficThreshold свыше TrafficNominal после превышения TrafficCriticalThreshold.|int s<br>1–3600|0|O|R||
