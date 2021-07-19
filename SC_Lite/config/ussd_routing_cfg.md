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
|<a name="usesimplesearch">UseSimpleSearch</a>|Флаг упрощенного поиска, при котором анализируются только значения MSISDN и SK.|bool||O|R||
|<a name="groupsfilename">GroupsFileName</a>|Имя файла с описанием групп MSISDN.|string||M|R||
|**[Routing]**||
|Direction|Номер направления, указанный в файле smpp.cfg.|int||M|R||
|[Groups](#groups)|Соответствие названий групп и списков USSD-кодов.<br>**Примечание.** При значении \* направление считается направлением по умолчанию для группы.|list, object||O|R||
|[IMSIs](#imsis)|Перечень IMSI и SK, передающихся по указанному направлению.|list, object||O|R||
|<a name="msisdns">MSISDNs</a>|Перечень номеров MSISDN.|list, string||O|R||
|<a name="sks">SKs</a>|Перечень префиксов IMSI и SK, передающихся по указанному направлению.<br>**Примечание.** [Формат](#formatsks) перечня зависит от значения параметра UseSimpleSearch(#usesimplesearch).|list, regex||O|R||

Формат задания <a name="groups">[Groups]</a>:
```
Groups = {
  #groupName = "#ussd;#ussd";
}
```

Формат задания <a name="imsis">[IMSIs]</a>:
```
IMSIs = {
  #imsi = "#ussd;#ussd;";
}
```

Формат задания <a name="formatsks">[SKs]</a>:
* для UseSimpleSearch = 0:
```
SKs = {
  "#ussd;#ussd";
}
```
* для UseSimpleSearch = 1:
```
SKs = {
  "#ussd";"#ussd";
}
```

### Алгоритм поиска направления

Имеются MSISDN, IMSI, ServiceKey.

* если UseSimpleSearch = 1 (упрощенный поиск):
1. Осуществляется поиск направления по значениям [MSISDN](#msisdns) и [SK](#sks).

* если UseSimpleSearch = 0 (полноценный поиск):
1. Извлекается название группы по значению [MSISDN](#msisdns) из файла, указанного в значении [GroupsFileName](#groupsfilename).
2. Осуществляется поиск направления по названию группы и значению [SK](#sks).
3. Если найти направление не удалось, в том числе и по умолчанию (\*), то осуществляется поиск направления по значениям [IMSI](#imsis) и [SK](#sks).
4. Если найти направление не удалось, в том числе и по умолчанию (\*), то осуществляется поиск направления по значению [SK](#sks).

Если после первой попытки найти направление не удалось, или найденное направление является направлением по умолчанию, то процедура повторяется еще один раз, исключив из SK первый символ.
