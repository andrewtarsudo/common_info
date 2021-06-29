---
title : "msisdn_groups.txt"
description : "Файл настройки групп MSISDN"
weight : 3
---
В файле настраиваются группы MSISDN и их префиксы.

**Примечание.** Имя задается параметром GroupsFileName в файле ussd_routing.cfg.

Используется во всех версиях.
## Описание параметров
|Name|Description|Type|Default|O/M|P/R|Version|
|:---|:----------|:---|:------|:--|:--|:------|
|nameGroup|Имя группы MSISDN.|string||M|R||
|prefix|Префикс группы MSISDN.|string||M|R||

Формат файла:
```
#nameGroup; #prefix;
#nameGroup; #prefix;
```
