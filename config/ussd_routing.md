---
title : "ussd_routing.cfg"
description : "Файл настройки маршрутизации USSD"
weight : 3
---

В файле настраиваются параметры маршрутизации USSD.

Для использования необходимо, чтобы в файле gsm.cfg было задано ApplicationCode = 9

Ключ для reload - **reload ussd_routing.cfg**.

## Описание параметров
|Name|Description|Type|Default|O/M|P/R|Version|
|:---|:----------|:---|:------|:--|:--|:------|
|**[General]**||
|GroupsFileName|Имя файла с описанием групп MSISDN.|string||M|R||
|**[Routing]**||
|Direction|Номер направления, указанный в файле smpp.cfg.|int||M|R||
|[Groups](#groups)|Перечень префиксов MSISDN, закрепленные за группами абонентов.|list, object||O|R||
|[IMSIs](#imsis)|Перечень IMSI и SK, передающихся по указанному направлению.|list, object||O|R||
|[SKs](#sks)|Перечень префиксов IMSI и SK, передающихся по указанному направлению.|list, regex||O|R||


Формат задания <a name="groups" />[Groups]:
```
Groups = {
  #groupName = "#msisdnPrefix";
}
```
Формат задания <a name="imsis" />[IMSIs]:
```
IMSIs = {
  #imsi = "#sk1;#skN" ;
}
```
Формат задания <a name="sks" />[SKs]:
```
SKs = { "#imsiPrefix"; "#sk" }
```
