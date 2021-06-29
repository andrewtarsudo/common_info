---
title : "SMS CDR"
description : ""
weight : 2
---

CDR для записи входящих сообщений по MAP.
Идентификатор журнала (для trace.cfg) - **sms_cdr**

### Формат CDR

1. DateTime - Дата и время формирования записи.
2. [EventType](#eventtype) - Вид транзакции.
3. SessionID - Идентификатор сессии.
4. BRT_ConnectionID - Идентификатор соединения с BRT.
5. BRT_ID/ScenarioID - Идентификатор BRT/сценария.
6. IMSI - Номер IMSI.
7. TON Calling Number - Тип номера отправителя.
8. NPI Calling Number - Идентификатор плана нумерации отправителя.
9. Calling Number - Номер MSISDN отправителя.
10. TON Destination Number - Тип номера получателя.
11. NPI Destination Number - План нумерации получателя.
12. Destination Number - Номер MSISDN получателя.
13. SMSC Number - Номер SMSC, обслуживающего абонента.
14. MSC Address/VLR Address - Номер MSC/VLR.
15. [Status](#status) - Статус SMS–сообщения.
16. MAP Cause - Код ошибки MAP.
17. SMPP Status - Код статуса SMPP.
18. SMPP Internal Error - Код внутренней ошибки SMPP.
19. BRT/Diameter Cause - Код ошибки BRT/Diameter.
20. IsCharge - Флаг тарификации по протоколу Diameter.
21. ErrorCode - Код ошибки.
22. StartTime - Время отправки сообщения.
23. New TON Calling Number - Новый тип номера отправителя.
24. New NPI Calling Number - Новый индикатор плана нумерации отправителя.
25. New Calling Number - Новый номер CgPN отправителя.
26. New TON Called Number - Новый тип номера получателя.
27. New NPI Called Number - Новый индикатор плана нумерации получателя.
28. New Called Number - Новый номер CdPN получателя.
29. DirectionID - Идентификатор направления SMPP.
30. IsMO_Forward - Флаг разрешения пересылать MO_SMS.
31. NewGT - GT места пересылки MAP_MO_SMS_Forward.
32. ZTE_MessageID - Идентификатор сообщения ZTE.
33. ZTE_Cause - Код ошибки ZTE.
34. MCC - MCC из опционального поля forwardSMreqwithCellInfo.
35. MNC - MNC из опционального поля forwardSMreqwithCellInfo.
36. LAC - LAC из опционального поля forwardSMreqwithCellInfo.
37. UID - Идентификатор пользователя в Service_Specific_Info.
38. [AppCode](#appcode) - Идентификатор приложения.
39. GT SCP - Значение GT, полученное в ответ на сообщение MAP_ATSI.
40. MessageIdFromSMSC - Идентификаторы сообщения на SMSC.
41. SendIfError - Флаг отправки сообщения при ошибке по протоколу Diameter.
42. TotalParts - Общее количество частей многокомпонентного сообщения.
43. CurrentPart - Порядковый номер текущая часть сообщения.
44. RefNum - Ссылочный номер reference_number на части сообщения.
45. Message (hex) - Текст сообщения в формате hex. Только если в gsm.cfg [CDR] WriteMessageText = 1.
46. MessageLength - Длина сообщения. Только если в gsm.cfg [CDR] WriteMessageText = 1.
47. DataCoding - Режим кодирования DCS сообщения SMS. Только если в gsm.cfg [CDR] WriteMessageText = 1.
48. [HttpStatus](#httpstatus) - Текущий статус запроса по HTTP.
49. [HttpErrorCode](#httperrorcode) - Код ошибки HTTP.

### <a name="eventtype">EventType</a>
Возможные значения:
* Sc;
* BRT;
* BRT-SC;
* Diameter;
* Diameter-SC;
* Diameter_MT;
* Diameter-SC_MT (Home Rerouting).

### <a name="appcode">AppCode</a>
Возможные значения:
* 0 - MOTIV;
* 1 - ORGA;
* 2 - GLOBAL;
* 3 - SITRONICS;
* 4 - REDKNEE;
* 5 - REDKNEE_2;
* 6 - NURTELECOM;
* 7 - MTT;
* 8 - SPRINT;
* 9 - MEGAFON;
* 10 - TINKOFF;
* 11 - PETER_SERVICE;
* 12 - SIM_TELECOM;
* 13 - HUMANS.

### <a name="status">Status</a>
Возможные значения:
* 0 - success;
* 1 - failure;
* 2 - reject;
* 3 - tcap_timeout;
* 4 - tcap_reject;
* 5 - tcap_abort;
* 6 - tcap_empty_end;
* 7 - not_use_brt_reject_scenario;
* 8 - use_brt_reject_scenario;
* 9 - not_use_diameter_reject_scenario;
* 10 - use_diameter_reject_scenario;
* 11 - tp_reject_duplicates;
* 12 - atsi_error;
* 13 - http_error;
* 14 - http_specific_error.

### <a name="httpstatus">HttpStatus</a>
Возможные значения:
* -1 - не используется;
* 0 - HTTP_SUCCESS;
* 1 - HTTP_TIMEOUT;
* 2 - HTTP_ERROR;
* 3 - HTTP_NOT_OK;
* 4 - HTTP_ANS_IS_EMPTY;
* 5 - HTTP_ANS_PARSE_ERR;
* 6 - HTTP_REJECT_SMS;
* 7 - HTTP_ERROR_BUT_SEND_SMS;
* 8 - HTTP_SUBSCRIBER_INACTIVE;
* 9 - HTTP_SPECIFIC_ERROR_BUT_SEND_SMS.

### <a name="httperrorcode">HttpErrorCode</a>
Возможные значения:
* 0 - e_http_success;
* 1 - e_http_disconnect_ind;
* 2 - e_http_connect_rejected;
* 3 - e_http_connect_fail_ind;
* 4 - e_http_response_timer;
* 5 - e_http_unexpected_prim;
* 6 - e_http_overloaded;
* 7 - e_http_message_parse;
* 8 - e_http_message_unexpected;
* 9 - e_http_no_ca;
* 10 - e_http_invalid_ca;
* 11 - e_http_ssl_fail;
* 12 - e_http_reload_in_progress;
