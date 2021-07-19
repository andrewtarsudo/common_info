---
title : "msisdn_groups.txt"
description : "Файл настройки групп MSISDN"
weight : 3
---
В файле настраиваются группы MSISDN и их префиксы.

**Примечание.** Имя задается параметром GroupsFileName в файле <a href="/Protei_SCL/docs/common/config/ussd_routing_cfg.md/#groupsfilename">[ussd_routing.cfg]</a>.

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
