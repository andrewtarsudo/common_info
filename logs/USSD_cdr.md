---
title : "USSD CDR"
description : ""
weight : 2
---

CDR для записи запросов USSD.
Идентификатор журнала (для trace.cfg) - **CDR_MO_USSD/CDR_MT_USSD или gsm.USSD.CDR_LogMO/gsm.USSD.CDR_LogMT;**

### Формат CDR

1. DateTime - Дата и время формирования записи.
2. ServiceKey/USSD_req - Идентификатор запрашиваемой услуги SK/услуги USSD.
3. DestAddr - Адрес назначения destination_addr.
4. SrcAddr - Адрес отправления source_addr.
5. [Result](#result) - Статус отправки сообщения.
6. IsConvertDCS - Флаг необходимости конвертации DCS.
7. SessionID - Идентификатор сессии Session–Id.
8. SMPPDirection - Идентификатор направления SMPP.
9. SessionDurationInSec - Продолжительность сессии.
10. SMPP_SessionID Идентификатор сессии по протоколу SMPP, извлеченный из значения ProteiSM_SessionID входящего сообщения SMPP_SUBMIT.
11. MAP_ErrorCode - Код ошибки протокола MAP.

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
* 12 - ERROR_USSD_BRT_ERROR;
* 13 - ERROR_USSD_BRT_AUTHORIZE_REJECT;
* 14 - ERROR_LICENSE_LIMIT;
* 16 - ERROR_BLOCKED_SMPP_DIRECTION;
* 17 - ERROR_DIRECTION_NOT_FOUND.
