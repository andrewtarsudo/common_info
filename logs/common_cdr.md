---
title : "Common CDR"
description : ""
weight : 2
---

CDR для записи отклоненных сообщений MT-SMS.
Идентификатор журнала (для trace.cfg) - **common_cdr**

### Формат CDR

1. DateTime - Дата и время формирования записи.
2. MessageType - Тип сообщения. Значение - MT.
3. Status - Статус сообщения. Значение - Reject.
4. OriginAddr_NPI - Индикатор плана нумерации отправителя.
5. OriginAddr_TON - Тип номера отправителя.
6. OriginAddr - Номер MSISDN отправителя.
7. OriginAddr_Direction - Идентификатор направления отправителя.
8. DestAddr_NPI - Индикатор плана нумерации получателя.
9. DestAddr_TON - Тип номера получателя.
10. DestAddr - Номер MSISDN получателя.
11. DestAddr_Direction - Идентификатор направления получателя.
12. MSC_GT - Адрес MSC.
13. [Cause](#cause) - Причина запрета транзакции.
14. Details - Дополнительная информация к параметру [Cause](#cause).
15. SMS_params - Параметры SMS в формате PARAM_NAME = PARAM_VALUE, перечисленные через запятую.
16. Тело SMS - Текст SMS-сообщения в hex-формате.

### <a name="cause">Cause</a>
Возможные значения:
* 1 - INVALID_SM - поле Details пусто;
* 2 - INVALID_GT - поле Details пусто;
* 3 - INVALID_IMSI - поле Details пусто;
* 4 - NO_ROUTE - в Details пишется IMSI абонента;
* 5 - SMPP_ERROR - в Details пишется код ошибки SMPP.
