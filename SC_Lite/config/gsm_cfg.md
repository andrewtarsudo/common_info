---
title : "gsm.cfg"
description : "Файл настройки интерфейса с мобильной сетью"
weight : 3
---
В файле настраиваются параметры взаимодействия с узлами мобильной сети.

Список разделов:
* **[General](#general)**
* **[TrafficManager](#trafficmanager)**
* **[SMSC](#smsc)**
* **[SMS](#sms)**
* **[CheckIMEI](#checkimei)**
* **[SRI](#sri)**
* **[Timers](#timers)**
* **[SMS_MT_Route](#smsmtroute)**
* **[CDR](#cdr)**
* **[MSC_GT](#mscgt)**
* **[SriRouting](#srirouting)**
* **[SMPP_StatusErrors](#smppstatuserrors)**
* **[SMPP_DeliveryFailureCause](#smppdeliveryfailurecause)**
* **[MAP_to_DiameterErrors](#maptodiametererrors)**
* **[HTTP](#http)**
  * **[MO](#mo)**
  * **[MT](#mt)**
  * **[RA](#ra)**
* **[LBS](#lbs)**
* **[SOAP_LOCATION](#soaplocation)**
* **[USSD](#ussd)**
* **[Other](#other)**
* **[SMS_MAP_Version](#smsmapversion)**
* **[BRT_to_MAP_Errors](#brttomaperrors)**
* **[MAP_to_BRT_Errors](#maptobrterrors)**
* **[SMPP_to_BRT_Errors](#smpptobrterrors)**
* **[SMPP_Status_to_BRT_Errors](#smppstatustobrterrors)**
* **[SMPP_InternalErrors](#smppinternalerrors)**
* **[NumberConvertation](#numberconvertation)**

## Описание параметров
|Name|Description|Type|Default|O/M|P/R|Version|
|:---|:----------|:---|:------|:--|:--|:------|
|**<a name="general">[General]</a>**|Ключ для reload -<br>**reload SMS_Routing**||
|[ApplicationCode](#applicationcode)|Код приложения заказчика.|int|0|O|P||
|TPRejectDuplicates|Флаг отбития MO‒SMS, если в сообщении SMPP_submit_sm активирован флаг TP-Reject-Duplicates.|bool|0|O|R||
|CoreCount|Количество ядер, выделяемых на обработку.|int||M|P||
|GPRS_SupportIndicator|Флаг активации gprsSupportIndicator при кодировании SRI для MT‒SMS.|bool|0|O|R||
|**<a name="trafficmanager">[TrafficManager]</a>**||
|MaxQueueSize|Максимальное допустимое количество примитивов в очереди.|int|600|O|P||
|**<a name="smsc">[SMSC]</a>**|Ключ для reload -<br>**reload SMS_Routing**||
|Handlers|Максимальное количество зарезервированных логик.<br> **Примечание.** Будет выделено в 2 раза больше логик, поскольку инициализируются и для SendSMS, и для остальных.|int|2500|O|P||
|SendSMS_Handlers|Максимальное количество логик, обрабатывающих SendSMS.|int|2500|O|P||
|RemoteGT|Адрес GT для SCCP.RemotePA при использовании услуг LBS.|string||O|R||
|Address|Адрес SCCP.LocalPA для транзакций, инициированых SC_Lite, от имени которого коммутатору отправляются запросы на определение местоположения абонента.|string||M|R||
|[UseChangeGTinTCAP_BEGIN](#usechangegtintcapbegin)|Флаг подмены SCCP.LocalPA на Address в сообщениях TCAP_BEGIN_Resp.|bool|0|O|R||
|UseChangeGTinUSSD_TCAP_BEGIN|Флаг подмены SCCP.LocalPA на Address в сообщениях TCAP_BEGIN_Resp для MO‒USSD.|bool|0|O|R||
|[AddressRI](#addressri)|Значение RI для Address.|int|-1, без замены|O|R||
|[AddressSSN](#addressssn)|Значение SSN для Address.|int|-1, без замены|O|R||
|IMSI_WhiteList|Разрешенный список префиксов IMSI для IMSI_MSISDN_Converter.|list, string|""|O|R||
|WhiteListPrefix|Префикс, добавляемый к номерам из белого списка.|string||O|R||
|IMSI_MSISDN_Converter|Правила конвертации IMSI в MSISDN. Формат:<br>{ "#msisdn"; "#imsi" };|list, string||O|R||
|MT_GT_BlackList|Маска для черного списка номеров MSC для MT‒SMS.|regex|""|O|R||
|MAP_ErrorFor_GT_BlackList|Код ошибки MT‒SMS, если MSC находится в черном списке.|int|0|O|R||
|MO_GT_WhiteList|Маска для белого списка номеров MSC для MT‒SMS.|regex|""|O|R||
|MAP_ErrorFor_GT_WhiteList|Код ошибки MO‒SMS, если MSC находится в черном списке.|int|0|O|R||
|ZTE_GT_CheckIMEI|Перечень масок MSC, для которых некоторые поля MAP-CheckIMEI обрабатываются по стандарту ZTE.|regex||O|R||
|**<a name="sms">[SMS]</a>**|Ключ для reload -<br>**./reload SMS_Routing**||
|DeliverType|Тип отправляемого сообщения. Возможные значения: deliver/data.|string|deliver|O|R||
|Translate7bit|Флаг включения трансляции 7 bit сообщений в ASCII.|bool|1|O|R||
|TruncateMSISDN|Флаг укорачивания MSISDN до 10 символов.|bool|1|O|R||
|TimeZone|Отклонение временной зоны, МАР-TP-Service-Centre-Time-Stamp, от времени по Гринвичу.|int|0|O|R||
|SMS_UseBRT|Флаг использования BRT_Interface для всех MO‒SMS.|bool|0|O|R||
|SMS_UseDiameter|Флаг использования тарификации Diameter для всех MO‒SMS.|bool|0|O|R||
|SMS_MT_UseDiameter|Флаг использования тарификации Diameter для всех MT‒SMS.|bool|0|O|R||
|SMS_MAP_MT_UseDiameter|Флаг использования тарификации Diameter для всех MAP‒MT‒SMS-сообщений.|bool|0|O|R||
|SMS_SleepBeforeSend|Задержка перед отправкой MAP‒SM.<br>**Примечание.** Если задано значение вне диапазона, то оно приводится к ближайшему числу в требуемом интервале.|int ms<br>0-10000|0|O|R||
|UseMoreMessagesToSendFlag|Флаг использования TP-More-Messages-to Send для отправки конкантенированных сообщений.|bool|0|O|R||
|UseZTE|Флаг обработки сообщений по стандарту ZTE.|bool|0|O|R||
|SMS_PrefixForZTE|Префикс номеров, чьи сообщения обрабатываются по стандарту ZTE.|string||O|R||
|WaitSMS_Resp|Время ожидания ответа.|int ms|150&thinsp;000|O|R||
|UseMROS|Флаг ведения подробных записей.|bool|0|O|R||
|UseMROS_MT|Флаг ведения подробных записей MAP-MT-SMS.|bool|0|O|R||
|RouteMtSmsByImsi|Флаг использования маршрутизации MAP-MT-SMS по номеру IMSI.|bool|0|O|R||
|**<a name="checkimei">[CheckIMEI]</a>**||
|SmppDirForDataSM|Идентификатор направления для сообщений SMPP_data_sm. при получении сообщения MAP-CheckIMEI.|int||O|R||
|**<a name="sri">[SRI]</a>**||
|HomeRoutingAddress|Адрес для сообщений MAP-SRI Home Routing.|ip||O|R||
|HomeRoutingNAI|Значение NAI для сообщений MAP-SRI Home Routing.|int|4|O|R||
|HomeRoutingNON|Значение Nature of the Number для сообщений MAP-SRI Home Routing.|int|1|O|R||
|UseCacheSRI|Флаг использования кэша данных получателя для сообщения MAP-SRI-FSM.|int|0|O|R||
|CacheInterval|Время хранения кэша данных.|int ms|120|O|R||
|**<a name="timers">[Timers]</a>**|
|MO_WaitNextPartTimeout|Время ожидания следующей части конкатенированного сообщения.|int ms|30&thinsp;000|O|R||
|**<a name="smsmtroute">[SMS_MT_Route]</a>**||
||**<a name="mo">[MO]</a>**||
|Direction|Номер направления для отправки запроса.|int||O|R||
|SendGet|Флаг возможности отправки GET-запросов.|bool|1|O|R||
|SendAfterDIAM|Флаг отправки http-запросов на подмену CdPN в биллинг после отправки запросов по протоколу Diameter для MO-SMS сообщений.|bool|0|O|R||
|URI|Ссылка на запрос.|string|""|O|R||
|SendIfError|Флаг отправления SMS-сообщения при получении ошибки или срабатывания таймера.|bool|0|O|R||
|DestBlackList|Перечень MSISDN получателей SMS-сообщений, которым не посылается запрос.|list, regex||O|R||
|DestWhiteList|Перечень MSISDN получателей SMS-сообщений, которым посылается запрос.|list, regex||O|R||
|SrcWhiteList|Перечень отправителей SMS, которым посылается запрос.|list, regex||O|R||
|SpecificDirection|Идентификатор HTTP-направления.|int|-1|O|R||
|SpecificURI|Ссылка на HTTP-запрос.|string|""|O|R||
|[SpecificSendIfError](#specificsendiferror)|Индикатор дальнейших действий по истечении времени ожидания или получении сообщения, отличного от HTTP 200 OK.|int||O|R||
|[SpecificSendIfResponseCodeIsNotZero](#specificsendifresponsecodeisnotzero)|Индикатор дальнейших действий при получении ответа с кодом ResponseCode, отличным от 0.|int||O|R||
||**<a name="mt">[MT]</a>**||
|Direction|Номер направления для отправки запроса.|int||O|R||
|ReserveDirection|Индикатор резервного HTTP-направления при недоступности основного.|int||O|R||
|SendGet|Флаг возможности отправки GET-запросов.|bool|1|O|R||
|URI|Ссылка на запрос.|string|""|O|R||
|SendIfError|Флаг отправления SMS-сообщения при получении ошибки или срабатывания таймера.|bool|0|O|R||
|SourceBlackList|Перечень отправителей SMS, для которых не посылается запрос на CPE.|list, regex||O|R||
|SourceBlackList|Перечень отправителей SMS, которым посылается запрос на CPE.|list, regex||O|R||
|SpecificDirection|Идентификатор HTTP-направления.|int|-1|O|R||
|SpecificURI|Ссылка на HTTP-запрос.|string|""|O|R||
|[SpecificSendIfError](#specificsendiferror)|Индикатор дальнейших действий по истечении времени ожидания или получении сообщения, отличного от HTTP 200 OK.|int||O|R||
|[SpecificSendIfResponseCodeIsNotZero](#specificsendifresponsecodeisnotzero)|Индикатор дальнейших действий при получении ответа с кодом ResponseCode, отличным от 0.|int||O|R||
|IMSI_WhiteListForSpecificHTTP|Перечень номеров IMSI, которым можно отправлять запросы.|list, regex||O|R||
||**<a name="ra">[RA]</a>**|обработка сообщения MAP-Alert-Service-Centre||
|Direction|Номер направления для отправки запроса.|int||O|R||
|ReserveDirection|Индикатор резервного HTTP-направления при недоступности основного.|int||O|R||
|URI|Ссылка на запрос.|string|""|O|R||
|**<a name="cdr">[CDR]</a>**|
|WriteMessageText|Флаг записи текста сообщения в журнал CDR.|bool||O|R||
|WriteMessageTextMT|флаг записи текста MT-сообщения в журнал CDR.|bool||O|R||
|**<a name="mscgt">[MSC_GT]</a>**|
|SMS_Continue|Перечень адресов MSC для SRI, при указании которых SMS-сообщение от SMSC, с активированным специальным флагом.|list, string||O|R||
|**<a name="srirouting">[SRI_Routing]</a>**|
|GT|Номер SCCP.CdPN, используемый для подмены в сообщениях MAP-SRI-SM.|regex||O|R||
|List|Маска номеров получателя.|regex||O|R||
|MSISDN|Маска номеров MSISDN отправителя.|regex||O|R||
|**<a name="smppstatuserrors">[SMPP_StatusErrors]</a>**||
|SMPP_MAP_ErrorsConverter|Правило конвертации ошибок SMPP и SS7. Формат строк:<br>{ #smppErr; #ss7Err; };<br>**Примечание.** При smppErr = 0 задается значение по умолчанию ss7Err = 0xff.|list, string|{};|O|R||
|**<a name="smppdeliveryfailurecause">[SMPP_DeliveryFailureCause]</a>**||
|SMPP_MAP_ErrorsConverter|Правило конвертации ошибок SMPP в SM-EnumeratedDelivery-Failure-Cause для SM-Delivery-Failure. Формат строк:<br>{ #err; #ss7Err; };|list, string|{};|O|R||
|**<a name="maptodiametererrors">[MAP_to_DiameterErrors]</a>**||
|ErrorsConverter|Параметры конвертации ошибок SS7 и Diameter. Формат строк:<br>{ #ss7Err; #diamErr; };|list, string|{};|O|R||
|**<a name="http">[HTTP]</a>**|Ключ для reload -<br>**./reload SMS_Routing**||
|sessionId|Уникальный идентификатор операции.|string||O|P||
|timestamp|Дата и время совершения действия. Формат: согласно ISO 8601-1:2019:<br>YYYY-MM-DD hh:mm:ss|datetime||M|R||
|msisdnA|Номер MSISDN отправителя.|string, не более 15 символов||O|R||
|msisdnB|Номер MSISDN получателя.|string, не более 15 символов||O|R||
|smsBody|Текст SMS-сообщения.|string||O|R||
|smsId|Идентификатор составного SMS-сообщения.|int<br>0-255||O|R||
|partsQty|Общее количество частей в составном SMS-сообщении.|int<b0r>0-255||O|R||
|partNumber|Идентификатор части составного SMS-сообщения.|int<br>0-255||O|R||
|vlr|Адрес VLR.|string, не более 15 символов||O|R||
|msgType|Источник сообщения.|string|SCL|O|R||
|msgSubType|Вид сообщения.|string||O|R||
|SpecificDirection|Идентификатор HTTP-направления.|int|-1|O|R||
|ReserveDirection|Индикатор резервного HTTP-направления при недоступности основного.|int||O|R||
|IMSI_WhiteListForSpecificHTTP|Перечень номеров IMSI, которым можно отправлять запросы.|list, regex||O|R||
|SourceBlackList|Перечень отправителей SMS-сообщений, для которых не посылается запрос на CPE.|list, regex||O|R||
|SendIfError|Флаг отправления SMS-сообщения при получении ошибки или срабатывания таймера.|bool|0|O|R||
|SpecificAnsTimeout|Время ожидания ответа по HTTP.|int s||O|R||
|Direction|Номер направления для отправки запроса.|int||O|R||
|DestBlackList|Перечень MSISDN получателей SMS-сообщений, которым не посылается запрос.|list, regex||O|R||
|DestWhiteList|Перечень MSISDN получателей SMS-сообщений, которым посылается запрос.|list, regex||O|R||
|SendGet|Флаг возможности отправки GET-запросов.|bool|1|O|R||
|**<a name="lbs">[LBS]</a>**|Ключ для reload -<br>**./reload lbs**||
|ActiveLocationRequest|Флаг применения запросов ActiveLocationRequest для LOC-сервисов не из списка типичных пользователей.<br>**Примечание.** Используется всегда: LOC4, LOC5, LOC6, LOC8, OJO.|bool|0|O|R||
|GT_HLR_ForATI|Адрес назначения MAP‒ATI для LOC11.|string|1|O|R||
|TP_OA_FSM|Значение Originating-Address, подставляемое в запросы MAP-FSM в рамках обработки сервисов LOC6 и OJO.|string|""|O|R|6.2.48+|
|SetEllipsoidArc|Флаг активации поля MAP_SupportedGADShapes со значением EllipsoidArc при кодировании MAP‒PSL для LOC5.|bool|0|O|R||
|AddSubscriberStateToPsiFor|Перечень услуг LBS, для которых заполняется поле SubscriberState в сообщения MAP–PSI.|list, string|""|O|R||
|SendPsiOnErrorFor|Перечень разрешенных адресов для отправления MAP‒PSI при получении TCAP_RETURN_ERROR для MAP‒FSM.|list, string|""|O|R||
|SubscriberStateWhiteListForSRI_GT|Перечень разрешенных адресов для запросов MAP‒SRI‒SM_Resp.<br>**Примечание.** При провале проверки MAP-FSM не отправляются.|list, string|""|O|R||
|SendPSL_ForMSC|Перечень разрешенных адресов для MAP‒ATI_Resp сервиса LOC 9.<br>**Примечание.** При успешной проверке MAP‒FSM не отправляются.|list, string|""|O|R||
|**<a name="soaplocation">[SOAP_LOCATION]</a>**|
|SoapDirection|Идентификатор SOAP-направления.|int||O|R||
|SoapURI|Ссылка SOAP на запрос.|string||O|R||
|ApplicationCode|Код SOAP для приложения заказчика.|int||O|R||
|ApplicationUserName|Имя приложения.|string||O|R||
|**<a name="ussd">[USSD]</a>**|Ключ для reload -<br>**./reload USSD**||
|UseForward|Флаг отправки USSD-сообщений.|bool|1|O|R||
|DecodeStartupNotification|Флаг проверки декодирования USSD-сообщений.|bool|1|O|R||
|BlockedSmppDirectionsMT_USSD|Список SMPP-направлений, для которых запрещена отправка MT-USSD.|list, int|не используется|O|R||
|DebugNumbers|Перечень номеров абонентов, которым в случае ошибки отправляется отладочная информация вместо ErrorMessage.|list, regex||O|R||
|TimeServiceNumber|Номер доступа к сервисной службе точного времени.|string|\*060#|O|R||
|UseBRT|Флаг использования BRT_Interface для всех MO USSD.|bool|0|O|R||
|TimeServiceEng|Флаг использования английского языка.|bool||O|R||
|TimeServiceZone|Номер доступа к службе информирования о временной зоне.|string|MSK|O|R||
|TimeServiceHeader|Текст перед временем.<br>**Примечание.** Задается в кодировке cp-1251.|string|Московское время:|O|R||
|AdminStatisticService|Номер доступа к сервису статистики работы SC_Lite для номеров DebugNumbers.|string|\*1790#|O|R||
|SimpleTestService|Номер доступа для тестирования приложения.|string|\*555#|O|R||
|InteractiveTestService|Номер доступа к службе тестирования интерактива приложения.|string|\*556#|O|R||
|UnicodeTestService|Номер доступа к приложению, выводящему информацию о поддержке русского языка.|string|\*557#|O|R||
|MaxLenService|Номер доступа к сервисной службе.|string|\*558#|O|R||
|<a name="errormessage">ErrorMessage</a>|Текст сообщение для абонента в случае ошибки работы с внешним приложением.|string|noBTOPuTe 3anpoc no3>\|<e.<br> Cnacu6o!\nPlease try later. Thank you!|O|R||
|ErrorMessageRus|Текст сообщения ErrorMessage, записанный кириллическими символами.|string|значение [ErrorMessage](#errormessage)|O|R||
|<a name="directionnotfoundmessage">DirectionNotFoundMessage</a>|Текст сообщения для абонента при отсутствии USSD_ServiceKey во всех направлениях SMPP.<br>**Примечание.** Поддерживаемые кодировки: Unicode и ASCII.|""||O|R||
|DirectionNotFoundMessageRus|Текст сообщения DirectionNotFoundMessage при ответе кириллическими символами.|string|значение [DirectionNotFoundMessage](#directionnotfoundmessage)|O|R||
|WaitApplicationTimeout|Время ожидания сообщения от внешнего приложения.<br>**Примечание.** По истечении времени сессия завершается.|int s|30|O|R||
|WaitUserTimeout|Время ожидания ответа от абонента для интерактивных сервисов.<br>**Примечание.** По истечении времени сессия завершается.|int s|600|O|R||
|ChopEndline|Флаг удаления последнего символа, если он является переходом на новую строку.|bool|0|O|R||
|USSD_MaxV1_Len|Максимальная количество символов в сессии USSDv1.<br>**Примечание.** При превышении фаза, полученная от приложения, укорачивается до допустимой по границе слова.|int|200|O|R||
|USSD_MaxV2_Len|Максимальная количество символов в ответе абоненту в сессии USSD v2.<br>**Примечание.** При превышении фаза, полученная от приложения, укорачивается до допустимой по границе слова.|int|182|O|R||
|USSD_MaxRus_Len|Максимальное количество кириллических символов в тексте.|int|80|O|R||
|SendMSISDN|Флаг запроса номера MSISDN.|bool|0|O|R||
|E214_PrefixDelete|Количество удаляемых символов при преобразовании номера от стандарта E212 к E214.|int|5|O|R||
|E214_PrefixAdd|Добавляемый префикс при преобразовании номера от стандарта E212 к E 214.|string|781296|O|R||
|USSD_Translate7bit|Флаг трансляции 7-битных сообщений в ASCII.|bool|1|O|R||
|MT_SendOriginationReference|Флаг требования заполнять поле OriginationReference для MT_USSD.|bool|0|O|R||
|MT_UseOpenInfoMSISDN|Флаг использования СgPA.MSISDN вместо Destination-Reference в Network initiated USSD-сообщениях.|bool|1|O|R||
|StatLogMO|Имя журнала МО-статистики.|string|statMO_USSD|O|R||
|StatLogMT|Имя журнала МТ-статистики.|string|statMT_USSD|O|R||
|CDR_Enabled|Флаг ведения журналов CDR.|bool|0|O|R||
|CDR_Body_Enabled|Флаг записи тела USSD в журнал CDR.|bool|0|O|R||
|CDR_LogMO|Имя журнала CDR для MO‒SMS.|string|CDR_MO_USSD|O|R||
|CDR_LogMT|Имя журнала CDR для MT‒SMS.|string|CDR_MТ_USSD|O|R||
|CDR_LogTR|Имя журнала CDR для TR_USSD.|string|CDR_TR_USSD|O|R||
|CDR_LogTR2|Имя журнала CDR для TR2_USSD.|string|CDR_TR2_USSD|O|R||
|CDR_LogTR2MT|Имя журнала CDR для TR2MT_USSD.|string|CDR_TR2MT_USSD|O|R||
|[USSD_Replies](#ussdreplies)|Перечень предопределенных ответов сервисов.<br>Формат: { #service;#response };|list, object||O|R||
|service|Название сервиса.|string||O|R||
|response|Текст заготовленного ответа.|string||O|R||
|UseSubAddress|Флаг использования поля subaddress.|bool|0|O|R||
|UseInbuiltService|Флаг использования встроенных сервисов: InteractiveTestService, UnicodeTestService, MaxLenService, AdminStatisticService, TimeServiceNumber, для локального тестирования.|bool|1|O|R||
|UseLoadDistributionByMSISDN|Флаг распределения нагрузки по значениям номеров MSISDN.|bool|0|O|R|6.3.49+|
|NodeCount|Количество SMPP-направлений, необходимое для распределения.|int||O|R|6.3.49+|
|**<a name="other">[Other]</a>**|Ключ для reload -<br>**./reload SMS_Routing**||
|DontCheckServiceTypeForSmppDataSM|Флаг обработки сообщения SMPP data_sm при отсутствии значения для service_type.|bool|0|O|R||
|SetSM_TP_SRI|Флаг заполнения поля Status-Report-Indication для логики SendSMS.|bool|0|O|R||
|GetSMPPDirectionJustBeforeSending|Флаг выбора SMPP-направления перед самой отправкой SMS-сообщения для учета всей новых данных, полученных позднее.|bool|0|O|R||
|AllowedPID_ForHR|Идентификаторы протокола PID, имеющие разрешение отправлять MAP-MT.<br>**Примечание.** Сообщения с другими PID отбиваются.|list, int|.*|O|R||
|**<a name="smsmapversion">[SMS_MAP_Version]</a>**||
|Default|[Версия MAP](#mapversion) по умолчанию.|int|1|O|R||
|HLR|Задание версии MAP в зависимости от GT HLR. Формат:<br>Default = #defVer;<br>{<br>&nbsp;&nbsp;GT = "#maskGt";<br>&nbsp;&nbsp;MAP_Version = #version;<br>};|object||O|R||
|Default|Используемая [версия MAP](#mapversion) по умолчанию.|int||O|R||
|GT|Маска GT для HLR.|regex||O|R||
|MAP_Version|[Версия MAP](#mapversion).|int||O|R||
|MSC|Задание версии MAP в зависимости от GT MSC. Формат идентичен формату HLR.|object||O|R||
|SMSC|Задание версии MAP в зависимости от GT SMSC. Формат идентичен формату HLR.|object||O|R||
|**<a name="brttomaperrors">[BRT_to_MAP_Errors]</a>**<br><a name="maptobrterrors">**[MAP_to_BRT_Errors]</a>**||
|ErrorsConverter|Правило конвертации внутренних ошибок BRT и SS7. Формат строк:<br>{ #brtErr;#ss7Err }<br>**Примечание.** При brtErr = 0 задается значение по умолчанию ss7Err = 32.|list, object|{}|O|R||
|**<a name="smpptobrterrors">[SMPP_to_BRT_Errors]</a>**|Ключ для reload -<br>**./reload SMS_Routing**||
|ErrorsConverter|Правило конвертации внутренних ошибок SMPP и BRT. Формат строк:<br>{ #smppErr;#brtErr }<br>**Примечание.** При smppErr = 0 задается значение  значение по умолчанию brtErr = 0xff.|list, object|{}|O|R||
|**<a name="smppstatustobrterrors">[SMPP_Status_to_BRT_Errors]</a>**||
|ErrorsConverter|Правило конвертации статусов SMPP и ошибок BRT. Формат строк:<br>{ #smppStatus;#brtErr }<br>**Примечание.** При smppStatus = 0 задается значение по умолчанию brtErr = 0xff.|list, object|{}|O|R||
|**<a name="smppinternalerrors">[SMPP_InternalErrors]</a>**||
|SMPP_MAP_ErrorsConverter|Правило конвертации внутренних ошибок SMPP и SS7. Формат строк:<br>{ #smppErr;#ss7Err }<br>**Примечание.** При smppErr = 0 задается значение по умолчанию ss7Err = 0xff.|list, object|{}|O|R||
|**<a name="numberconvertation">[NumberConvertation]</a>**|Ключ для reload -<br>**reload SMS_Routing**||
|SMS_SRI_Numbers|Параметры подмены номера при ответе на запрос MAP_SRI.|list, object||O|R||
|Pattern|Маска номера, для которого осуществляется подмена.|regex||O|R||
|ToDo|Параметры подмены.|object||O|R||
|Delete|Правило удаления части номера. Формат:<br>Delete = #numDelete, #startDigit;|object||O|R||
|numDelete|Количество удаляемых символов.|int||M|R||
|startDigit|Позиция первого удаляемого символа в номере.|int|0|O|R||
|Insert|Правило добавления символов к номеру. Формат:<br>Insert = #insSym, #firstDigit;|object||O|R||
|insSym|Символы, добавляемые к номеру.|int||M|R||
|firstDigit|Позиция первого добавляемого символа в номере.|int|0|O|R||
|Replace|Правило замены символов в номере. Формат:<br>Replace = #beginDigit, #numDigit, #replaceSym;|string||O|R||
|beginDigit|Позиция первого заменяемого символа в номере.|int||M|R||
|numDigit|Количество заменяемых символов.|int||M|R||
|replaceSym|Символы, используемые для замены.|int|" "|O|R||
|ReplaceAll|Правило полной подмены номера, новый номер.|int||M|R||


**Примечание.** Использование <a name="usechangegtintcapbegin">UseChangeGTinTCAP_BEGIN</a>:
* для CheckIMEI - в сообщении TCAP_BEGIN_Resp;
* для RecvSM - в сообщении TCAP_BEGIN_Resp;
* для RecvSM - в сообщениях MAP-MO-FSM и MAP-MT-FSM.

**Примечание.** Использование <a name="addressri">AddressRI</a>:
* для CheckIMEI - в сообщении TCAP_BEGIN_Resp;
* для GetLoc - в сообщении MAP-FSM для LOC6 и OJO;
* для RecvSM - в сообщении TCAP_BEGIN_Resp;
* для RecvSM - в сообщениях MAP-MO-FSM и MAP-MT-FSM;
* для SendSMS - при отправке сообщения MAP-SRI;
* для SendSMS - при отправке SMS-сообщения абоненту;
* для SendSMS - при отправке сообщения MAP-Report-SM-Delivery-Status.
* для MO_USSD - при отправке сообщения MAP-SRI.

**Примечание.** Использование <a name="addressssn">AddressSSN</a>:
* для GetLoc - в сообщении MAP-FSM для LOC6 и OJO;
* для RecvSM - в сообщении TCAP_BEGIN_Resp;
* для SendSMS - при отправке сообщения MAP-SRI;
* для SendSMS - при отправке SMS-сообщения абоненту;
* для SendSMS - при отправке сообщения MAP-Report-SM-Delivery-Status.
* для MO_USSD - при отправке сообщения MAP-SRI.

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

### **<a name="specificsendifresponsecodeisnotzero">SpecificSendIfResponseCodeIsNotZero</a>**
Возможные значения:
* 0 - отбой;
* 1 - продолжение обработки.

### **<a name="specificsendiferror">SpecificSendIfError</a>**
Возможные значения:
* 0 - отбой;
* 1 - продолжение обработки.

### **<a name="mapversion">MAP_Version</a>**
Возможные значения:
* 1 - MAPv1;
* 2 - MAPv2;
* 3 - MAPv3.

### **<a name="msgsubtype">msgSubType</a>**
Возможные значения:
* MT - входящее SMS-сообщение;
* MO - исходящее SMS-сообщение;
* HR - home routing SMS-сообщение.

### **<a name="ussdreplies">USSD_Replies</a>**
Можно использовать следующие спецсимволы:
* \\ — задает escape–последовательность, следующие за \\ символы экранируются;
* \# — символ комментария;
* \\\ — обозначение для перехода на следующую строку.
