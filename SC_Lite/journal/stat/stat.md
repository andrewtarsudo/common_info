---
title : "Статистика принятых сообщений"
description : ""
weight : 1
---

Идентификатор журнала в файле *trace.cfg* - stat.
Формат названия файла: stat–YYYYMMDD–hhmm.log.
YYYYMMDD-hhmm - дата и время начала сбора статистики.

### Формат записи:

DateTime; StatName; MsgName; Start_stat_time; SuccessCount; FailCount; MaxSpeed; RegTimeMax;<br>
StatName; MsgName; Start_stat_time; SuccessCount; FailCount; MaxSpeed; RegTimeMax;<br>
StatName; MsgName; Start_stat_time; SuccessCount; FailCount; MaxSpeed; RegTimeMax;

### Описание полей

1. DateTime - Дата и время формирования записи.
2. StatName - Имя статистики. Значение по умолчанию - stat.
3. <a name="msgname">MsgName</a> - Название счетчика SMS–сообщений.
4. Start_stat_time - Время начала сбора статистики. Формат: hh:mm:ss.
5. SuccessCount - Количество успешно обработанных SMS–сообщений.
6. FailCount - Количество неуспешно обработанных SMS–сообщений.
7. MaxSpeed - Максимальная производительность обработки, количество SMS–сообщений в секунду за определенный промежуток времени.
8. RegTimeMax - Время, в течение которого фиксировалась максимальная
производительность.

Значения п. 2-8 выводятся друг за другом последовательно для [MsgName](#msgname) = Send MT/Receive MT/Receive MO.
