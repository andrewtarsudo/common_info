---
title : "brt.cfg"
description : "Файл настройки работы с BRT"
weight : 3
---

## Используемые секции

Секции, читаемые библиотекой BRT. Эти секции в классическом понимании не перегружаемые. Секция [Timers](#timerrs) вычитывается каждый раз при новом подключении, изменения для старых подключений применять нельзя.
* **[Server](#server)**
* **[Timers](#timers)**

Секции, читаемые приложением. Ключ для reload - **brt.cfg**:
* **[General](#general)**
* **[CDR](#cdr)**
* **[SMS_MSC](#sms_msc)**
* **[ServiceCode](#servicecode)**
* **[MegafonOptimalRouting](#megafonoptimalrouting)**
* **[EmptyIMSI](#emptyimsi)**
* **[VoiceEndReasonConverter](#voiceendreasonconverter)**
* **[RoutingByServiceKey](#routingbyservicekey)**
* **[DurationVerification](#durationverification)**

## Описание параметров

|Name|Description|Type|Default|O/M|P/R|Version|
|:---|:----------|:---|:------|:--|:--|:------|
|**<a name="server">[Server]</a>**||
|IP|Ожидаемый адрес соединения с биллингом.|ip|0.0.0.0|O|P||
|Port|Порт соединения с биллингом.|int||M|P||
|**<a name="timers">[Timers]</a>**||
|ResponseTimeOut|Время ожидания ответа на сообщение от BRT. По истечении времени отправляется ошибка.|int ms|10000|O|C||
|ErrorCount|Максимальное количество ошибок подряд до разрыва связи с BRT. Счетчик ведется отдельно для каждого соединения с биллингом.|int|1|O|C||
|AlarmErrorCount|Максимальное количество ошибок до отправки аварии CAPL.Sg.BRT.Timeout.{ConnID}.<br>**Примечание.** Если значение не меньше ErrorCount, то преобразуется в 0.|int|0|O|C||
|KeepAliveTimeOut|Интервал перепосылки запроса Keep-Alive. <br>**Примечание.** Значение не может быть меньше KeepAliveResponseTimeOut. Keep-Alive не отправляется при KeepAliveTimeOut&nbsp;=&nbsp;0.|int ms|30000|O|C||
|KeepAliveResponseTimeOut|Время ожидания ответа на запрос Keep-Alive.|int ms|10000|O|C|| 
|**<a name="general">[General]</a>**||
|ForwardUnconditionalLocationInformation|Флаг отправки LocationInformation узлу BRT, если причина переадресации - unconditional.|bool|1|O|R||
|ForwardCFNALocationInformation|Флаг отправки LocationInformation узлу BRT, если причина переадресации - 0110b, Mobile Subscriber not Reachable.|bool|1|O|R||
|CpeDirection|Имя направления для соединения с платформой CPE.|string||O|R||
|CallCollectSMSNotification|Список причин отбоя, требующих отправить абоненту SMS с помощью платформы СРЕ.|list, int||O|R||
|ProxyGT|GT для переадресации запроса CAP_InitialDP.|string||O|R||
|IVR_Number|Номер IVR, используемый в сообщении CAP_ETC услуги SponsoredCall.|string||O|R||
|UseUpperSymbols|Флаг использования заглавных букв при передаче номеров в BRT.|bool|0|O|R||
|SendIpAddress|Флаг передачи информации об IP-адресе в поле BRT UserData.|bool|0|O|R|4.3.46.0+, 5.0|
|**<a name="cdr">[CDR]</a>** ||
|VoiceInCdrCharge|Имя CDR для входящих тарифицируемых вызовов.|string||O|R||
|VoiceOutCdrCharge|Имя CDR для входящих нетарифицируемых вызовов.|string||O|R||
|VoiceInCdrNoCharge|Имя CDR для исходящих тарифицируемых вызовов.|string||O|R||
|VoiceOutCdrNoCharge|Имя CDR для исходящих нетарифицируемых вызовов.|string||O|R||
|SmsCdrCharge|Имя CDR для тарифицируемых SMS-сообщений.|string||O|R||
|SmsCdrNoCharge|Имя CDR для нетарифицируемых SMS-сообщений.|string||O|R||
|NewBrtCdr|Имя CDR для вызовов, где был переход на резервный BRT.|string||O|R||
|RestoredVoiceCdr|Имя CDR для восстановленных сессий.|string||O|R||
|**<a name="sms_msc">[SMS_MSC]</a>**||
|MSC_List|Белый список масок MSC отправителя.<br>**Примечание.** При попадании адреса MSC под маску запрос обрабатывается без обращения к BRT, иначе - отправляется запрос в BRT.|regex||O|R||
|**<a name="servicecode">[ServiceCode]</a>**||
|ServiceCodeType|Флаг передачи ServiceCode к BRT без декодирования.|bool|0|O|R||
|DataServiceKeys|Перечень идентификаторов услуг ServiceKey, для которых при ServiceCodeType = 1 и ServiceCode = MO_#/MT_#/MF_# в запросе BRT_AuthorizeVoice к BRT производится замена # на data.|list, int||O|R||
|DefaultServiceCodeType|Подставляемое значение ServiceCodeType для запроса BRT_AuthorizeVoice на BRT.<br>**Примечание.** Для работы подстановки необходимо наличие обоих параметров DefaultServiceCodeType и DefaultServiceCode.|byte 0-255||O|R||
|DefaultServiceCode|Подставляемое значение ServiceCode для запроса BRT_AuthorizeVoice на BRT.<br>**Примечание.** Для работы подстановки необходимо наличие обоих параметров DefaultServiceCodeType и DefaultServiceCode.|int||O|R||
|**<a name="megafonoptimalrouting">[MegafonOptimalRouting]</a>**||
|MSC_List|Маска номеров MSC.|regex||O|R||
|LAC|Значение LAC, подставляемое в поле LocationInformation.|int||M|R||
|**<a name="emptyimsi">[EmptyIMSI]</a>**||
|IMSI|Подстановка при отсутствии IMSI в запросе CAP_InitialDP для SMS.|string|000000000000000|O|R||
|**<a name="voiceendreasonconverter">[VoiceEndReasonConverter]</a>**||
|ReleaseCause|Список кодов причин для подмены.|list, int||M|R||
|EndReason|Подставляемое значение причины.|int|0|M|R||
|**<a name="routingbyservicekey">[RoutingByServiceKey]</a>**||
|ServiceKeys|Список ServiceKey, для которых поиск BRT осуществляется по фиктивному IMSI.|list, int||M|R||
|VirtualIMSI|Фиктивный IMSI для поиска подходящего BRT.|string||M|R||
|MSC_BlackList|Маска номеров MSC для черного списка.|regex||O|R||
|OnlyNotRedirect|Флаг использования VirtualIMSI только для не переадресованных вызовов.|bool|1|O|R||
|**<a name="durationverification">[DurationVerification]</a>**||
|Delta|Значение с которым сравнивается (scp.CallAttemptTime + appllyChargingReport.Duration) - (callInformationReport.callAttemptElapsedTime + callInformationReport.callConnectedElapsedTime).<br>**Примечание.** Значение задается в секундах, но сравнение фактически идет в 100-мс интервалах.|int s|3|O|R||
|CdPN|Маска номера отправителя.|regex||M|R||
|CgPN|Маска номера получателя.|regex||M|R||
|BadReleaseCause|Код ошибки, который будет отправляться на BRT, если абсолютная разница значений ACR и CIR превышает Delta.|int|999|O|R||
