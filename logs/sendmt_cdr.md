---
title : "SendMT CDR"
description : ""
weight : 2
---

CDR для записи исходящих сообщений MAP‒Send‒MT‒SMS (SMPP_DATA->MAP).
Идентификатор журнала (для trace.cfg) - **sendmt_cdr**

### Формат CDR
1. DateTime - Дата и время формирования записи.
2. EventType - Вид транзакции. Значение - SendMT.
3. SMPP_packet_type - Тип сообщения SMPP. Возможные значения: data/submit.
4. SMPP Direction ID - Идентификатор направления отправителя.
5. TON Calling Number - Тип номера отправителя.
6. NPI Calling Number - План нумерации отправителя.
7. Calling Number - Номер MSISDN отправителя.
8. TON Destination Number - Тип номера получателя.
9. NPI Destination Number - План нумерации получателя.
10. Destination Number - Номер MSISDN получателя.
11. IMSI - Номер IMSI.
12. <a name="smscnumber">SMSC_Number</a> - Номер SMSC, обслуживающего абонента.
13. MSC Address (VLR Address Number) Номер MSC/VLR.
14. [Status](#status) - Статус транзакции.
15. [ErrorState](#errorstate) - Состояние сообщения, в котором случилась ошибка.
16. [ErrorType](#errortype) - Тип ошибки.
17. ErrorCode - Код ошибки SCL_Internal.
18. FSM_Number - Количество принятых частей сообщения/количество отправленных сообщений. #received/#sent.
19. IsCharge - Флаг тарификации по протоколу Diameter.
20. CdPN TT - Тип трансляции для получателя.
21. [MessageType](#messagetype) - Тип сообщения. 
22. [DeliveryReportStatus](#deliveryreportstatus) - Статус отчета о доставке.
23. SMS_MT_tarification - Флаг тарификации MT‒SMS.
24. BRT_SessionID - Уникальный идентификатор сессии с BRT.
25. BRT_ConnectionID - Идентификатор соединения с BRT.
26. BRT_ID - Идентификатор BRT. **Примечание.** Пуст при отсутствии работы с BRT.
27. BRT_Cause - Код ошибки BRT.
28. [HttpStatus](#httpstatus) - Статус запроса по протоколу HTTP.
29. DiamResultCode - Идентификатор результата запроса Diameter Result–Code.
30. SendIfError - Флаг отправки сообщения при ошибке по протоколу Diameter.
31. CdrID - Идентификатор cdr для использования при пересылке на другой номер. Значение для SCL - 155.
32. UseForwardingToNewDest - Флаг использования номера, полученного из SMS+, в качестве адреса назначения.
33. sessionId - Идентификатор сессии. **Примечание.** Используется только при ApplicationCode = 10.
34. OriginalDstAddr - Первоначальный номер, полученный в SMPP.dest_addr.
35. Message (hex) - Текст сообщения в формате hex. Только если в gsm.cfg [CDR] WriteMessageText = 1.
36. MessageLength - Длина сообщения. Только если в gsm.cfg [CDR] WriteMessageText = 1.
37. DataCoding - Режим кодирования DCS сообщения SMS. Только если в gsm.cfg [CDR] WriteMessageText = 1.
38. HttpErrorCode - Код ошибки HTTP.
39. ProteiSM_SourceDir - Адрес отправки.
40. Modified_MSCA - Измененный адрес MSC при использовании [SMS_MT_Route] с AddPrefix. Иначе используется значение [SMSC_Number](#smscnumber).
41. DestForSRI - Адрес назначения для сообщения MAP‒SRI. **Примечание.** Используется в качестве SCCP.CdPN, MAP.MSISDN.
42. MessageID - Значение поля SMPP_DATA.m_ProteiSM_MessageID, полученное от узла SMSC.

### <a name="status">Status</a>
Возможные значения:
* 0 - success;
* 1 - failure SRI;
* 2 - failure forward SM;
* 3 - failure register SM;
* 6 - status_failure_Diameter.

### <a name="errorstate">ErrorState</a>
Возможные значения:
* 1 - GetAddr;
* 2 - SendSMS;
* 3 - ReportSMS;
* 4 - WaitSMS;
* 5 - RegisterSMS;
* 6 - UseDiameter.

### <a name="errortype">ErrorType</a>
Возможные значения:
* 3 - GSM;
* 7 - SMPP;
* 8 - SCL_Internal;
* 9 - DiameterBillingError.

### <a name="messagetype">MessageType</a>
Возможные значения:
0 - Message;
1 - DeliveryReport.

### <a name="deliveryreportstatus">DeliveryReportStatus</a>
Возможные значения:
* 0 - DEFAULT (Short message received by the SME);
* 1 - ENROUTE (SME busy);
* 2 - DELIVERED (Short message received by the SME);
* 3 - EXPIREDSM (Validity Period Expired);
* 4 - DELETEDSM (Deleted by SC Administration);
* 5 - UNDELIVERABLE (Not obtainable);
* 6 - ACCEPTED (SME busy);
* 7 - UNKNOWN (Remote procedure error);
* 8 - REJECTED (Remote procedure error).

### <a name="httpstatus">HttpStatus</a>
Возможные значения:
* 0 - HTTP_SUCCESS;
* 1 - HTTP_TIMEOUT;
* 2 - HTTP_ERROR;
* 3 - HTTP_NOT_OK;
* 4 - HTTP_ANS_IS_EMPTY;
* 5 - HTTP_ANS_PARSE_ERR;
* 6 - HTTP_REJECT_SMS;
* 7 - HTTP_ERROR_BUT_SEND_SMS;
* 8 - HTTP_SUBSCRIBER_INACTIVE.
