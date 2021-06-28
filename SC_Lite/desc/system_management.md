---
title : "Управление узлом"
description : ""
weight : 8
---

PROTEI SC_Lite — программное обеспечение, запускаемое на серверах с операционной системой Alt8SP/CentOS/RedHat. В PROTEI SC_Lite используются следующие директории: 

- */usr/protei/Protei\_SCP* — рабочая директория; 
- */usr/protei/Protei\_SCP/bin* — директория для исполняемых файлов; 
- */usr/protei/Protei\_SCP/cdr* — директория для CDR–журналов; 
- */usr/protei/Protei\_SCP/config* — директория для конфигурационных файлов; 
- */usr/protei/Protei\_SCP/logs* — директория для хранения лог–файлов. 

Чтобы запустить PROTEI SC_Lite, следует выполнить одну из команд: 

- команду `systemctl start` от лица суперпользователя;
```bash
[protei@SCL]$ sudo systemctl start scl
```

- запустить скрипт `start` из рабочей папки.
```bash
[protei@SCL]$ sh /usr/protei/Protei_SCL/start
```

Чтобы остановить PROTEI SC_Lite, следует выполнить одну из команд: 

- команду `systemctl stop` от лица суперпользователя;
```bash
[protei@SCL]$ sudo systemctl stop scl
```

- запустить скрипт `stop` из рабочей папки.
```bash
[protei@SCL]$ sh /usr/protei/Protei_SCL/stop
```

Чтобы проверить текущее состояние PROTEI SC_Lite, следует выполнить команду `status`:
```bash
[protei@SCL]$ sudo systemctl status scl
● scl.service – scl
Loaded: loaded (/usr/lib/systemd/system/scl.service; disabled; vendor preset: disabled)
Active: active (running) since Mon 2020–10–01 13:26:38 MSK; 1 weeks 1 days ago
Main PID: 8945 (SC_Lite)
CGroup: /system.slice/scl.service
└─8945 ./bin/Protei_SCL
```

Чтобы проверить текущую версию Узла PROTEI SCP, следует выполнить команду `version`: 
```bash
[protei@SCL]$ sh /usr/protei/Protei_SCL/version
Start: Protei_SCL_GSM
Protei_SCL_GSM
ProductCode 6.2.39.3 build 524
Supported license
        Sigtran
        Release

SIGTRAN M2PA
ProductCode 4.2.0.16 build 1 
RFC4165
```

Чтобы перезагрузить PROTEI SC_Lite, следует выполнить одну из команд: 

- команду `systemctl restart` от лица суперпользователя;
```bash
[protei@SCL]$ sudo systemctl restart scl
```
- запустить скрипт `restart` из рабочей папки.
```bash
[protei@SCL]$ sh /usr/protei/Protei_SCL/restart
```

Чтобы перезагрузить конфигурационный файл *file.cfg*, следует выполнить команду `reload`: 
```bash
[protei@SCL]$ /usr/protei/Protei_SCL/reload file.cfg
```

Чтобы записать дамп памяти, следует выполнить команду `core_dump`:
```bash
[protei@SCL]$ sh /usr/protei/Protei_SCL/core_dump
Are you sure you want to continue? y
Core dump generated!
```

Файл дампа хранится в директории /var/lib/systemd/coredump.

Чтобы вывести на экран записи журнала *trace.log*, следует выполнить команду `trace`:
```bash
[protei@SCL]$ sh /usr/protei/Protei_SCL/trace
```
