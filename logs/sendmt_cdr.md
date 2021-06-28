---
title : "SendMT CDR"
description : ""
weight : 2
---

CDR для записи исход.сообщений (SMPP_DATA->MAP)
Идентификатор журнала (для trace.cfg) - **sendmt_cdr**

### Формат CDR

1. DateTime
2. EventType (SendMT)
3. SMPP_packet_type (data/submit)
4. SMPP Direction ID (откуда пришло)
5. TON Calling Number
6. NPI Calling Number
7. Calling Number
8. TON Destination Number
9. NPI Destination Number
10. Destination Number
11. IMSI
12. SCL Address
13. MSC Address (VLR Address Number)
14. Status (0 - success, 1 - failure SRI, 2 - failure forward SM, 3 - failure register SM (превышена лицензия или не удается закодировать SMS), 6 - Status_Failure_Diameter)
15. ErrorState (состояние: GetAddr = 1, SendSMS = 2, ReportSMS = 3, WaitSMS = 4, RegisterSMS = 5, UseDiameter = 6)
16. ErrorType (тип ошибки: GSM = 3, SMPP = 7, SCL_Internal = 8, DiameterBillingError = 9)
17. ErrorCode (код ошибки)
18. Кол-во Forward SM (сколько из скольки дошло, например: 1/3; заполняется не всегда)
19. IsCharge - 0|1 (for diameter tarification)
20. CdPNTT - TranslationType for CdPN
21. MessageType - 0 - message/ 1- deliveryreport
22. DeliveryReportStatus
    0 -  default (not present) (Short message received by the SME)
    1 - ENROUTE (SME busy)
    2 - DELIVERED (Short message received by the SME)
    3 - EXPIREDSM (Validity Period Expired)
    4 - DELETEDSM (Deleted by SC Administration)
    5 - UNDELIVERABLE (Not obtainable)
    6 - ACCEPTED (SME busy)
    7 - UNKNOWN (Remote procedure error)
    8 - REJECTED (Remote procedure error) 

23. SMS_MT_tarification
24. BRT_SessionID
25. BRT_ConnectionID
26. BRT_ID
27. BRT_Cause
28. HttpStatus
    0 - HTTP_SUCCESS,
    1 - HTTP_TIMEOUT
    2 - HTTP_ERROR
    3 - HTTP_NOT_OK
    4 - HTTP_ANS_IS_EMPTY
    5 - HTTP_ANS_PARSE_ERR
    6 - HTTP_REJECT_SMS
    7 - HTTP_ERROR_BUT_SEND_SMS
    8 - HTTP_SUBSCRIBER_INACTIVE

29. DiamResultCode -
30. SendIfError - отправлять смс если не смогли отправить запрос по диаметру
31. CdrID - id для связывания cdrs при форвардинге на другой номер (SCL-155)
32. UseForwardingToNewDest - используем номер, полученный из smsplus в качестве Dest
33. sessionId - only for Tinkoff (ApplicationCode = 10)
34. OriginalDstAddr - первоначальный номер, полученный в SMPP.dest_addr
35. Mesage (hex) # если gsm.cfg [CDR] WriteMessageTextMT = 1;
36. Message length # если gsm.cfg [CDR] WriteMessageTextMT = 1;
37. DataCoding # если gsm.cfg [CDR] WriteMessageTextMT = 1;
38. HttpErrorCode
39. ProteiSM_SourceDir
40. Modified_MSCA - измененный MSC адрес в случае использования [SMS_MT_Route] с AddPrefix, иначе изначальный адрес(MSC из 12 поля)
41. DestForSRI - адрес используемый для отправки SRI (SCCP.CdPN, MAP.MSISDN)
42. MessageID - значение поля SMPP_DATA.m_ProteiSM_MessageID полученное от SMSC
