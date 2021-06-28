---
title : "Alert CDR"
description : ""
weight : 2
---

CDR для записи сообщений MAP_AlertServiceCentre.
Идентификатор журнала (для trace.cfg) - **alert_cdr**

### Формат CDR

1. DateTime - Дата и время формирования записи.
2. MSC_GT - Адрес MSC, извлеченный из SCCP_CgPA.
3. SMSC_GT - Адрес обслуживающего SMSC, извлеченный из SCCP_CdPA.
4. SrcAddr - Номер MSISDN отправителя.
5. EsmeAddr - Адрес SC_Lite, значение gsm.SMSC.Address в файле gsm.cfg.
6. DirectionList - Перечень идентификаторов направлений для отправки alert. Значения извлекаются из флагов gsm.HTTP.ReceiveAlert файла gsm.cfg. Разделитель - ;
