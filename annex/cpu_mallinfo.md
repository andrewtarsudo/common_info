CPU
|Term|Meaning|Description|
|:---|:------|:----------|
|us|user cpu time (or) % CPU time spent in user space|процессорное время в контексте пользователя или % времени работы процессора, затраченного в пространстве пользователя|
|ni|user nice cpu time (or) % CPU time spent on low priority processes|процессорное время в контексте пользователя для вежливых запросов или % времени работы процессора, затраченного на процессы с низким приоритетом|
|sy|system cpu time (or) % CPU time spent in kernel space|процессорное время в контексте системы или % времени работы процессора, затраченного в пространстве ядра|
|id|idle cpu time (or) % CPU time spent idle|процессорное время простоя или % времени работы процессора в бездействии|
|wa|io wait cpu time (or) % CPU time spent in wait (on disk)|процессорное время ожидания отклика или % времени работы процессора, затраченного на ожидание ответа|
|hi|hardware irq (or) % CPU time spent servicing/handling hardware interrupts|время выполнения аппаратных запросов на прерывание или % времени работы процессора, затраченного на исполнение/обработку аппаратных запросов на прерывание|
|si|software irq (or) % CPU time spent servicing/handling software interrupts|время выполнения программных запросов на прерывание или % времени работы процессора, затраченного на исполнение/обработку программных запросов на прерывание|
|st|steal time, % CPU time in involuntary wait by virtual cpu while hypervisor is servicing another processor (or) % CPU time stolen from a virtual machine|% времени работы процессора, затраченного на вынужденное ожидание виртуального процессора во время обслуживания гипервизором другой процессора или % времени работы процессора, недополученного виртуальной машиной|

mallinfo
|Term|Meaning|Description|
|:---|:------|:----------|
|arena|user cpu time (or) % CPU time spent in user space|процессорное время в контексте пользователя или % времени работы процессора, затраченного в пространстве пользователя|
|ordblks|user nice cpu time (or) % CPU time spent on low priority processes|процессорное время в контексте пользователя для вежливых запросов или % времени работы процессора, затраченного на процессы с низким приоритетом|
|sy|system cpu time (or) % CPU time spent in kernel space|процессорное время в контексте системы или % времени работы процессора, затраченного в пространстве ядра|
|id|idle cpu time (or) % CPU time spent idle|процессорное время простоя или % времени работы процессора в бездействии|
|wa|io wait cpu time (or) % CPU time spent in wait (on disk)|процессорное время ожидания отклика или % времени работы процессора, затраченного на ожидание ответа|
|hi|hardware irq (or) % CPU time spent servicing/handling hardware interrupts|время выполнения аппаратных запросов на прерывание или % времени работы процессора, затраченного на исполнение/обработку аппаратных запросов на прерывание|
|si|software irq (or) % CPU time spent servicing/handling software interrupts|время выполнения программных запросов на прерывание или % времени работы процессора, затраченного на исполнение/обработку программных запросов на прерывание|
|st|steal time, % CPU time in involuntary wait by virtual cpu while hypervisor is servicing another processor (or) % CPU time stolen from a virtual machine|% времени работы процессора, затраченного на вынужденное ожидание виртуального процессора во время обслуживания гипервизором другой процессора или % времени работы процессора, недополученного виртуальной машиной|
