---
title : "diameter.cfg"
description : "Файл настройки локального Diameter-узла"
weight : 3
---
В файле настраиваются следующие параметры:
* локальный адрес узла;
* локальные возможности узла, которые будут использоваться при установлении соединения;
* значения таймеров.

Ключ для reload - **reload diameter.cfg**.

Список разделов:

* **[Common](#common)**
* **[LocalAddress](#localaddress)**
* **[LocalPeerCapabitities](#localpeercapabitities)**
* **[Timers](#timers)**

## Описание параметров
|Name|Description|Type|Default|O/M|P/R|Version|
|:---|:----------|:---|:------|:--|:--|:------|
|**<a name="common">[Common]</a>**||
|RequestQueueLimit|Допустимое количество запросов, ожидающих отправку в сокете.|int|0 , без ограничений.|O|R||
|**<a name="localaddress">[LocalAddress]</a>**|параметры адреса локального host||
|LocalHost|Адрес локального сетевого интерфейса.|ip||M|P||
|LocalPort|Локальный IP-порт.|int||M|P||
|local_interfaces|Адреса ip:port для мультихоуминга.|string||O|P||
|remote_interfaces|Белые адреса ip:port, доступные для мультихоуминга.|string||O|P||
|Transport|Транспортный протокол. Возможные значения:<br>tcp/sctp.|string|tcp|O|P||
|InStreams|Количество входящих SCTP-потоков.|int 1-65535|1|O|P||
|OutStreams|Количество исходящих SCTP-потоков.|int 1-65535|1|O|P||
|MaxInitRetransmits|Количество попыток отправить сообщение INIT, прежде чем считать хост недоступным.|int|10|O|R||
|InitTimeout|Время ожидания сообщения INIT_ACK.|int ms|1000|O|R||
|RtoMax|Максимальное значение RTO.|int ms|60000|O|R||
|RtoMin|Минимальное значение RTO.|int ms|1000|O|R||
|RtoInitial|Первоначальное значение RTO.|int ms|3000|O|R||
|HbInterval|Периодичность отправления heartbeat-сообщения.|int ms|30000|O|R||
|AssociationMaxRetrans|Максимальное количество переадресаций, при превышении которого хост считается недоступным.|int|10|O|R||
|**<a name="localpeercapabitities">[LocalPeerCapabitities]</a>**|параметры участника Peer–to–Peer сети||
|Origin-Host|Значение Origin-Host для протокола Diameter. Подробное описание приведено в <a href="https://datatracker.ietf.org/doc/html/rfc6733">RFC 6733</a>. Формат:<br>#Host.epc.mnc#Mnc.mcc#Mcc.3gppnetwork.org.|string||M|R||
|Origin-Realm|Значение Origin-Realm для протокола Diameter. Подробное описание приведено в <a href="https://datatracker.ietf.org/doc/html/rfc6733">RFC 6733</a>.|string||M|R||
|Vendor-ID|Идентификатор Vendor-ID. Подробное описание приведено в <a href="https://datatracker.ietf.org/doc/html/rfc6733">RFC 6733</a>.|int||M|R||
|Product-Name|Название системы Product-Name. Подробное описание приведено в <a href="https://datatracker.ietf.org/doc/html/rfc6733">RFC 6733</a>.|string||M|R||
|Firmware-Revision|Версия ПО Firmware-Revision. Подробное описание приведено в <a href="https://datatracker.ietf.org/doc/html/rfc6733">RFC 6733</a>.|int||O|R||
|Origin-State-Id|Идентификатор состояния Origin-State-Id. Подробное описание приведено в <a href="https://datatracker.ietf.org/doc/html/rfc6733">RFC 6733</a>.|int||O|R||
|Host-IP-Address|Адрес Host-IP-Address. Подробное описание приведено в <a href="https://datatracker.ietf.org/doc/html/rfc6733">RFC 6733</a>.|list, ip||M|R||
|Auth-Application-Id|Идентификатор приложения Auth-Application-Id. Подробное описание приведено в <a href="https://datatracker.ietf.org/doc/html/rfc6733">RFC 6733</a>.|list, int||O|R||
|Acct-Application-Id|Идентификатор приложения Acct-Application-Id. Подробное описание приведено в <a href="https://datatracker.ietf.org/doc/html/rfc6733">RFC 6733</a>.|list, int||O|R||
|Vendor-Specific-Application-Id|Идентификатор приложения Vendor-Specific-Application-Id. Подробное описание приведено в <a href="https://datatracker.ietf.org/doc/html/rfc6733">RFC 6733</a>. Формат указан [ниже](#vendorspecificapplicationid).|object||O|R||
|Inband-Security-Id|Идентификатор безопасности Inband-Security-Id. Подробное описание приведено в <a href="https://datatracker.ietf.org/doc/html/rfc6733">RFC 6733</a>.|list, int||O|R||
|Supported-Vendor-Id|Идентификатор Supported-Vendor-Id. Подробное описание приведено в <a href="https://datatracker.ietf.org/doc/html/rfc6733">RFC 6733</a>.|list, int||O|R||
|Case-Sensitive|Флаг хранения регистра в строковых значениях AVP.|bool|1|O|R||
|ReceivingFromAnyHost|Флаг принятия запросов от сторонних хостов.|bool|0|O|R||
|DRMP|Приоритет.|int<br>0-15||O|R||
|**<a name="timers">[Timers]</a>**||
|Tx_Timeout|Время ожидания ответа на запрос.|int ms|30000|O|R||
|Appl_Timeout|Время ожидания установления Diameter-соединения.<br> **Примечание.** Отсчитывается с момента отправления запроса на установление TCP–соединения до получения сообщения Capabilities-Exchange-Answer.|int ms|40000|O|R||
|Watchdog_Timeout|Время ожидания для отправки сообщений Watchdog, которые контролируют состояние соединения.<br>**Примечание.** Отсчитывается с момента отправки последнего сообщения, не обязательно DeviceWatchdogRequest.|int ms|10000|O|R||
|Reconnect_Timeout|Время ожидания на переустановление соединения от момента разрыва соединения до попытки восстановления.|int ms|30000|O|R||

Формат элементов списка <a name="vendorspecificapplicationid">Vendor–Specific–Application–Id:
```
{
  Vendor–Id = #idVendor;
  Auth–Application–Id = #idApp;
}
```
либо
```
{
  Vendor–Id = #idVendor;
  Acct–Application–Id = #idApp;
}
```
