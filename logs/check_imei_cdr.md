---
title : "CheckIMEI CDR"
description : ""
weight : 2
---

CDR для записи сообщений MAP_CheckIMEI.
Идентификатор журнала (для trace.cfg) - **check_imei_cdr**

### Формат CDR

1. DateTime - Дата и время формирования записи.
2. MSC_GT - Значение GT для MSC или номер отправителя SCCP.CgPN.
3. TON_MSC_GT - Тип нумерации для внешнего MSC.
4. NPI_MSC_GT - Индикатор плана нумерации для внешнего MSC.
5. SMSC_GT - Значение GT для SMSC или номер получателя SCCP.CdPN.
6. RTID - Идентификатор TID при удаленном доступе Remote.
7. IMEI - Идентификатор IMEI.
8. MSISDN - Номер MSISDN.
9. IMSI - Номер IMSI.
10. SMPP_DirectionID - Идентификатор SMPP–направления.
11. ErrorCode - Флаг наличия ошибки.
12. [Status](#status) - Статус запроса MAP_Check_IMEI.

### <a name="status">Status</a>
Возможные значения:
* 2 - e_smpp_dir_empty;
* 3 - e_cant_parse_data;
* 4 - e_invalid_operation_code;
* 5 - e_smpp_error.
