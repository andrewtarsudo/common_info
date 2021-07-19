---
title : "diam.cfg"
description : "Файл настройки порогов аварийной индикации"
weight : 3
---

В файле настраиваются параметры взаимодействия по протоколу Diameter.

Ключ для reload - **reload diam.cfg**.

Список разделов:
* **[General](#general)**
* **[ATSI](#atsi)**
* **[MT_SMS_Diameter](#mtsmsdiameter)**
* **[DiameterError](#diametererror)**
* **[SMS_MSC](#smsmsc)**
* **[MSISDN_WhiteList](#msisdnwhitelist)**
* **[Route](#route)**
* **[NumberConvertation](#numberconvertation)**
* **[Scenarios](#scenarios)**
* **[AVP_Values](#avpvalues)**
* **[ATI](#ati)**
* **[Other](#other)**


## Описание параметров
|Name|Description|Type|Default|O/M|P/R|Version|
|:---|:----------|:---|:------|:--|:--|:------|
|**<a name="general">[General]** ||
|[ApplicationCode](#applicationcode)|Код приложения.|int||M|R||
|**<a name="atsi">[ATSI]** ||
|SendATSI|Флаг отправки сообщения MAP‒ATSI.|bool|0|O|R||
|RemoteGT|Адрес gsmSCF_Address при отправке MAP‒ATSI.|string|не используется|O|R||
|MSISDN_ATSI_List|Маски номеров для отправки MAP‒ATSI.|regex|не используется|O|R||
|**<a name="mtsmsdiameter">[MT_SMS_Diameter]** ||
|ScrList|Маски номеров отправителей, для которых необходимо осуществлять MT–тарификацию.|regex||O|R||
|DstList|Маски номеров получателей, для которых необходимо осуществлять MT–тарификацию.|regex||O|R||
|ImsiList|Маски IMSI, для которых необходимо осуществлять MT–тарификацию.|regex||O|R||
|SrcBlackList|Черный список масок номеров отправителей, для которых не надо осуществлять MT–тарификацию.|regex||O|R||
|**<a name="diametererror">[DiameterError]** ||
|[SendSMS](#sendsms)|Код действия после получения ошибки со стороны биллинга во время обработки SMS–сообщения.|int|0|O|R||
|[SendMAP_MT_SMS](#sendmapmtsms)|Код действия после получения ошибки со стороны биллинга во время обработки MAP‒MT‒SMS–сообщения.|int|0|O|R||
|AllowedErrorCodesForMT|Список кодов ответа от биллинга для МТ, при которых нужно перейти на работу по сценарию.|string||O|R||
|AllowedErrorCodesForMO|Список кодов ответа от биллинга для МO, при которых нужно перейти на работу по сценарию.|string||O|R||
|AllowedErrorCodesFor<br>MAP_MT|Список кодов ответа от биллинга для Home Rerouting, при которых нужно перейти на работу по сценарию.|string||O|R||
|**<a name="smsmsc">[SMS_MSC]** ||
|MSC_List|MSC номера, с которых не будут осуществляться запросы по протоколу Diameter.|regex||O|R||
|**<a name="msisdnwhitelist">[MSISDN_WhiteList]** ||
|MSISDN_List|Белый список номеров MSISDN отправителей, которым разрешено отправлять SMS–сообщения.|list, regex||O|R||
|**<a name="route">[Route]**|параметры маршрутизации||
|IMSI|Маски IMSI, для которых применяется правило.|regex||M|R||
|MSISDN|Маски MSISDN, для которых применяется правило.|regex||O|R||
|Dest|Адрес GT SCF–Address, полученный в ответ на сообщение MAP‒ATSI.|string|не используется|O|R||
|Host|Перечень Host_Identity из файла DIAM.cfg.|list, int||O|R||
|[UseCA](#usecavalues)|Способ выбора Diameter–подключения.|int|0|O|R||
|CA|Перечень PCSM из файла DIAM.cfg.<br>**Примечание.** Обязателен, только если UseCA = 1.|list, string||C|R||
|LoadSharing|Флаг использования режим распределенной нагрузки LoadSharing|bool|0|O|R||
|MaxErrorCount|Максимальное количество ошибок в процессе обращения к биллингу до прекращения отправки запросов в данном направлении.|int|1|O|R||
|BreakDownTimeout|Время ожидания при превышении порога ошибок Diameter.|int ms|30000|O|R||
|**<a name="numberconvertation">[NumberConvertation]**|параметры подмены номеров||
|AddTonNpi|Флаг добавления TON и NPI при отправке запросов Diameter.|bool|1|O|R||
|CheckWithTonNpi|Флаг анализирования правила для TON и Number.|bool|1|O|R||
|Numbers|Набор параметров, определяющих работу секции.|list, object||O|R||
|Number|Маска номера получателя.|regex||O|R||
|TON|Перечень подходящих типов нумерации TON.|list, int|0|O|R||
|NPI|Перечень подходящих планов нумерации NPI.|list, int|0|O|R||
|Delete|Количество цифр, удаляемых из начала номера слева направо.|int|0|O|R||
|Insert|Префикс, добавляемый в начало номера слева.|string|""|O|R||
|NewTON|Новый TON, задаваемый номеру.|int|–1, не менять|O|R||
|NewNPI|Новый NPI, задаваемый номеру.|int|–1, не менять|O|R||
|UseDiameter|Флаг отправки запроса по протоколу Diameter для данного правила.|bool||O|R||
|**<a name="scenarios">[Scenarios]**|параметры сценариев работы||
|[Type](#type)|Вид SMS.|string||O|R||
|MSISDN|Маска номеров отправителей.|regex||O|R||
|ScenarioID|Уникальный идентификатор сценария.|int||O|R||
|MSC_GT|Маска GT центра MSC.|regex||O|R||
|DestAddr|Маска номеров получателей.|regex||O|R||
|Possible|Флаг разрешения отправки SMS–сообщений.|bool||O|R||
|Priority|Приоритет сценария.|int||O|R||
|DTON|TON назначения.|int||O|R||
|UseDiameter|Флаг отправки запроса по протоколу Diameter для тарификации в рамках данного сценария.|bool||O|R||
|SendIfError|Флаг продолжения обработки SMS при истечении времени ожидания ответа от биллинг–центра.|bool|0|O|R||
|IMSI|Маски IMSI, для которых выполняются проверки.|regex||O|R||
|UseDiameterIfOutOfScenariosMO|Флаг отправки запросов по протоколу Diameter, если MO‒SMS‒сообщения не попадают ни под один сценарий.|bool|1|O|R||
|PossibleIfOutofScenariosMO|Флаг разрешения отправки запросов, если MO‒SMS–сообщения не попадают ни под один сценарий.|bool|1|O|R||
|SendIfErrorIfOutOfScenariosMO|Флаг отправки сообщения об ошибке, если MO‒SMS–сообщения не попадают ни под один сценарий.|bool|0|O|R||
|UseDiameterIfOutOfScenariosMT|Флаг отправки запросов по протоколу Diameter, если MT‒SMS–сообщения не попадают ни под один сценарий.|bool|1|O|R||
|PossibleIfOutOfScenariosMT|Флаг разрешения отправки запросов, если MT‒SMS–сообщения не попадают ни под один сценарий.|bool|1|O|R||
|SendIfErrorIfOutOfScenariosMT|Флаг отправки сообщения об ошибке, если MT‒SMS–сообщения не попадают ни под один сценарий.|bool|0|O|R||
|UseDiameterIfOutOf<br>ScenariosMAP_MT|Флаг отправки запросов по протоколу Diameter, если MAP‒MT‒SMS–сообщения не попадают ни под один сценарий.|bool|1|O|R||
|PossibleIfOutOf<br>ScenariosMAP_MT|Флаг разрешения отправки запросов, если MAP‒MT‒SMS–сообщения не попадают ни под один сценарий.|bool|1|O|R||
|SendIfErrorIfOutOf<br>ScenariosMAP_MT|Флаг отправки сообщения об ошибке, если MAP‒MT‒SMS–сообщения не попадают ни под один сценарий.|bool|0|O|R||
|**<a name="avpvalues">[AVP_Values]**||
|Origin-Host|Значение AVP для параметра Origin–Host.|string||M|R||
|Origin-Realm|Значение AVP для параметра Origin–Realm.|string||M|R||
|DestinationHost|Значение AVP для параметра DestinationHost.|string||M|R||
|DestinationRealm|Значение AVP для параметра DestinationRealm.|string||M|R||
|ServiceContextID|Значение AVP для параметра ServiceContextID.|string||M|R||
|**<a name="ati">[ATI]**||
|SendATI|Флаг разрешения отправки запроса MAP‒ATI.|bool||O|R||
|RemoteGT|Адрес SCCP CdPA.|string||O|R||
|**<a name="other">[Other]**||
|SendZeroedIMSI|Флаг отправки IMSI, состоящего из нулей, на узел OCS.|bool|1|O|R||
  
**Примечание.** Содержимое MAP‒ATSI_Resp:
* GT, отсутствующий в [Route] - тарификация не ведется, сообщение регистрируется;
* ошибка informationNotAvailable (62) - тарификация не ведется, сообщение регистрируется;
* любая другая ошибка - тарификация не ведется, сообщение отбивается.

### **<a name="applicationcode">ApplicationCode</a>**
Возможные значения:
* 0 - CODE_MOTIV;
* 1 - CODE_ORGA;
* 2 - CODE_GLOBAL;
* 3 - CODE_SITRONICS;
* 4 - CODE_REDKNEE;
* 5 - CODE_REDKNEE_2;
* 6 - CODE_NURTELECOM;
* 7 - CODE_MTT;
* 8 - CODE_SPRINT;
* 9 - CODE_MEGAFON;
* 10 - CODE_TINKOFF;
* 11 - CODE_PETER_SERVICE.

### <a name="sendsms">SendSMS</a>
Возможные значения:
* 0 - отбивать SMS;
* 1 - передавать SMS дальше.

### <a name="sendmapmtsms">SendMAP_MT_SMS</a>
Возможные значения:
* 0 - отбивать MAP‒MT‒SMS;
* 1 - передавать MAP‒MT‒SMS дальше.

### <a name="useca">UseCA</a>
Возможные значения:
* 0 - используются Host–Identity;
* 1 - используются CA.

### <a name="type">Type</a>
Возможные значения:
* MO - MO‒SMS;
* MT - MT‒SMS;
* MAP_MT - SMS, полученное в роуминге.
