
Секция [General] Команда для reload: **reload SMS_Routing**
ApplicationCode O/P Код приложения заказчика. Тип - int. Значение по умолчанию - 0.
TPRejectDuplicates O/R Флаг отбития MO‒SMS, если в сообщении SMPP_submit_sm активирован флаг TP–Reject–Duplicates. Тип - bool. Значение по умолчанию - 0.
GPRS_SupportIndicator O/R Флаг активации gprsSupportIndicator при кодировании SRI для MT‒SMS. Тип - bool. Значение по умолчанию - 0.
Секция [TrafficManager]
MaxQueueSize O/P Максимальное допустимое количество примитивов в очереди. Тип - int. Значение по умолчанию - 600.
Секция [SMPP_StatusErrors]
SMPP_MAP_Errors_Converter O/R Правило конвертации ошибок SMPP и SS7. Формат:<br>SMPP_MAP_Errors_Converter = {<br>  { #smppErr;#ss7Err }<br>}<br>**Примечание.** При smppErr = 0 задается значение ss7Err по умолчанию. Если такой пары нет, то значением по умолчанию принимается 0xff. Тип - list, object.
Секция [SMPP_InternalErrors]
SMPP_MAP_ErrorsConverter O/R Правило конвертации внутренних ошибок SMPP и SS7. Формат:<br>SMPP_MAP_ErrorsConverter = {<br>  { #smppErr;#ss7Err }<br>}<br>**Примечание.** При smppErr = 0 задается значение ss7Err по умолчанию. Если такой пары нет, то значением по умолчанию принимается 0xff. Тип - list, object.
Секция [SMSC] Команда для reload: **reload SMS_Routing**
Handlers O/P Максимальное количество зарезервированных логик.<br> **Примечание.** Будет выделено в 2 раза больше логик, поскольку инициализируются и для SendSMS, и для остальных. Тип - int. Значение по умолчанию - 2500.
RemoteGT O/R Адрес GT для SCCP.RemotePA при использовании услуг LBS. Тип - string.
Address M/R Адрес SCCP.LocalPA для транзакций, инициированых SC_Lite, от имени которого коммутатору отправляются запросы на определение местоположения абонента. Тип - string.
UseChangeGTinTCAP_BEGIN O/R Флаг подмены SCCP.LocalPA на Address в сообщениях TCAP_BEGIN_Resp. Тип - bool. Значение по умолчанию - 0.
UseChangeGTinUSSD_TCAP_BEGIN O/R Флаг подмены SCCP.LocalPA на Address в сообщениях TCAP_BEGIN_Resp для MO‒USSD. Тип - bool. Значение по умолчанию - 0.
AddressRI O/R Значение RI для Address.<br>**Примечание.** Используется для CheckIMEI, GetLoc, RecvSM, SendSMS, MO_USSD.Тип - int. Значение по умолчанию - "–1", без замены.
AddressSSN O/R Значение SSN для Address. **Примечание.** Используется для GetLoc, RecvSM, SendSMS, MO_USSD. Тип - int. Значение по умолчанию - "–1", без замены.
IMSI_WhiteList O/R Разрешенный список префиксов IMSI для IMSI_MSISDN_Converter. Тип - list, string.
Значение по умолчанию - "".
IMSI_MSISDNConverter O/R Правила конвертации MSISDN и IMSI друг в друга. Формат:<br>{ "#msisdn"; "#imsi" } Тип - list, object.
MSISDN_IMSIConverter O/R Параметр, позволяющий задать несколько правил конвертации MSISDN и IMSI друг в друга. Формат:<br>{ "#msisdn"; "#imsi" } Тип - list, object. 
MT_GT_BlackList O/R Маска для черного списка номеров MSC для MT‒SMS. Тип - regex. Значение по умолчанию - "".
MAP_ErrorFor_GT_BlackList O/R Код ошибки MT‒SMS, если MSC находится в черном списке. Тип - int. Значение по умолчанию - 0.
MO_GT_WhiteList O/R Маска для белого списка номеров MSC для MT‒SMS. Тип - regex. Значение по умолчанию - "".
MAP_ErrorFor_GT_WhiteList O/R Код ошибки MO‒SMS, если MSC находится в черном списке. Тип - int. Значение по умолчанию - 0.
Секция [SMSC] Ключ для reload: **./reload USSD**
BlockedSmppDirectionsMT_USSD O/R Список SMPP–направлений, для которых запрещена отправка MT– USSD. Тип - list, int. Значение по умолчанию - не используется.
DebugNumbers O/R Перечень номеров абонентов, которым в случае ошибки отправляется отладочная информация вместо ErrorMessage. Тип - list, regex.
TimeServiceNumber O/R Номер доступа к сервисной службе точного времени. Тип - string. Значение по умолчанию – *060#.
TimeServiceEng O/R Флаг использования английского языка. Тип - bool.
TimeServiceZone O/R Номер доступа к службе информирования о временной зоне. Тип - string, Значение по умолчанию - MSK.
TimeServiceHeader O/R Текст перед временем.<br>**Примечание.** Задается в кодировке cp–1251. Тип - string. Значение по умолчанию - Московское время:.
AdminStatisticService O/R Номер доступа к сервису статистики работы SC_Lite для номеров DebugNumbers. Тип - string. Значение по умолчанию - *1790#
SimpleTestService O/R Номер доступа для тестирования приложения. Тип - string. Значение по умолчанию - *555#.
InteractiveTestService O/R Номер доступа к службе тестирования интерактива приложения. Тип - string. Значение по умолчанию - *556#.
UnicodeTestService O/R Номер доступа к приложению, выводящему информацию о поддержке русского языка. Тип - string. Значение по умолчанию - *557#.
MaxLenService O/R Номер доступа к сервисной службе. Тип - string. Значение по умолчанию - *558#.
ErrorMessage O/R Текст сообщение для абонента в случае ошибки работы с внешним приложением. Тип - string. Значение по умолчанию - "noBTOPuTe 3 anpoc no3>|<e. Cnacu 6 o!\nPlease try later. Thank you!"
ErrorMessageRus O/R Текст сообщения ErrorMessage, записанный кириллическими символами. Тип - string. Значение по умолчанию - значение ErrorMessage.
DirectionNotFoundMessage O/R Текст сообщения для абонента при отсутствии USSD_ServiceKey во всех направлениях SMPP. **Примечание.** Поддерживаемые кодировки: Unicode и ASCII. Значение по умолчанию – "".
DirectionNotFoundMessageRus O/R Текст сообщения DirectionNotFoundMessage при ответе абоненту кириллическими символами. Тип - string. Значение по умолчанию - используется ошибка на английском.
WaitApplicationTimeout O/R Время ожидания сообщения от внешнего приложения.<br>**Примечание.** По истечении времени сессия завершается. Тип - int s. Значение по умолчанию - 30.
WaitUserTimeout O/R Время ожидания ответа от абонента для интерактивных сервисов.<br>**Примечание.** По истечении времени сессия завершается. Тип - int s. Значение по умолчанию - 600.
ChopEndline O/R Флаг удаления последнего символа, если он является переходом на новую строку. Тип - bool. Значение по умолчанию - 0.
USSD_MaxV1_Len O/R Максимальная количество символов в сессии USSD v1.<br>**Примечание.** При превышении фаза, полученная от приложения, укорачивается до допустимой по границе слова. Тип - int. Значение по умолчанию - 200.
USSD_MaxV2_Len O/R Максимальная количество символов в ответе абоненту в сессии USSD v2.<br>**Примечание.** При превышении фаза, полученная от приложения, укорачивается до допустимой по границе слова. Тип - int. Значение по умолчанию - 182.
USSD_MaxRus_Len O/R Максимальное количество кириллических символов в тексте. Тип - int. Значение по умолчанию - 80.
SendMSISDN O/R Флаг запроса номера MSISDN. Тип - bool. Значение по умолчанию - 0.
E214_PrefixDelete O/R Количество удаляемых символов при преобразовании номера от стандарта E212 к E214. Тип - int. Значение по умолчанию - 5.
E214_PrefixAdd O/R Добавляемый префикс при преобразовании номера от стандарта E212 к E 214. Тип - string. Значение по умолчанию - 781296.
USSD_Translate7bit O/R Флаг трансляции 7–битных сообщений в ASCII.
Тип - bool. Значение по умолчанию - 1.
MT_SendOriginationReference O/R Флаг требования заполнять поле OriginationReference для MT_USSD. Тип - bool. Значение по умолчанию - 0.
StatisticsEnabled O/R Флаг ведения статистики. Тип - bool. Значение по умолчанию - 0.
StatisticsPeriodLength O/R Период сброса статистики. Тип - int s.
Значение по умолчанию - 3600.
StatLogMO O/R Имя журнала МО–статистики. Тип - string. Значение по умолчанию - statMO_USSD.
StatLogMT O/R Имя журнала МТ–статистики. Тип - string. Значение по умолчанию - statMT_USSD.
CDR_Enabled O/R Флаг ведения журналов CDR. Тип - bool. Значение по умолчанию - 0.
CDR_PeriodLength O/R Период сброса CDR. Тип - int s. Значение по умолчанию - 60.
CDR_LogMO O/R Имя журнала CDR для MO‒SMS. Тип - string. Значение по умолчанию - CDR_MO_USSD.
CDR_LogMT O/R Имя журнала CDR для MT‒SMS. Тип - string. Значение по умолчанию - CDR_MТ_USSD.
CDR_LogTR2 O/R Имя журнала CDR для TR2_USSD. Тип - string. Значение по умолчанию - CDR_TR2_USSD.
WriteCDR_LogTR2 O/R Флаг ведения журнал CDR_LogTR2. Тип - bool. Значение по умолчанию - 0.
USSD_Replies O/R Перечень предопределенных ответов сервисов. Формат:<br>USSD_Replies = {<br>{ #service;#response };<br>}
**Примечание**. Можно использовать следующие спецсимволы:<br> \ - задает escape–последовательность, следующие за \ символы экранируются;<br> # - символом комментария;<br>\\ - обозначение для перехода на следующую строку. Тип - list, object.
service O/R Название сервиса. Тип - string.
response O/R Текст заготовленного ответа. Тип - string.
Секция [SMS] Ключ для reload - **./reload SMS_Routing**
DeliverType O/R Тип отправляемого сообщения. Возможные значения:
deliver/data. Тип - string. Значение по умолчанию - deliver.
Translate7bit O/R Флаг включения трансляции 7 bit сообщений в ASCII. Тип - bool. Значение по умолчанию - 1.
TruncateMSISDN О/R Флаг укорачивания MSISDN до 10 символов. Тип - bool. Значение по умолчанию - 1.
TimeZone O/R Отклонение временной зоны, МАР–TP–Service–Centre–Time–Stam, от времени по Гринвичу. Тип - int. Значение по умолчанию - 0.
SMS_UseBRT O/R Флаг использования BRT_Interface для всех MO‒SMS. Тип - bool. Значение по умолчанию - 0.
SMS_UseDiameter O/R Флаг использования тарификации Diameter для всех MO‒SMS. Тип - bool. Значение по умолчанию - 0.
SMS_MT_UseDiameter O/R Флаг использования тарификации Diameter для всех MT‒SMS. Тип - bool. Значение по умолчанию - 0.
SMS_MAP_MT_UseDiameter O/R Флаг использования тарификации Diameter для всех MAP‒MT‒SMS– сообщений. Тип - bool. Значение по умолчанию - 0.
SMS_SleepBeforeSend O/R Задержка перед отправкой MAP‒SM.<br>**Примечание.** Если задано значение вне диапазона, то оно приводится к ближайшему числу в требуемом интервал. Тип - int ms, 0–10000. Значение по умолчанию - 0.
UseMoreMessagesToSendFlag O/R Флаг использования More Messages to Send, TP–MMS, для отправки конкантенированных сообщений. Тип - bool. Значение по умолчанию - 0.
Секция [HTTP] ./reload SMS_Routing
sessionId O/P Уникальный идентификатор операции. Тип - string.
timestamp M/R Дата и время совершения действия. Формат:<br>согласно стандарту ISO 8601 – 1 :2019: YYYY–MM–DD hh:mm:ss Тип - datetime. 
msisdnA O/R Номер MSISDN отправителя. Тип - string, не более 15 символов.
msisdnB O/R Номер MSISDN получателя. Тип - string, не более 15 символов.
smsBody O/R Текст SMS–сообщения. Тип - string.
smsId O/R Идентификатор составного SMS–сообщения. Тип - int<br>0-255.
partsQty O/R Общее количество частей в составном SMS–сообщении. Тип - int<br>0-255.
partNumber O/R Идентификатор части составного SMS–сообщения. Тип - int<br>0-255.
vlr O/R Адрес VLR. Тип - string, не более 15 символов.
msgType O/R Источник сообщения. Тип - string. Значение - SCL.
msgSubType O/R Вид сообщения.<br>MT - входящее SMS–сообщение;<br>MO - исходящее SMS–сообщение;<br>HR - home routing SMS–сообщение. Тип - string.
SpecificDirection O/R Идентификатор HTTP–направления. Тип - int. Значение по умолчанию - –1.
ReserveDirection O/R Индикатор резервного HTTP–направления при недоступности основного. Тип - int.
IMSI_WhiteListForSpecificHTTP O/R Перечень номеров IMSI, которым можно отправлять запросы. Тип - list, regex.
SourceBlackList O/R Перечень отправителей SMS, для которых не посылается запрос на CPE. Тип - list, элементы - маски MSISDN типа regex.
SpecificSendIfResponseCodeIsNotZero O/R Индикатор дальнейших действий при получении ResponseCode, отличного от 0.<br>0 - отбой;<br>1 - продолжение обработки. Тип - int.
SpecificSendIfError O/R Индикатор дальнейших действий по истечении времени ожидания или получении сообщения, отличного от HTTP 200 OK.<br>0 - отбой;<br>1 - продолжение обработки. Тип - int. Возможные значения:
URI O/R Ссылка на запрос. Тип - string. Значение по умолчанию - "".
SendIfError O/R Флаг отправления SMS–сообщения при получении ошибки или срабатывания таймера. Тип - bool. Значение по умолчанию - 0.
SpecificAnsTimeout O/R Время ожидания ответа по HTTP. Тип - int s.
Direction O/R Номер направления для отправки запроса. Тип - int.
DestBlackList O/R Перечень MSISDN получателей SMS–сообщений, которым не
посылается запрос. Тип - list, regex.
DestWhiteList O/R Перечень MSISDN получателей SMS–сообщений, которым посылается запрос. Тип - list, элементы - маски MSISDN типа regex.
SendAfterDIAM O/R Флаг отправки http–запросов на подмену CdPN в биллинг после отправки запросов по протоколу Diameter для MO–SMS сообщений. Тип - bool. Значение по умолчанию - 0.
SendGet O/R Флаг возможности отправки GET–запросов. Тип - bool. Значение по умолчанию - 1.
Секция [LBS] ./reload lbs
ActiveLocationRequest O/R Флаг применения запросов ActiveLocationRequest для LOC–сервисов не из списка типичных пользователей.<br>**Примечание.** Используется всегда: LOC4, LOC5, LOC6, LOC8, OJO. Тип - bool. Значение по умолчанию - 0.
GT_HLR_ForATI O/R Адрес назначения MAP‒ATI для LOC11. Тип - string. Значение по умолчанию - 1.
SetEllipsoidArc О/R Флаг активации поля MAP_SupportedGADShapes со значением EllipsoidArc при кодировании MAP‒PSL для LOC5. Тип - bool. Значение по умолчанию - 0.
AddSubscriberStateToPsiFor O/R Перечень разрешенных адресов для заполнения поля e_subscriberState сообщения MAP_RequestedInfo при кодировании MAP–PSL для LOC5. Тип - int. Значение по умолчанию - 0.
SendPsiOnErrorFor O/R Перечень разрешенных адресов для отправления MAP‒PSI при получении TCAP_RETURN_ERROR для MAP‒FSM. Тип - list, string. Значение по умолчанию - "".
SubscriberStateWhiteListForSRI_GT O/R Перечень разрешенных адресов для запросов MAP‒SRI‒SM_Resp.<br>**Примечание.** При провале проверки MAP–FSM не отправляются. Тип - list, string. Значение по умолчанию - "".
SendPSL_ForMSC O/R Перечень разрешенных адресов для MAP‒ATI_Resp сервиса LOC 9.<br>**Примечание.** При успешной проверке MAP‒FSM не отправляются. Тип - list, string. Значение по умолчанию - "".
Секция [Other] Команда для перезагрузки - ./reload SMS_Routing
ZTE_GT_CheckIMEI O/R Перечень масок номеров, обслуживающиеся по стандарту ZTE. Тип - regex.
UseMT_ForwardingByError O/R Флаг активации услуги переадресации. Тип - bool. Значение по умолчанию - 0.
FwCauses O/R Перечень кодов причин для переадресации сообщения. Тип - list, int.
AllowedPID_ForHR O/R Идентификаторы протокола PID, имеющие разрешение отправлять MT‒FSM для HomeRouting. Тип - list, элементы - идентификаторы типа int.
GetSMPPDirectionJustBeforeSending O/R Флаг повторного выбора SMPP–направления для SMS–сообщения в случае модификации номера со стороны биллинга. Тип - bool.
DontCheckServiceTypeForSmppDataSM O/R Флаг отмены проверки параметра service_type для входящих SMS–сообщений. Тип - bool. Значение по умолчанию - 0.
Секция [SMS_MAP_Version]
Default O/R Версия MAP по умолчанию. Тип - int. Значение по умолчанию - 1.
HLR O/R Задание версии MAP в зависимости от GT HLR. Формат:<br>HLR = {<br> Default = #defVer;<br>{<br>GT = "#maskGt";<br>MAP_Version = #version;<br>};<br>}. Тип - object.
Default O/R Используемая версия MAP по умолчанию.<br>1 - MAPv1;<br>2 - MAPv2;<br>3 - MAPv3.<br> Тип - int.
GT O/R Маска GT для HLR. Тип - regex.
MAP_Version O/R Версия MAP.<br>1 - MAPv1;<br>2 - MAPv2;<br>3 - MAPv3.<br> Тип - int.
MSC O/R Задание версии MAP в зависимости от GT MSC. Формат:<br>MSC = {<br>Default = #defVer;<br>{<br>GT = "#maskGt";<br>MAP_Version = #version;<br>};<br>} Тип - object.
Секция [BRT_to_MAP_Errors]
Секция [MAP_to_BRT_Errors]
ErrorsConverter O/R Правило конвертации внутренних ошибок BRT и SS7. Формат:<br>SMPP_MAP_Errors_Converter = {<br>{ #brtErr;#ss 7 Err }<br>}
**Примечание.** При brtErr = 0 задается значение ss 7 Err по умолчанию.
Если такой пары нет, то значением по умолчанию принимается 32. Тип - list, object.
Секция [SMPP_to_BRT_Errors] Команда для перезагрузки: ./reload SMS_Routing
ErrorsConverter O/R Правило конвертации внутренних ошибок SMPP и BRT. Формат:<br>SMPP_BRT_Errors_Converter = {<br>{ #smppErr;#brtErr }<br>}<br>**Примечание.** При smppErr = 0 задается значение brtErr по умолчанию. Если такой пары нет, то значением по умолчанию принимается 0xff.  Тип - list, object.
Секция [SMPP_Status_to_BRT_Errors]
ErrorsConverter O/R Правило конвертации статусов SMPP и ошибок BRT. Формат:<br>SMPP_BRT_Errors_Converter = {<br>{ #smppStatus;#brtErr }<br>}<br>**Примечание.** При smppStatus = 0 задается значение brtErr по умолчанию. Если такой пары нет, то значением по умолчанию принимается 0 xff. Тип - list, object.
Секция [SMS_MT_Route]
CdPN O/R Номер получателя SMS–сообщения. Тип - string.
IMSI O/R Маска номера IMSI получателя. Тип - regex.
VLR O/R Адрес VLR. Тип - string.
InboundSMPP_dirs O/R Перечень идентификаторов направления на ядре SMSC. Тип - list, int.
DelDigitsFromBegin O/R Количество цифр, удаляемых с начала номера. Тип - int.
SGSN O/R Адрес SGSN. Тип - string.
AddPrefix O/R Символы, добавляемые к началу номера. Тип - string.
BlockWithCommandStatus O/R Идентификатор статуса команды command_status, при наличии которого SMS–сообщения блокируются. Тип - int.
ErrorType O/R Тип ошибки при блокировке SMS–сообщения, передаваемые в SMSC для настройки обработки SMS–сообщения в сценарии. Тип - int.
ErrorCode O/R Код ошибки при блокировке SMS–сообщения, передаваемые в SMSC для настройки обработки SMS–сообщения в сценарии. Тип - int.
