---
title : "Note-MM-Event CDR"
description : ""
weight : 2
---

CDR для записи сообщений MAP_NoteMM_Event.
Идентификатор журнала (для trace.cfg) - **notemm_event_cdr**

### Формат CDR

1. DateTime – Дата и время формирования записи.
2. MSISDN - Номер MSISDN.
3. IMSI - Номер IMSI.
4. IMEI - Номер IMEI. Пустое поле.
5. LAC - Код LAC.
6. CellID - Идентификатор соты Cell ID.
7. RAI - Идентификатор RAI. Пустое поле.
8. MSC - Адрес MSC.
9. SGSN - Адрес узла SGSN. Пустое поле.
10. [EventMet](#eventmet) - Код триггера.
11. MessageID - Идентификатор Message–Id. Пустое поле.
12. VLR - Адрес VLR.
13. MCC - Код страны MCC.
14. MNC - Код сети MNC.
15. ServiceKey - Идентификатор услуги SK.

### <a name="eventmet">EventMet</a>
Возможные значения:
* 0 - Location-update-in-same-VLR MM-Code;
* 1 - Location-update-to-other-VLR MM-Code;
* 2 - IMSI-Attach MM-Code;
* 3 - MS-initiated-IMSI-Detach MM-Code;
* 4 - Network-initiated-IMSI-Detach MM-Code.
