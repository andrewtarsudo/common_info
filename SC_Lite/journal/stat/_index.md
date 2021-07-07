---
title : "Статистика"
description : ""
weight : 4

---

Ведение статистики включается в конфигурационном файле [gsm.cfg]() в секции [Statistics](). 

### Файлы статистики

Для записи статистики в файл необходимо задать соответствующие идентификаторы в файлах *trace.cfg* и *statistics.cfg*.

* [stat](stat) - статистика принятых сообщений;
* [statussd](statussd) - статистика принятых USSD–сообщений.

### Online-статистика

Online-статистика передает данные на внешнее приложение по протоколу SNMP. Событие: STAT.
Также есть возможность запроса мгновенного состояния статистики с помощью SNMP Get запроса SCL.Traffic.Stat.{type}.

Подробности по формату SNMP-статистики на странице [аварий]().