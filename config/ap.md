---
title : "ap.cfg"
description : "Файл настройки подсистемы сбора аварий"
weight : 3
---

В файле настраиваются параметры подсистемы аварийной индикации, SNMP–соединений и правил преобразования компонентных адресов в SNMP–адреса.

**Внимание!** Крайне не рекомендуется менять параметры в этом файле.

Список разделов:
* [General](#general);
* [Dynamic](#dynamic);
* [SNMP](#snmp);
* [StandardMib](#standardmib);
* [AtePath2ObjName](#atepath2objname);
* [SNMPTrap](#snmptrap);
* [Filter](#filter);
* [SpecificTrapCA_Object](#st_ca_object);
* [SpecificTrapCT_Object](#st_ct_object);
* [SpecificTrapCA_Var](#st_ca_var);
* [Logs](#logs).

## Описание параметров
|Name|Description|Type|Default|O/M|P/R|Version|
|:---|:----------|:---|:------|:--|:--|:------|
|**<a name="general" />[General]**||
|Root|Корень дерева.|string|PROTEI(1.3.6.1.4.1.20873)|O|R||
|ApplicationAddress|Адрес приложения.|string|SC_Lite|M|R||
|MaxConnectionCount|Максимальное количество одновременных подключений.|int|10|O|R||
|ManagerThread|Запуск встроенного менеджера в отдельном потоке.|bool|0|O|R||
|CyclicWalkTree|Циклический обход деревьев.|bool|0|O|R||
|**<a name="dynamic" />[Dynamic]**||
|caVar|Компонентный адрес переменной.|string||O|R||
|value|Значение переменной.|string||O|R||
|**<a name="snmp" />[SNMP]**||
|ListenIP|IP–адрес, с которым будет устанавливать соединение система обработки сообщений AlarmProcessor.|ip|0.0.0.0|O|R||
|ListenPort|Прослушиваемый порт.|int 0–65535|161|O|R||
|OwnEnterprise|SNMP–адрес приложения.|string|1.3.6.1.4.1.20873|O|R||
|**<a name="standardmib" />[StandardMib]**||
|addrSNMP|Адрес SNMP для переменной.|string||O|R||
|typeVar|Тип переменной.|string||O|R||
|value|Значение переменной.|string||O|R||
|**<a name="atepath2objname" />[AtePath2ObjName]**||
|ctObject|Компонентный тип объекта.|regex||O|R||
|caVar|Компонентный адрес переменной.|string||O|R||
|**<a name="snmptrap" />[SNMPTrap]**||
|ipManSNMP|IP–адрес SNMP–менеджера.|ip||O|R||
|portManSNMP|Порт SNMP–менеджера.|int 0–65535||O|R||
|caObjFilter|Фильтр по адресу объекта.|regex||O|R||
|ctObjFilter|Фильтр по типу объекта.|regex||O|R||
|caVarFilter|Фильтр по адресу переменной.|regex||O|R||
|**<a name="filter" />[Filter]**||
|CA_Object|Фильтр по адресу объекта.|regex|.*|O|R||
|CT_Object|Фильтр по типу объекта.|regex|.*|O|R||
|CA_Var|Фильтр по адресу переменной.|regex|.*|O|R||
|TrapIndicator|Фильтр по индикатору трапа.|string|1|O|R||
|DynamicIndicator|Фильтр по индикатору динамического объекта.|string|0|O|R||
|**<a name="st_ca_object" />[SpecificTrapCA_Object]**||
|caVar|Компонентный адрес переменной.|string||O|R||
|specificTrapOffset|Смещение в нумерации.|int||O|R||
|**<a name="st_ct_object" />[SpecificTrapCT_Object]**||
|ctObject|Компонентный тип объекта.|regex||O|R||
|specificTrapBase|Число начала нумерации.|int||O|R||
|**<a name="st_ca_var" />[SpecificTrapCA_Var]**||
|caObj|Компонентный адрес объекта.|regex||O|R||
|specificTrapOffset|Смещение в нумерации.|int||O|R||
|**<a name="logs" />[Logs]**||
|TreeTimerPeriod|Период сохранения текущего состояния объектов в логах.|int ms|60000|O|R||
|<a name="filterlevel" />FilterLevel|Правила фильтрации аварий по журналам.|list, object||O|R||
|caObj|Компонентный адрес объекта.|regex||O|R||
|ctObj|Компонентный тип объекта.|regex||O|R||
|caVar|Компонентный адрес переменной.|regex||O|R||
|nLevel|Уровень журнала.|int||O|R||

Формат [Dynamic](#dynamic):<br>
`{ #caVar;#value; };`<br>
Формат [StandardMib](#standardmib):<br>
`{ #addrSNMP;#typeVar;#value; };`<br>
Формат [AtePath2ObjName](#atepath2objname):<br>
`{ #ctObject;#caVar; };`<br>
Формат [SNMPTrap](#snmptrap):<br>
`{ #ipManSNMP;#portManSNMP;#caObjFilter;#ctObjFilter;#caVarFilter; };`<br>
Формат [SpecificTrapCA_Object](#st_ca_object):<br>
`{ #caVar;#specificTrapOffset; }`<br>
Формат [SpecificTrapCT_Object](#st_ct_object):<br>
`{ #ctObject;#specificTrapBase; }`<br>
Формат [SpecificTrapCA_Var](#st_ca_var):<br>
`{ #caObj;#specificTrapOffset; }`<br>
Формат [FilterLevel](#filterlevel):<br>
`{ #caObj;#ctObj;#caVar;#nLevel; }`<br>
