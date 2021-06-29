---
title : "Процедура обращения к платформе IRIS"
description : ""
weight : 6
---

{{<mermaid>}}
sequenceDiagram
  participant M as MSC
  participant SL as SC_Lite
  participant IN as IN
  participant I as IRIS
  participant O as OCS
  participant S as SMSC
autonumber
  M ->> SL: MAP-MO-FSM (src_real; dest_virt)
  SL ->> IN: HTTP GET vnumber (src_real; dest_virt; dcs)
  IN ->> SL: HTTP Response (src_virt; dest_real; footer)
  SL ->> I: HTTP/XML Request
  I ->> SL: HTTP/XML Response (responseCode)
  SL ->> O: Diameter CCR-Initial (src_real; dest_virt)
  O ->> SL: Diameter CCA-Initial
  SL ->> S: smpp_data_sm (src_real; dest_real; footer)
  S ->> SL: smpp_data_sm_resp
  SL ->> O: Diameter CCR-Termination (src_real; dest_virt)
  O ->> SL: Diameter CCA-Termination
  SL ->> M: MAP-MO-FSM_ACK
{{</mermaid>}}

### HTTP Request:
```http
<IRIS>
  <Version value="1" />
  <Message value="ModelRequest" />
  <MessageTypeId value="70" />
  <MessageId value="#msgId" />
  <sessionId value=#sessionId />
  <timestamp value=YYYY–MM–DD hh:mm:ss />
  <vlr value=#addVlr />
  <partsQty value=#numParts />
  <partNumber value=#currNum />
  <smsId value=#smsId />
  <msgSubType value=#typeMsg />
  <smsBody value=#text />
  <msisdnA value=#cgMsisdn />
  <msisdnB value=#cdMsisdn />
  <msgType value=SCL />
</IRIS>
```
### HTTP Response:

```http
<IRIS>
  <Version value="1" />
  <Message value="ModelResponse" />
  <IrisInstance value="SP_1" />
  <MessageTypeId value="70" />
  <SystemTime value="2019–02–25 14:54:50" />
  <UniqueRecordId value="#recordId" />
  <MessageId value="#msgId" />
  <Merging value="0" />
  <InstanceStatus value="#status" />
  <Latency value="1.07" />
  <ErrorCode value="#errorCode" />
  <responseCode value=#respCode />
</IRIS>
```

### Описание параметров запроса и ответа

* sessionId - Уникальный идентификатор операции;
* timestamp - Дата и время совершения действия. UTC–дата и время в формате ISO 8601.<br>**Примечание.** Время указывается в часовом поясе UTC+3 (Мск);
* msisdnA - MSISDN отправителя. Max: 15 символов;
* msisdnB - MSISDN получателя. Max: 15 символов;
* smsBody - Текст сообщения;
* smsId - Идентификатор сцепленного SMS. Диапазон: 0–255;
* partsQty - Количество частей сцепленного SMS. Диапазон: 0–255;
* partNumber - Номер части SMS. Диапазон: 0–255;
* vlr - Адрес коммутатора. Max: 15 символов;
* [msgSubType](#msgsubtype) - Вид сообщения;
* msgType - Отправитель сообщения. Значение - всегда SCL.

#### <a name="msgsubtype">msgSubType</a>
Возможные значения:
* MT - входящие SMS;
* MO - исходящие SMS;
* HR - Home Routing SMS.
