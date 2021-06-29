---
title : "gsm.cfg"
description : "Файл настройки интерфейса с мобильной сетью"
weight : 3
---
В файле настраиваются параметры взаимодействия с узлами мобильной сети.

Список разделов:
* [General](#general);
* [TrafficManager](#trafficmanager);
* [SMPP_StatusErrors](#smppstatuserrors);
* [SMPP_InternalErrors](#smppinternalerrors);
* [SMSC](#smsc);
* [USSD](#ussd);
* [SMS](#sms);
* [HTTP](#http);
* [LBS](#lbs);
* [Other](#other);
* [SMS_MAP_Version](#smsmapversion);
* [BRT_to_MAP_Errors](#brttomaperrors);
* [MAP_to_BRT_Errors](#maptobrterrors);
* [SMPP_to_BRT_Errors](#smpptobrterrors);
* [SMPP_Status_to_BRT_Errors](#smppstatustobrterrors);
* [SMS_MT_Route](#smsmtroute).

## Описание параметров
|Name|Description|Type|Default|O/M|P/R|Version|
|:---|:----------|:---|:------|:--|:--|:------|
|**<a name="general">[General]</a>**|Ключ для reload -<br>**reload SMS_Routing**||
|ApplicationCode|Код приложения заказчика.|int|0|O|P||
|TPRejectDuplicates|Флаг отбития MO‒SMS, если в сообщении SMPP_submit_sm активирован флаг TP-Reject-Duplicates.|bool|0|O|R||
|GPRS_SupportIndicator|Флаг активации gprsSupportIndicator при кодировании SRI для MT‒SMS.|bool|0|O|R||
|**<a name="trafficmanager">[TrafficManager]</a>**||
|MaxQueueSize|Максимальное допустимое количество примитивов в очереди.|int|600|O|P||
|**<a name="smppstatuserrors">[SMPP_StatusErrors]</a>**||
|SMPP_MAP_Errors_Converter|Правило конвертации ошибок SMPP и SS7. Формат строк:<br>{ #smppErr;#ss7Err }<br>**Примечание.** При smppErr = 0 задается значение ss7Err по умолчанию.|list, object|{ 0; 0xff }|O|R||
|**<a name="smppinternalerrors">[SMPP_InternalErrors]</a>**||
|SMPP_MAP_ErrorsConverter|Правило конвертации внутренних ошибок SMPP и SS7. Формат строк:<br>{ #smppErr;#ss7Err }<br>**Примечание.** При smppErr = 0 задается значение ss7Err по умолчанию.|list, object|{ 0; 0xff }|O|R||
|**<a name="smsc">[SMSC]</a>**|Ключ для reload -<br>**reload SMS_Routing**||
|Handlers|Максимальное количество зарезервированных логик.<br> **Примечание.** Будет выделено в 2 раза больше логик, поскольку инициализируются и для SendSMS, и для остальных.|int|2500|O|P||
|RemoteGT|Адрес GT для SCCP.RemotePA при использовании услуг LBS.|string||O|R||
|Address|Адрес SCCP.LocalPA для транзакций, инициированых SC_Lite, от имени которого коммутатору отправляются запросы на определение местоположения абонента.|string||M|R||
|UseChangeGTinTCAP_BEGIN|Флаг подмены SCCP.LocalPA на Address в сообщениях TCAP_BEGIN_Resp.|bool|0|O|R||
|UseChangeGTinUSSD_TCAP_BEGIN|Флаг подмены SCCP.LocalPA на Address в сообщениях TCAP_BEGIN_Resp для MO‒USSD.|bool|0|O|R||
|AddressRI|Значение RI для Address.<br>**Примечание.** Используется для CheckIMEI, GetLoc, RecvSM, SendSMS, MO_USSD.|int|-1, без замены||O|R||
|AddressSSN|Значение SSN для Address.<br>**Примечание.** Используется для GetLoc, RecvSM, SendSMS, MO_USSD.|int|-1, без замены|O|R||
|IMSI_WhiteList|Разрешенный список префиксов IMSI для IMSI_MSISDN_Converter.|list, string|""|O|R||
|IMSI_MSISDN_Converter|Правила конвертации IMSI в MSISDN.|list, object||O|R||
|MSISDN_IMSI_Converter|Правила конвертации MSISDN в IMSI.|list, object||O|R|| 
|MT_GT_BlackList|Маска для черного списка номеров MSC для MT‒SMS.|regex|""|O|R||
|MAP_ErrorFor_GT_BlackList|Код ошибки MT‒SMS, если MSC находится в черном списке.|int|0|O|R||
|MO_GT_WhiteList|Маска для белого списка номеров MSC для MT‒SMS.|regex|""|O|R||
|MAP_ErrorFor_GT_WhiteList|Код ошибки MO‒SMS, если MSC находится в черном списке.|int|0|O|R||
|**<a name="ussd">[USSD]</a>**|Ключ для reload -<br>**./reload USSD**||
|BlockedSmppDirectionsMT_USSD|Список SMPP-направлений, для которых запрещена отправка MT-USSD.|list, int|не используется|O|R||
|DebugNumbers|Перечень номеров абонентов, которым в случае ошибки отправляется отладочная информация вместо ErrorMessage.|list, regex||O|R||
|TimeServiceNumber|Номер доступа к сервисной службе точного времени.|string|\*060#|O|R||
|TimeServiceEng|Флаг использования английского языка.|bool||O|R||
|TimeServiceZone|Номер доступа к службе информирования о временной зоне.|string|MSK|O|R||
|TimeServiceHeader|Текст перед временем.<br>**Примечание.** Задается в кодировке cp-1251.|string|Московское время:|O|R||
|AdminStatisticService|Номер доступа к сервису статистики работы SC_Lite для номеров DebugNumbers.|string|\*1790#|O|R||
|SimpleTestService|Номер доступа для тестирования приложения.|string|\*555#|O|R||
|InteractiveTestService|Номер доступа к службе тестирования интерактива приложения.|string|\*556#|O|R||
|UnicodeTestService|Номер доступа к приложению, выводящему информацию о поддержке русского языка.|string|\*557#|O|R||
|MaxLenService|Номер доступа к сервисной службе.|string|\*558#|O|R||
|<a name="errormessage">ErrorMessage</a>|Текст сообщение для абонента в случае ошибки работы с внешним приложением.|string|"noBTOPuTe 3anpoc no3>\|<e.<br> Cnacu6o!\nPlease try later. Thank you!"|O|R||
|ErrorMessageRus|Текст сообщения ErrorMessage, записанный кириллическими символами.|string|значение [ErrorMessage](#errormessage)|O|R||
|<a name="directionnotfoundmessage">DirectionNotFoundMessage</a>|Текст сообщения для абонента при отсутствии USSD_ServiceKey во всех направлениях SMPP.<br>**Примечание.** Поддерживаемые кодировки: Unicode и ASCII.|""||O|R||
|DirectionNotFoundMessageRus|Текст сообщения DirectionNotFoundMessage при ответе абоненту кириллическими символами.|string|значение [DirectionNotFoundMessage](#directionnotfoundmessage)|O|R||
|WaitApplicationTimeout|Время ожидания сообщения от внешнего приложения.<br>**Примечание.** По истечении времени сессия завершается.|int s|30|O|R||
|WaitUserTimeout|Время ожидания ответа от абонента для интерактивных сервисов.<br>**Примечание.** По истечении времени сессия завершается.|int s|600|O|R||
|ChopEndline|Флаг удаления последнего символа, если он является переходом на новую строку.|bool|0|O|R||
|USSD_MaxV1_Len|Максимальная количество символов в сессии USSD v1.<br>**Примечание.** При превышении фаза, полученная от приложения, укорачивается до допустимой по границе слова.|int|200|O|R||
|USSD_MaxV2_Len|Максимальная количество символов в ответе абоненту в сессии USSD v2.<br>**Примечание.** При превышении фаза, полученная от приложения, укорачивается до допустимой по границе слова.|int|182|O|R||
|USSD_MaxRus_Len|Максимальное количество кириллических символов в тексте.|int|80|O|R||
|SendMSISDN|Флаг запроса номера MSISDN.|bool|0|O|R||
|E214_PrefixDelete|Количество удаляемых символов при преобразовании номера от стандарта E212 к E214.|int|5|O|R||
|E214_PrefixAdd|Добавляемый префикс при преобразовании номера от стандарта E212 к E 214.|string|781296|O|R||
|USSD_Translate7bit|Флаг трансляции 7-битных сообщений в ASCII.|bool|1|O|R||
|MT_SendOriginationReference|Флаг требования заполнять поле OriginationReference для MT_USSD.|bool|0|O|R||
|StatisticsEnabled|Флаг ведения статистики.|bool|0|O|R||
|StatisticsPeriodLength|Период сброса статистики.|int s|3600|O|R||
|StatLogMO|Имя журнала МО-статистики.|string|statMO_USSD|O|R||
|StatLogMT|Имя журнала МТ-статистики.|string|statMT_USSD|O|R||
|CDR_Enabled|Флаг ведения журналов CDR.|bool|0|O|R||
|CDR_PeriodLength|Период сброса CDR.|int s|60|O|R||
|CDR_LogMO|Имя журнала CDR для MO‒SMS.|string|CDR_MO_USSD|O|R||
|CDR_LogMT|Имя журнала CDR для MT‒SMS.|string|CDR_MТ_USSD|O|R||
|CDR_LogTR2|Имя журнала CDR для TR2_USSD.|string|CDR_TR2_USSD|O|R||
|WriteCDR_LogTR2|Флаг ведения журнал CDR_LogTR2.|bool|0|O|R||
|USSD_Replies|Перечень предопределенных ответов сервисов. Формат:<br>{ #service;#response };<br>**Примечание**. Можно использовать следующие спецсимволы:<br>\ — задает escape–последовательность, следующие за \ символы экранируются;<br># — символ комментария;<br>\\ — обозначение для перехода на следующую строку.|list, object||O|R||
|service|Название сервиса.|string||O|R||
|response|Текст заготовленного ответа.|string||O|R||
|**<a name="sms">[SMS]</a>**|Ключ для reload -<br>**./reload SMS_Routing**||
|DeliverType|Тип отправляемого сообщения. Возможные значения: deliver/data.|string|deliver|O|R||
|Translate7bit|Флаг включения трансляции 7 bit сообщений в ASCII.|bool|1|O|R||
|TruncateMSISDN|Флаг укорачивания MSISDN до 10 символов.|bool|1|O|R||
|TimeZone|Отклонение временной зоны, МАР-TP-Service-Centre-Time-Stam, от времени по Гринвичу.|int|0|O|R||
|SMS_UseBRT|Флаг использования BRT_Interface для всех MO‒SMS.|bool|0|O|R||
|SMS_UseDiameter|Флаг использования тарификации Diameter для всех MO‒SMS.|bool|0|O|R||
|SMS_MT_UseDiameter|Флаг использования тарификации Diameter для всех MT‒SMS.|bool|0|O|R||
|SMS_MAP_MT_UseDiameter|Флаг использования тарификации Diameter для всех MAP‒MT‒SMS-сообщений.|bool|0|O|R||
|SMS_SleepBeforeSend|Задержка перед отправкой MAP‒SM.<br>**Примечание.** Если задано значение вне диапазона, то оно приводится к ближайшему числу в требуемом интервале.|int ms<br>0-10000|0|O|R||
|UseMoreMessagesToSendFlag|Флаг использования More Messages to Send, TP-MMS, для отправки конкантенированных сообщений.|bool|0|O|R||
|**<a name="http">[HTTP]</a>**|Ключ для reload -<br>**./reload SMS_Routing**||
|sessionId|Уникальный идентификатор операции|string||O|P||
|timestamp|Дата и время совершения действия. Формат:<br>согласно ISO 8601-1:2019: YYYY-MM-DD hh:mm:ss|datetime||M|R||
|msisdnA|Номер MSISDN отправителя.|string, не более 15 символов||O|R||
|msisdnB|Номер MSISDN получателя.|string, не более 15 символов||O|R||
|smsBody|Текст SMS-сообщения.|string||O|R||
|smsId|Идентификатор составного SMS-сообщения.|int<br>0-255||O|R||
|partsQty|Общее количество частей в составном SMS-сообщении.|int<br>0-255||O|R||
|partNumber|Идентификатор части составного SMS-сообщения.|int<br>0-255||O|R||
|vlr|Адрес VLR.|string, не более 15 символов||O|R||
|msgType|Источник сообщения.|string|SCL|O|R||
|msgSubType|Вид сообщения.<br>MT - входящее SMS-сообщение;<br>MO - исходящее SMS-сообщение;<br>HR - home routing SMS-сообщение.|string||O|R||
|SpecificDirection|Идентификатор HTTP-направления.|int|-1|O|R||
|ReserveDirection|Индикатор резервного HTTP-направления при недоступности основного.|int||O|R||
|IMSI_WhiteListForSpecificHTTP|Перечень номеров IMSI, которым можно отправлять запросы.|list, regex||O|R||
|SourceBlackList|Перечень отправителей SMS, для которых не посылается запрос на CPE.|list, regex||O|R||
|SpecificSendIfResponseCodeIsNotZero|Индикатор дальнейших действий при получении ResponseCode, отличного от 0.<br>0 - отбой;<br>1 - продолжение обработки.|int||O|R||
|SpecificSendIfError|Индикатор дальнейших действий по истечении времени ожидания или получении сообщения, отличного от HTTP 200 OK.<br>0 - отбой;<br>1 - продолжение обработки.|int||O|R||
|URI|Ссылка на запрос.|string|""|O|R||
|SendIfError|Флаг отправления SMS-сообщения при получении ошибки или срабатывания таймера.|bool|0|O|R||
|SpecificAnsTimeout|Время ожидания ответа по HTTP.|int s||O|R||
|Direction|Номер направления для отправки запроса.|int||O|R||
|DestBlackList|Перечень MSISDN получателей SMS-сообщений, которым не посылается запрос.|list, regex||O|R||
|DestWhiteList|Перечень MSISDN получателей SMS-сообщений, которым посылается запрос.|list, regex||O|R||
|SendAfterDIAM|Флаг отправки http-запросов на подмену CdPN в биллинг после отправки запросов по протоколу Diameter для MO-SMS сообщений.|bool|0|O|R||
|SendGet|Флаг возможности отправки GET-запросов.|bool|1|O|R||
|**<a name="lbs">[LBS]</a>**|Ключ для reload -<br>**./reload lbs**||
|ActiveLocationRequest|Флаг применения запросов ActiveLocationRequest для LOC-сервисов не из списка типичных пользователей.<br>**Примечание.** Используется всегда: LOC4, LOC5, LOC6, LOC8, OJO.|bool|0|O|R||
|GT_HLR_ForATI|Адрес назначения MAP‒ATI для LOC11.|string|1|O|R||
|SetEllipsoidArc|Флаг активации поля MAP_SupportedGADShapes со значением EllipsoidArc при кодировании MAP‒PSL для LOC5.|bool|0|O|R||
|AddSubscriberStateToPsiFor|Флаг заполнения поля e_subscriberState сообщения MAP_RequestedInfo при кодировании сообщения MAP–PSI для заданных в конфигурации LOC*.|bool|0|O|R||
|SendPsiOnErrorFor|Перечень разрешенных адресов для отправления MAP‒PSI при получении TCAP_RETURN_ERROR для MAP‒FSM.|list, string|""|O|R||
|SubscriberStateWhiteListForSRI_GT|Перечень разрешенных адресов для запросов MAP‒SRI‒SM_Resp.<br>**Примечание.** При провале проверки MAP-FSM не отправляются.|list, string|""|O|R||
|SendPSL_ForMSC|Перечень разрешенных адресов для MAP‒ATI_Resp сервиса LOC 9.<br>**Примечание.** При успешной проверке MAP‒FSM не отправляются.|list, string|""|O|R||
|**<a name="other">[Other]</a>**|Ключ для reload -<br>**./reload SMS_Routing**||
|ZTE_GT_CheckIMEI|Перечень масок номеров, обслуживающихся по стандарту ZTE.|regex||O|R||
|UseMT_ForwardingByError|Флаг активации услуги переадресации.|bool|0|O|R||
|FwCauses|Перечень кодов причин для переадресации сообщения.|list, int||O|R||
|AllowedPID_ForHR|Идентификаторы протокола PID, имеющие разрешение отправлять MT‒FSM для HomeRouting.|list, int||O|R||
|GetSMPPDirectionJustBeforeSending|Флаг повторного выбора SMPP-направления для SMS-сообщения в случае модификации номера со стороны биллинга.|bool||O|R||
|DontCheckServiceTypeForSmppDataSM|Флаг отмены проверки параметра service_type для входящих SMS-сообщений.|bool|0|O|R||
|**<a name="smsmapversion">[SMS_MAP_Version]</a>**||
|Default|Версия MAP по умолчанию.|int|1|O|R||
|HLR|Задание версии MAP в зависимости от GT HLR. Формат:<br>Default = #defVer;<br>{<br>&nbsp;&nbsp;GT = "#maskGt";<br>&nbsp;&nbsp;MAP_Version = #version;<br>};|object||O|R||
|Default|Используемая версия MAP по умолчанию.<br>1 - MAPv1;<br>2 - MAPv2;<br>3 - MAPv3.|int||O|R||
|GT|Маска GT для HLR.|regex||O|R||
|MAP_Version|Версия MAP.<br>1 - MAPv1;<br>2 - MAPv2;<br>3 - MAPv3.|int||O|R||
|MSC|Задание версии MAP в зависимости от GT MSC.|object||O|R||
|**<a name="brttomaperrors">[BRT_to_MAP_Errors]</a>**<br><a name="maptobrterrors">**[MAP_to_BRT_Errors]</a>**||
|ErrorsConverter|Правило конвертации внутренних ошибок BRT и SS7. Формат строк:<br>{ #brtErr;#ss7Err }<br>**Примечание.** При brtErr = 0 задается значение ss7Err по умолчанию.|list, object|{ 0; 32 }|O|R||
|**<a name="smpptobrterrors">[SMPP_to_BRT_Errors]</a>**|Ключ для reload -<br>**./reload SMS_Routing**||
|ErrorsConverter|Правило конвертации внутренних ошибок SMPP и BRT. Формат строк:<br>{ #smppErr;#brtErr }<br>**Примечание.** При smppErr = 0 задается значение brtErr по умолчанию.|list, object|{ 0; 0xff }|O|R||
|**<a name="smppstatustobrterrors">[SMPP_Status_to_BRT_Errors]</a>**||
|ErrorsConverter|Правило конвертации статусов SMPP и ошибок BRT. Формат строк:<br>{ #smppStatus;#brtErr }<br>**Примечание.** При smppStatus = 0 задается значение brtErr по умолчанию.|list, object|{ 0; 0xff }|O|R||
|**<a name="smsmtroute">[SMS_MT_Route]</a>**||
|CdPN|Номер получателя SMS-сообщения.|string||O|R||
|IMSI|Маска номера IMSI получателя.|regex||O|R||
|VLR|Адрес VLR.|string||O|R||
|InboundSMPP_dirs|Перечень идентификаторов направления на ядре SMSC.|list, int||O|R||
|DelDigitsFromBegin|Количество цифр, удаляемых с начала номера.|int||O|R||
|SGSN|Адрес SGSN.|string||O|R||
|AddPrefix|Символы, добавляемые к началу номера.|string||O|R||
|BlockWithCommandStatus|Идентификатор статуса команды command_status, при наличии которого SMS-сообщения блокируются.|int||O|R||
|ErrorType|Тип ошибки при блокировке SMS-сообщения, передаваемые в SMSC для настройки обработки SMS-сообщения в сценарии.|int||O|R||
|ErrorCode|Код ошибки при блокировке SMS-сообщения, передаваемые в SMSC для настройки обработки SMS-сообщения в сценарии.|int||O|R||
