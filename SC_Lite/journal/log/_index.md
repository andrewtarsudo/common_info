---
title : "Логирование"
description : ""
weight : 3
---

Все журналы настраиваются в файле *trace.cfg*.

* **trace** - общий журнал действий;
* **alarm** - журнал аварий системы;
* **binary** - записи дампа;
* **config** - журнал загрузок конфигурационных файлов, списков абонентов и словарей;
* **error** - журнал вывода ошибок в системе;
* **fsm** - журнал, отображающий все пересылаемые сообщения;
* **info** - общий журнал событий;
* **logics** - журнал статистики состояния логик;
* **profilers** - журнал использования физических ресурсов и логик приложения;
* **sctp_binary** - дамп SCTP–соединений;
* **si** - журнал действий сокет–интерфейса;
* **smpp** - журнал SMPP–соединений;
* **stat** - журнал статистики;
* **stderr** - общий журнал вывода ошибок;
* **stdout** - общий журнал вывода;
* **warning** - общий журнал предупреждений.

Отдельные подсистемы также имеют несколько журналов:

* alarm_tree & alarm_snmp & alarm_warning & alarm_info - журналы подсистемы AP;
* brt_trace & brt_binary - журналы подсистемы BRT;
* diam_trace & diam_warning - журналы подсистемы Diameter;
* M2PA_trace & M2PA_warning & M2PA_info - журналы подсистемы M2PA;
* M3UA_trace & M3UA_warning & M3UA_info - журналы подсистемы M3UA;
* SCCP_trace & SCCP_warning - журналы подсистемы SCCP;
* Sg_trace & Sg_info & Sg_warning - журналы подсистемы Sg;
* si_info & si_warning - журналы подсистемы SI;
* smpp_binary & smpp_login - журналы подсистемы SMPP;
* TCAP_trace & TCAP_warning & TCAP_stat - журналы подсистемы TCAP.
