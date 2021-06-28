---
title : "CDR_TR2_USSD CDR"
description : ""
weight : 2
---

CDR для расширенной записи запросов USSD.
Идентификатор журнала (для trace.cfg) - **gsm.USSD.CDR_LogTR2 = CDR_TR2_USSD**

### Формат CDR

1. Datetime - Дата и время формирования записи.
2. SessionID - Идентификатор сессии.
3. SrcAddr - Номер MSISDN отправителя, извлеченный из MAP_OpenInfo.OriginationReference.
4. DstAddr - Номер MSISDN получателя, извлеченный из MAP_OpenInfo.DestinationReference.
5. [Type](#type) - Тип сообщения.
6. Text - Текст сообщения.
7. Dcs - Схема кодирования DCS.
8. Direction - Идентификатор направления SMPP.
9. [MessageStage](#messagestage) - Код типа сообщения TCAP.
10. MSISDN - Номер MSISDN, извлеченный из MAP_PDU, MAP_OpenInfo или MAP_OpenInfo.DestinationReference. **Примечание.** В иных случаях пусто.
11. [Result](#result) - Код результата отправки сообщения.

### <a name="type">Type</a>
Возможные значения:
* req_mo;
* req_mt;
* resp_mo;
* resp_mt.

### <a name="messagestage">MessageStage</a>
Возможные значения:
* 0 - TCAP_BEGIN;
* 1 - TCAP_CONTINUE;
* 2 - TCAP_END.

### <a name="result">Result</a>
Возможные значения:
* 0 - SUCCESS;
* 1 - ERROR_SMPP_NO_CONNECTION;
* 2 - ERROR_SMPP_TIMEOUT;
* 3 - ERROR_SMPP_LIMIT_EXCEED;
* 4 - ERROR_SMPP_UNSPECIFIED;
* 5 - ERROR_SMPP_RESPONSE;
* 6 - ERROR_SMPP_MESSAGE;
* 7 - ERROR_APP_TIMEOUT;
* 8 - ERROR_APP_NO_HANDLERS;
* 9 - ERROR_USER_TIMEOUT;
* 10 - ERROR_USER_ABORT;
* 11 - ERROR_UNKNOWN;
* 12 - ERROR_LICENSE_LIMIT;
* 13 - ERROR_BLOCKED_SMMP_DIRECTION.
