---
title : "Аварии"
description : ""
weight : 5
---

Столбец Type/Address задает используемые компонентные типы и адреса. В большинстве случаев тип и адрес совпадают, некоторые адреса имеют дополнительную переменную часть указанную в фигурных скобках.

Все переменные имеют тип AP_TYPE_STRING.

|Type/address|Name|Value|Description|
|:-----------|:---|:----|:----------|
|**SCL**|||**Общее состояние приложения Protei SC_Lite** 
||OSTATE|{"ACTIVATE","FAIL"}|Оперативное состояние приложения|
|**SCL.OVRLOAD.Handler.SL**|||**Перегрузка занятых логик**|
||OSTATE|{"ACTIVATE","FAIL"}|Активация/деактивация перегрузки| 
||PARAM|Handlers = {}|Количество занятых логик|
|**SCL.OVRLOAD.Handler.SendSMS**|||**Перегрузка занятых SendSMS–логик**|
||OSTATE|{"ACTIVATE","FAIL"}|Активация/деактивация перегрузки|
||PARAM|Handlers = {}|Количество занятых логик SendSMS|
|**SCL.OVRLOAD.Queue.Logic**|||**Превышение внутренних очередей примитивов**|
||OSTATE|{"ACTIVATE","FAIL"}|Активация/деактивация превышения|
||PARAM|Size = {}|Размер очереди|
|**SCL.OVRLOAD.Traffic.TCAP.In**|||**Превышение входящего TCAP-трафика**|
||OSTATE|{"ACTIVATE","FAIL"}|Превышение ограничения InThreshold зафиксировано/не зафиксировано|
||PARAM|Count = {}|Величина InThreshold|
|**SCL.OVRLOAD.Traffic.TCAP.Out**|||**Превышение исходящего TCAP-трафика**|
||OSTATE|{"ACTIVATE","FAIL"}|Превышение ограничения OutThreshold зафиксировано/не зафиксировано|
||PARAM|Count = {}|Величина OutThreshold|
|**SCL.OVRLOAD.Traffic.TCAP.Total**|||**Превышение суммарного TCAP-трафика**|
||OSTATE|{"ACTIVATE","FAIL"}|Превышение ограничения TotalThreshold зафиксировано/не зафиксировано|
||PARAM|Count = {}|Величина TotalThreshold|
|**SCL.OVRLOAD.LICENSE.MINOVR**|||**Превышение ограничений лицензии**|
||OSTATE|{"ACTIVATE","FAIL"}|Превышение ограничения TrafficNominal зафиксировано/не зафиксировано|
||PARAM|CallsCount = {}|Величина TrafficNominal|
|**SCL.OVRLOAD.LICENSE.MAJOVR**|||**Превышение ограничений лицензии в течение длительного времени**|
||OSTATE|{"ACTIVATE"}|Постоянное превышение ограничения в течение TrafficThresholdInterval зафиксировано|
||OSTATE|{"FAIL"}|Превышение ограничения в течение CheckInterval не зафиксировано|
||PARAM|Count = {}|Величина TrafficThresholdInterval|
|**Sg.BRT{#ConnID}**|||Общее состояние BRT|
||OSTATE|{"ACTIVATE","FAIL"}|Соединение активно/не активно|
||PARAM|BRT_ID = {}|Идентификатор BRT|
|SCL.Traffic.Stat|||Статистика обработанных SMS|
||STAT|STAT|Статистика|
||PARAM|{<br>&nbsp;&nbsp;Name = {};<br>&nbsp;&nbsp;Start = {};<br>&nbsp;&nbsp;ReceiveMO = {<br>&nbsp;&nbsp;&nbsp;&nbsp;Count;Rejected;MaxSpeed;<br>&nbsp;&nbsp;&nbsp;&nbsp;TimeOfMaxSpeed;<br>&nbsp;&nbsp;};<br>&nbsp;&nbsp;ReceiveMT = {<br>&nbsp;&nbsp;&nbsp;&nbsp;Count;Rejected;MaxSpeed;<br>&nbsp;&nbsp;&nbsp;&nbsp;TimeOfMaxSpeed;<br>&nbsp;&nbsp;};<br>&nbsp;&nbsp;SendMT = {<br>&nbsp;&nbsp;&nbsp;&nbsp;Count;Rejected;MaxSpeed;<br>&nbsp;&nbsp;&nbsp;&nbsp;TimeOfMaxSpeed;<br>&nbsp;&nbsp;};<br>}|Значение статистики|
